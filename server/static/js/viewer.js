import * as THREE from 'three';
import { OrbitControls } from 'OrbitControls';
import { OBJLoader } from 'OBJLoader';

viewer = {
	ready: false,

	renderer: null,
	camera: null,
	controls: null,
	scene: null,

	aborted: false,
	rendering: false,

	__track_resize: true,

	init: function () {
		this.ready = true;
	},

	//

	show_mesh: function (model) {
		this.show();
		this.make_renderer();

		var loader = new OBJLoader();
		var self = this;
		loader.load(model, function (geometry) {
			geometry.scale.x = 3;
			geometry.scale.y = 3;
			geometry.scale.z = 3;
			self.scene.add(geometry);
		}, undefined, function (err) {
			console.error(err);
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

		var e = document.getElementById("model_viewer");
		e.onclick = function (ev) { if (ev.target == e) self.hide(); };
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

	show: function (e) {
		e = e || document.getElementById("model_viewer");
		e.classList.add("open");
	},

	hide: function (e) {
		e = e || document.getElementById("model_viewer");
		e.classList.remove("open");
	},

	make_renderer: function (e) {
		e = e || document.getElementById("model_renderer");
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

viewer.init();
