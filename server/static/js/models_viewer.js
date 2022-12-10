import * as THREE from 'three';
import { OrbitControls } from 'OrbitControls';
import { OBJLoader } from 'OBJLoader';
import { MTLLoader } from 'MTLLoader';

models_viewer = {
	ready: false,
	free_viewer_id: 0,
	viewers: [],

	init: function () {
		this.ready = true;
	},

	construct_viewer: function (shortname, fullname) {
		var viewer_instance = {
			viewer_id: -1,
			window_id: -1,

			container: null,
			renderer: null,
			camera: null,
			controls: null,
			scene: null,

			aborted: false,
			rendering: false,

			__track_resize: true,

			init: function (viewer_id, shortname, fullname) {
				this.viewer_id = viewer_id;

				var title = fullname + " — Models Viewer";
				var button_title = shortname + " — Models Viewer";
				var e = windows.new_window(title, button_title);
				e.classList.add("models_viewer");
				this.container = e;

				var r = document.createElement("div");
				r.className = "models_renderer";
				e.appendChild(r);

				var w = windows.get_latest_window();
				if (w != null) {
					this.window_id = w.wid;

					var self = this;
					var cb = function () {
						var w2 = windows.get_window_by_id(self.window_id);
						windows.unsubscribe_from_window(w2, cb);
						models_viewer.destroy_viewer(self);
					};

					windows.subscribe_to_window(w, cb);
				}
			},

			show_mesh: function (locator, looks, lod) {
				this.make_renderer();

				var mtl_url = "/api/models_viewer/mtl?locator=" + locator;
				var obj_url = "/api/models_viewer/obj?locator=" + locator + "&looks=" + looks + "&lod=" + lod;

				var self = this;
				var mtl_loader = new MTLLoader();
				mtl_loader.resourcePath = "/";
				mtl_loader.load(mtl_url, function (materials) { // TODO: update models_viewer to have /api endpoint for materials
					var loader = new OBJLoader();
					loader.setMaterials(materials);
					loader.load(obj_url, function (geometry) {
						geometry.scale.x = 3;
						geometry.scale.y = 3;
						geometry.scale.z = 3;
						self.scene.add(geometry);
						materials.preload();
					}, undefined, function (err) {
						console.error(err);
					});
				});

				var frontSpot = new THREE.SpotLight(0xFFFFFF);
				var backSpot = new THREE.SpotLight(0xFFFFFF);
				frontSpot.position.set(1000, 1000, 1000);
				backSpot.position.set(-500, -500, -500);
				this.scene.add(frontSpot);
				this.scene.add(backSpot);

				if (!this.rendering) {
					this.aborted = false;
					this.render();
				}
			},

			render: function () {
				if (this.aborted) {
					this.rendering = false;
					return;
				}

				this.rendering = true;
				requestAnimationFrame(this.render.bind(this));

				this._resize_renderer();
				this.renderer.render(this.scene, this.camera);
			},

			_resize_renderer: function () {
				if (!this.__track_resize) return;
				if (this.renderer == null || this.renderer.domElement == null) return;
				
				var p = this.renderer.domElement;
				if (p == null) return;

				var gp = p.parentElement;
				if (gp == null) return;
				
				if (gp.clientWidth != p.clientWidth || gp.clientHeight != p.clientHeight) {
					var w = gp.clientWidth;
					var h = gp.clientHeight;
					this.camera.aspect = w / h;
					this.camera.updateProjectionMatrix();
					this.renderer.setSize(w, h);
				}
			},

			abort: function () {
				this.aborted = true;
			},

			//

			make_renderer: function (e) {
				e = e || this.container.children[0];
				var w = e.clientWidth;
				var h = e.clientHeight;

				this.renderer = new THREE.WebGLRenderer();
				this.renderer.setSize(w, h);
				e.innerHTML = "";
				e.appendChild(this.renderer.domElement);

				this.camera = new THREE.PerspectiveCamera(75, w / h, 0.1, 10000);
				this.camera.position.z = 5;

				this.controls = new OrbitControls(this.camera, e);
				this.controls.target.set(0, 0, 0);
				this.controls.rotateSpeed = 0.5;
				this.controls.update();

				this.scene = new THREE.Scene();
				this.scene.background = new THREE.Color(0x282C34);
				this.renderer.render(this.scene, this.camera);
			},

			test: function () {
				if (this.renderer == null) {
					this.make_renderer();
				}

				const geometry = new THREE.TorusKnotGeometry(10, 1.3, 500, 6, 6, 20);
				const material = new THREE.MeshStandardMaterial({
					color: 0xfcc742,
					emissive: 0x111111,
					// specular: 0xffffff,
					metalness: 1,
					roughness: 0.55,
				});

				const mesh = new THREE.Mesh(geometry, material);
				mesh.scale.x = 0.1;
				mesh.scale.y = 0.1;
				mesh.scale.z = 0.1;
				this.scene.add(mesh);

				const frontSpot = new THREE.SpotLight(0xeeeece);
				const frontSpot2 = new THREE.SpotLight(0xddddce);
				frontSpot.position.set(1000, 1000, 1000);
				frontSpot2.position.set(-500, -500, -500);
				this.scene.add(frontSpot);
				this.scene.add(frontSpot2);

				var self = this;
				var r = this.renderer;
				const animate = function () {
					if (self.renderer != r) return; // stop test animation if renderer changed
					requestAnimationFrame(animate);

					mesh.rotation.x += 0.005;
					mesh.rotation.y += 0.005;
					mesh.rotation.z += 0.005;

					self.renderer.render(self.scene, self.camera);
				};
				animate();
			}
		};

		viewer_instance.init(this.free_viewer_id, shortname, fullname);
		this.free_viewer_id += 1;
		this.viewers.push(viewer_instance);

		return viewer_instance;
	},

	destroy_viewer: function (v) {
		if (v == null) return;

		var i = this.viewers.indexOf(v);
		if (i == -1) return;

		this.viewers.splice(i, 1);
	},

	show_mesh: function (locator, shortname, fullname, looks, lod) {
		looks = looks || "0";
		lod = lod || "0";
		var v = this.construct_viewer(shortname, fullname);
		v.show_mesh(locator, looks, lod);
	},

	test: function () {
		var v = this.construct_viewer("test", "test");
		v.test();
	}
};

models_viewer.init();
