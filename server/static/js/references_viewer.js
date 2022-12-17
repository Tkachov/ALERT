references_viewer = {
	ready: false,
	free_viewer_id: 0,
	viewers: [],

	init: function () {
		this.ready = true;
	},

	//

	construct_viewer: function (shortname, fullname, locator) {
		var viewer_instance = {
			viewer_id: -1,
			window_id: -1,

			locator: null,
			depth: 0,
			unique: false,
			info: null,
			container: null,

			init: function (viewer_id, shortname, fullname, locator) {
				this.viewer_id = viewer_id;

				var title = fullname + " — References Viewer";
				var button_title = shortname + " — References Viewer";
				var e = windows.new_window(title, button_title);
				e.classList.add("references_viewer");
				this.container = e;

				var w = windows.get_latest_window();
				if (w != null) {
					this.window_id = w.wid;

					var self = this;
					var cb = function () {
						var w2 = windows.get_window_by_id(self.window_id);
						windows.unsubscribe_from_window(w2, cb);
						references_viewer.destroy_viewer(self);
					};

					windows.subscribe_to_window(w, cb);
				}

				this.locator = locator;
				this.get_references();
			},

			render: function () {
				var self = this;
				var e = this.container;
				e.innerHTML = "";

				var d = document.createElement("div");
				e.appendChild(d);

				//

				if (this.info == null) {
					var sp = createElementWithTextNode("span", "Loading...");
					sp.className = "loading";
					d.appendChild(sp);
					return;
				}

				//

				var d2 = document.createElement("div");
				d2.className = "controls";
				d.appendChild(d2);

				{
					var cb_id = "unique_refs_" + Date.now();

					var cb = document.createElement("input");
					cb.type = "checkbox";
					cb.id = cb_id;
					cb.checked = self.unique;

					var lb = createElementWithTextNode("label", "Hide repeating references");
					lb.htmlFor = cb_id;

					var p = document.createElement("p");
					p.className = "checkbox_line";
					p.appendChild(cb);
					p.appendChild(lb);
					d2.appendChild(p);

					cb.onchange = function () {
						self.unique = cb.checked;
						self.render();
					};
				}

				{
					var depth_input = document.createElement("input");
					depth_input.type = "number";
					depth_input.value = self.depth;

					var p = document.createElement("p");
					p.appendChild(createElementWithTextNode("span", "Depth: "));
					p.appendChild(depth_input);
					d2.appendChild(p);

					var btn = createElementWithTextNode("button", "Refresh");
					btn.onclick = function () {
						self.depth = depth_input.value;
						self.get_references();
					};
					d2.appendChild(btn);
				}

				//

				var unique_refs = new Map();
				for (var r of this.info.references) {
					if (unique_refs.has(r.asset_id)) continue;
					unique_refs.set(r.asset_id, 1);
				}

				var sp = createElementWithTextNode("span", (this.info.references.length == 0 ? "No references found" : unique_refs.size + " references found:"));
				sp.style.display = "block";
				sp.style.padding = "2pt";
				sp.style.marginBottom = "10pt";
				d.appendChild(sp);

				if (this.info.references.length == 0) return;

				//

				// TODO: checkboxes to select and actions to perform (like stage all selected)

				var t = document.createElement("table");

				var tr = document.createElement("tr");
				tr.appendChild(createElementWithTextNode("th", "Depth"));
				tr.appendChild(createElementWithTextNode("th", "Name"));
				tr.appendChild(createElementWithTextNode("th", "Referenced in"));
				tr.appendChild(createElementWithTextNode("th", "Locations"));
				t.appendChild(tr);

				unique_refs = new Map();
				for (var r of this.info.references) {
					if (this.unique && unique_refs.has(r.asset_id)) continue;
					unique_refs.set(r.asset_id, 1);

					t.appendChild(this.make_reference_row(t, r));
				}

				d.appendChild(t);
			},

			make_reference_row: function (container, reference) {
				var tr = document.createElement("tr");
				tr.className = "result_entry";
				// tr.title = r.aid + (r.path != "" ? " - " + r.path : ""); // TODO: fullname / aid

				var namecell = document.createElement("td");
				namecell.appendChild(createElementWithTextNode("span", reference.filename)); // TODO: just name

				var browse = document.createElement("span");
				browse.className = "browse_button";
				browse.title = "Find in Asset Browser";
				browse.onclick = function () {
					assets_browser.make_asset_search_callback(reference.asset_id, "")(); // TODO: correct stage hint?
					var w = windows.get_window_by_id(0);
					if (w != null) w.button.click();
				};
				namecell.appendChild(browse);

				tr.appendChild(createElementWithTextNode("td", reference.depth));
				tr.appendChild(namecell);
				tr.appendChild(createElementWithTextNode("td", reference.referenced_in.join(", ")));
				tr.appendChild(createElementWithTextNode("td", reference.comment));

				return tr;
			},

			//

			get_references: function () {
				var self = this;
				self.info = null;

				ajax.postAndParseJson(
					"api/references_viewer/make", {
						locator: this.locator,
						depth: this.depth
					},
					function(r) {
						if (r.error) {
							// TODO: self.editor.search.error = r.message;
							return;
						}

						// TODO: self.editor.search.error = null;
						self.info = r.viewer;
						self.render();
					},
					function(e) {				
						// TODO: self.editor.search.error = e;
					}
				);

				self.render();
			}
		};

		viewer_instance.init(this.free_viewer_id, shortname, fullname, locator);
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

	show_viewer: function (locator, shortname, fullname) {
		this.construct_viewer(shortname, fullname, locator);
	}
};

references_viewer.init();
