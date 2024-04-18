// ALERT: Amazing Luna Engine Research Tools
// This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
// For more details, terms and conditions, see GNU General Public License.
// A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

references_viewer = {
	ready: false,
	free_viewer_id: 0,
	viewers: [],

	init: function () {
		this.ready = true;
	},

	//

	construct_viewer: function (shortname, fullname, locator, aid) {
		var viewer_instance = {
			viewer_id: -1,
			window_id: -1,

			locator: null,
			fullname: null,
			aid: null,
			depth: 0,
			unique: false,
			info: null,
			container: null,
			checked: {},
			ref_count: null,

			init: function (viewer_id, shortname, fullname, locator, aid) {
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
				this.fullname = fullname;
				this.aid = aid;
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

				this.render_controls(d);

				//

				var new_checked = {};
				new_checked[this.aid] = this.checked[this.aid] || false;

				for (var r of this.info.references) {
					new_checked[r.asset_id] = this.checked[r.asset_id] || false;
				}
				this.checked = new_checked;

				//

				var sp = createElementWithTextNode("span", "");
				sp.style.display = "block";
				sp.style.padding = "2pt";
				sp.style.marginBottom = "10pt";
				this.ref_count = sp;
				d.appendChild(sp);

				if (this.info.references.length == 0) return;

				this.update_references_count();
				this.render_table(d);
			},

			render_controls: function (d) {
				var self = this;
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

				{
					var p = document.createElement("p");
					p.appendChild(createElementWithTextNode("span", "With selected: "));
					p.className = "selected_actions_group";
					d2.appendChild(p);

					var btn = createElementWithTextNode("button", "Add to stage...");
					btn.onclick = function () {
						self.add_selected_to_stage();
					};
					d2.appendChild(btn);
				}
			},

			update_references_count: function () {
				var unique_refs_count = 0;
				var selected_count = 0;				
				for (var k in this.checked) {
					++unique_refs_count;
					if (this.checked[k]) ++selected_count;
				}

				var pref = "";
				if (selected_count > 0) pref += " (" + selected_count + " selected)";

				var text = (this.info.references.length == 0 ? "No references found" : unique_refs_count + " references " + pref + " found:");
				this.ref_count.innerHTML = "";
				this.ref_count.appendChild(document.createTextNode(text));

				var e = this.container.querySelector(".controls");
				if (e != null) classListSetIf(e, "has_selected", (selected_count > 0));
			},

			render_table: function (d) {
				var t = document.createElement("div");
				this.render_table_headers(t);
				this.render_table_contents(t);
				d.appendChild(t);
			},

			render_table_headers: function (t) {
				var self = this;
				var tr = document.createElement("div");
				tr.className = "headers";

				var ref_line = document.createElement("div");
				ref_line.className = "ref_line";

				var cbcell = document.createElement("div");
				cbcell.className = "checkbox_column";

				var cb = document.createElement("input");
				cb.type = "checkbox";
				cb.name = "select_all";
				cb.checked = false;
				var self = this;
				var cbl = document.createElement("label");
				cbl.appendChild(cb);
				cbcell.appendChild(cbl);

				cb.onchange = function (ev) {
					for (var k in self.checked)
						self.checked[k] = cb.checked;

					var els = self.container.querySelectorAll(".ref input[type='checkbox']");
					for (var el of els) {
						el.checked = self.checked[el.name];
					}
					self.update_references_count();
				};

				ref_line.appendChild(cbcell);

				var namecell = document.createElement("div");
				namecell.className = "name_column";
				namecell.appendChild(createElementWithTextNode("span", "Name"));

				var browse = document.createElement("span");
				browse.className = "browse_button";
				ref_line.appendChild(namecell);

				var info_cell = document.createElement("div");
				info_cell.className = "info_column";
				ref_line.appendChild(info_cell);

				info_cell.appendChild(browse);
				info_cell.appendChild(createElementWithTextNode("span", "Referenced in"));
				info_cell.appendChild(createElementWithTextNode("span", "Locations"));
				tr.appendChild(ref_line);

				t.appendChild(tr);
			},

			render_table_contents: function (t) {
				var unique_refs = new Map();
				var containers = [t];
				var depth = -1;

				{
					var r = {
						filename: this.fullname,
						asset_id: this.aid,
						depth: -1,
						referenced_in: [],
						comment: ""
					};
					var first_row = this.make_reference_row(t, r);
					first_row.classList.remove("closed");

					t.appendChild(first_row);
					containers.push(t);

					unique_refs.set(r.asset_id, 1);
				}

				for (var r of this.info.references) {
					if (this.unique && unique_refs.has(r.asset_id)) continue;
					unique_refs.set(r.asset_id, 1);

					var row = this.make_reference_row(t, r, depth+1);
					if (r.depth != depth) {
						if (r.depth > depth) {
							var prev_row = containers[containers.length-1].lastChild;
							prev_row.classList.add("has_contents");
							containers.push(prev_row.lastChild);
							depth += 1;
						} else {
							while (depth > r.depth) {
								depth -= 1;
								containers.splice(containers.length - 1, 1);
							}
						}
					}

					row.firstChild.children[1].style.paddingLeft = (20*(depth+1) + 2) + "pt";
					row.firstChild.children[2].style.marginLeft = (-20*(depth+1) - 2) + "pt";

					containers[containers.length-1].appendChild(row);
				}
			},

			make_reference_row: function (container, reference) {
				var tr = document.createElement("div");
				tr.className = "ref closed";

				var ref_line = document.createElement("div");
				ref_line.className = "ref_line";
				ref_line.onclick = function () { tr.classList.toggle("closed"); };

				var cbcell = document.createElement("div");
				cbcell.className = "checkbox_column";

				var cb = document.createElement("input");
				cb.type = "checkbox";
				cb.name = reference.asset_id;
				cb.checked = this.checked[reference.asset_id];
				var self = this;
				var cbl = document.createElement("label");
				cbl.appendChild(cb);
				cbcell.appendChild(cbl);

				cbcell.onclick = function (ev) {
					ev.stopPropagation();
				};

				cb.onchange = function (ev) {
					self.checked[reference.asset_id] = cb.checked;
					var els = self.container.querySelectorAll("input[type='checkbox']");
					for (var el of els) {
						if (el.name == reference.asset_id) {
							el.checked = self.checked[reference.asset_id];
						}
					}
					self.update_references_count();
				};

				ref_line.appendChild(cbcell);

				var namecell = document.createElement("div");
				namecell.className = "name_column";
				namecell.appendChild(createElementWithTextNode("span", get_basename(reference.filename)));
				namecell.title = reference.asset_id + (reference.filename != "" ? " - " + reference.filename : "");

				var browse = document.createElement("span");
				browse.className = "browse_button";
				browse.title = "Find in Asset Browser";
				browse.onclick = function (ev) {
					assets_browser.make_asset_search_callback(reference.asset_id, "")(); // TODO: correct stage hint?
					var w = windows.get_window_by_id(0);
					if (w != null) w.button.click();
					ev.stopPropagation();
				};
				ref_line.appendChild(namecell);

				var info_cell = document.createElement("div");
				info_cell.className = "info_column";
				ref_line.appendChild(info_cell);

				info_cell.appendChild(browse);

				info_cell.appendChild(createElementWithTextNode("span", reference.referenced_in.join(", ")));
				info_cell.appendChild(createElementWithTextNode("span", reference.comment));
				tr.appendChild(ref_line);

				var content = document.createElement("div");
				content.className = "content";
				tr.appendChild(content);

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
			},

			add_selected_to_stage: function () {
				var list = [];
				var title = "";

				already_added = new Map();
				for (var r of this.info.references) {
					if (r.asset_id == this.aid) continue;
					if (already_added.has(r.asset_id)) continue;
					already_added.set(r.asset_id, 1);
					if (this.checked[r.asset_id])
						list.push(r);
				}

				if (this.checked[this.aid]) {
					title = this.fullname;
					if (list.length > 0)
						title += " and " + list.length + " references";
					list.push({
						filename: this.fullname,
						locator: this.locator
					});
				} else {
					title = list.length + " references of " + this.fullname;
				}

				if (list.length == 0) return;
				stage_selector.show_selector_for_list(title, list);
			}
		};

		viewer_instance.init(this.free_viewer_id, shortname, fullname, locator, aid);
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

	show_viewer: function (locator, shortname, fullname, aid) {
		this.construct_viewer(shortname, fullname, locator, aid);
	}
};

references_viewer.init();
