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

			locator: null,
			info: null,
			details_pane: null,
			details_lod_select: null,
			details_looks_checkboxes: null,
			details_use_materials_cb: null,
			loading: false,

			container: null,
			renderer: null,
			camera: null,
			controls: null,
			scene: null,
			obj_materials: null,
			obj_geometry: null,

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

			setup_viewer: function (locator, info, looks, lod) {
				this.locator = locator;
				this.info = info;

				this.make_details_pane();
				
				// update details selection
				{
					var default_lod = info.lods[0] + "";

					var default_look = "";
					var body_and_mask = "";
					var has_venom = false;

					for (var i=0; i<info.looks.length; ++i) {
						var l = info.looks[i];
						var n = l.name;

						if (n == "Default") default_look = i + "";
						else if (n == "body" || n == "mask") {
							if (body_and_mask != "") body_and_mask += ",";
							body_and_mask += i + "";
						} else if (n.toLowerCase().includes("venom")) {
							has_venom = true;
						}
					}

					var default_looks = (has_venom ? body_and_mask : default_look);

					looks = looks || default_looks;
					lod = lod || default_lod;

					var use_materials = true; // TODO: configurable

					this.details_lod_select.value = lod;
					this.details_use_materials_cb.querySelector("input[type=\"checkbox\"]").checked = use_materials;

					looks = looks.split(',');

					var cbs = this.details_looks_checkboxes.querySelectorAll("input[type=\"checkbox\"]");
					for (var cb of cbs) {
						cb.checked = (looks.includes(cb.name.substr(4)));
					}
				}

				this.show_selected_mesh();
			},

			make_details_pane: function () {
				if (this.details_pane == null) {
					this.details_pane = document.createElement("div");
					this.details_pane.className = "details";
					this.container.appendChild(this.details_pane);
				}

				var self = this;
				var info = this.info;
				var e = this.details_pane;
				e.innerHTML = "";

				var opener = document.createElement("span");
				opener.className = "opener";
				opener.onclick = function () { e.classList.toggle("open"); };
				e.appendChild(opener);

				var scrollbox = document.createElement("div");
				scrollbox.className = "scrollbox";
				e.appendChild(scrollbox);

				// lod selector

				function make_section(container, name) {
					var s = document.createElement("div");
					s.className = "collapsible";

					var h = createElementWithTextNode("span", name);
					s.appendChild(h);
					h.onclick = function () { s.classList.toggle("collapsed"); };

					var c = document.createElement("div");
					c.className = "content";
					s.appendChild(c);

					container.appendChild(s);
					return c;
				}

				var section_container = make_section(scrollbox, "Model Preview");

				if (this.details_lod_select == null) {
					function count_lod_meshes(lod_index) {
						var meshes = [];

						for (var l of info.looks) {
							var lod = l.lods[lod_index];
							for (var i = lod[0]; i < lod[0] + lod[1]; ++i) {
								if (!meshes.includes(i))
									meshes.push(i);
							}
						}

						return meshes.length;
					}

					function make_option(text, value) {
						var o = createElementWithTextNode("option", text);
						o.value = value;
						return o;
					}

					var select = document.createElement("select");
					for (var l of info.lods) {
						select.appendChild(make_option("LOD" + l + ": " + count_lod_meshes(l) + " meshes", l));
					}
					select.selectedIndex = 0;
					if (info.lods.length < 2) select.disabled = true;

					this.details_lod_select = select;
				}

				this.details_lod_select.disabled = this.loading;
				section_container.appendChild(this.details_lod_select);

				// looks

				function make_checkbox(base_id, name, text) {
					var cb_id = base_id + "_" + Date.now();

					var cb = document.createElement("input");
					cb.type = "checkbox";
					cb.name = name;
					cb.id = cb_id;
					cb.checked = false;

					var lb = createElementWithTextNode("label", text);
					lb.htmlFor = cb_id;

					var p = document.createElement("p");
					p.className = "checkbox_line";
					p.appendChild(cb);
					p.appendChild(lb);
					return p;
				}

				if (this.details_looks_checkboxes == null) {
					var d = document.createElement("div");
					d.className = "lookgroups";
					for (var i=0; i<info.looks.length; ++i) {
						d.appendChild(make_checkbox("display_lookgroup_" + i, "look" + i, info.looks[i].name));
					}

					this.details_looks_checkboxes = d;
				}

				var cbs = this.details_looks_checkboxes.querySelectorAll("input[type=\"checkbox\"]");
				for (var cb of cbs) {
					cb.disabled = this.loading;
				}

				section_container.appendChild(this.details_looks_checkboxes);

				// use_materials checkbox

				if (this.details_use_materials_cb == null) {
					this.details_use_materials_cb = make_checkbox("use_materials", "use_materials", "Load materials");
				}

				this.details_use_materials_cb.querySelector("input[type=\"checkbox\"]").disabled = this.loading;
				section_container.appendChild(this.details_use_materials_cb);

				// button to apply selected looks/lods & use_materials; button to reset?

				var b = createElementWithTextNode("button", (this.loading ? "Loading..." : "Reload"));
				// b.className = "";
				b.disabled = this.loading;
				b.onclick = this.show_selected_mesh.bind(this);
				section_container.appendChild(b);

				// materials list

				section_container = make_section(scrollbox, "Materials List");

				function make_asset_browse(aid) {
					return function () {
						assets_browser.make_asset_search_callback(aid, "")(); // TODO: correct stage hint?
						var w = windows.get_window_by_id(1);
						if (w != null) w.button.click();
					};
				}

				for (var i=0; i<this.info.materials.length; ++i) {
					var m = this.info.materials[i];
					var material = document.createElement("div");
					material.className = "material";
					material.appendChild(createElementWithTextNode("span", "#" + i + ": " + m.name));
					material.title = m.aid + " - " + m.file;

					var browse = document.createElement("span");
					browse.className = "browse_button";
					browse.onclick = make_asset_browse(m.aid);
					browse.title = "Find in Asset Browser";
					material.appendChild(browse);

					section_container.appendChild(material);
				}

				if (this.info.materials.length == 0) {
					var msg = createElementWithTextNode("span", "No materials");
					msg.className = "empty_message";
					section_container.appendChild(msg);
				}

				// meshes list

				section_container = make_section(scrollbox, "Meshes Visibility");

				if (this.obj_geometry != null) {
					function make_mesh_visibility_toggle(cb, mesh) {
						return function () {
							mesh.visible = cb.checked;
						};
					}

					for (var m of this.obj_geometry.children) {
						var cb_line = make_checkbox("mesh_visible_" + m.name, m.name, m.name);
						var cb = cb_line.querySelector("input[type=\"checkbox\"]");
						cb.checked = m.visible;
						cb.onchange = make_mesh_visibility_toggle(cb, m);
						section_container.appendChild(cb_line);
					}
				}

				if (this.obj_geometry == null || this.obj_geometry.children.length == 0) {
					var msg = createElementWithTextNode("span", (this.loading ? "Loading..." : "No meshes"));
					msg.className = "empty_message";
					section_container.appendChild(msg);
				}
			},

			show_selected_mesh: function () {
				if (this.details_pane == null) return;

				var lod = this.details_lod_select.value + "";

				var looks = "";
				var cbs = this.details_looks_checkboxes.querySelectorAll("input[type=\"checkbox\"]");
				for (var cb of cbs) {
					if (cb.checked) {
						if (looks != "") looks += ",";
						looks += cb.name.substr(4);
					}
				}

				var use_materials = this.details_use_materials_cb.querySelector("input[type=\"checkbox\"]").checked;

				this.show_mesh(looks, lod, use_materials);
			},

			show_mesh: function (looks, lod, use_materials) {
				this.make_renderer();

				this.loading = true;
				this.obj_materials = null;
				this.obj_geometry = null;
				this.make_details_pane();

				var locator = this.locator;
				var mtl_url = "/api/models_viewer/mtl?locator=" + locator;
				var obj_url = "/api/models_viewer/obj?locator=" + locator + "&looks=" + looks + "&lod=" + lod;

				if (use_materials)
					this.load_materials_then_geometry(mtl_url, obj_url);
				else
					this.load_geometry(obj_url);

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

			load_materials_then_geometry: function (mtl_url, obj_url) {
				var mtl_loader = new MTLLoader();
				mtl_loader.resourcePath = "/";

				var self = this;
				mtl_loader.load(mtl_url, function (materials) {
					self.obj_materials = materials;
					self.load_geometry(obj_url);
				}, undefined, function (err) { // TODO: onProgress to update progress bar or something
					console.error(err);
					self.loading = false;
					self.make_details_pane();
				});
			},

			load_geometry: function (obj_url) {
				var loader = new OBJLoader();
				if (this.obj_materials != null)
					loader.setMaterials(this.obj_materials);

				var self = this;
				loader.load(obj_url, function (geometry) {
					self.obj_geometry = geometry;

					geometry.scale.x = 3;
					geometry.scale.y = 3;
					geometry.scale.z = 3;
					self.scene.add(geometry);

					if (self.obj_materials != null)
						self.obj_materials.preload();

					self.loading = false;
					self.make_details_pane();
				}, undefined, function (err) { // TODO: onProgress to update progress bar or something
					console.error(err);
					self.loading = false;
					self.make_details_pane();
				});
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
		var self = this;
		ajax.postAndParseJson(
			"api/models_viewer/make", {
				locator: locator
			},
			function(r) {
				if (r.error) {
					// TODO: self.editor.search.error = r.message;
					return;
				}

				// TODO: self.editor.search.error = null;
				var v = self.construct_viewer(shortname, fullname);
				v.setup_viewer(locator, r.viewer, looks, lod);
			},
			function(e) {				
				// TODO: self.editor.search.error = e;
			}
		);
	},

	test: function () {
		var v = this.construct_viewer("test", "test");
		v.test();
	}
};

models_viewer.init();
