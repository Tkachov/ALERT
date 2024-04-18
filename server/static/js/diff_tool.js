// ALERT: Amazing Luna Engine Research Tools
// This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
// For more details, terms and conditions, see GNU General Public License.
// A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

diff_tool = {
	ready: false,
	free_viewer_id: 0,
	viewers: [],

	files_to_compare: [],
	info_map: {},

	init: function () {
		this.ready = true;
	},

	//

	construct_viewer: function () {
		var viewer_instance = {
			viewer_id: -1,
			window_id: -1,

			container: null,
			local_files_to_compare: [],
			left_index: 0,
			right_index: 0,

			loading: 0,
			error: null,
			message: null,
			left_info: null,
			right_info: null,
			diff_info: null,
			mode: "compare",

			compare_dom: null,
			compare_dom_left_index: -1,
			compare_dom_right_index: -1,

			init: function (viewer_id) {
				this.viewer_id = viewer_id;

				var title = "Compare & Diff";
				var button_title = "Compare & Diff";
				var e = windows.new_window(title, button_title);
				e.classList.add("diff_tool");
				this.container = e;

				var w = windows.get_latest_window();
				if (w != null) {
					this.window_id = w.wid;

					var self = this;
					var cb = function () {
						var w2 = windows.get_window_by_id(self.window_id);
						windows.unsubscribe_from_window(w2, cb);
						diff_tool.destroy_viewer(self);
					};

					windows.subscribe_to_window(w, cb);
				}

				this.local_files_to_compare = diff_tool.files_to_compare.slice();

				if (this.local_files_to_compare.length > 1) {
					this.left_index = this.local_files_to_compare.length - 2;
					this.right_index = this.local_files_to_compare.length - 1;
				}

				this.render();
			},

			render: function () {
				var self = this;
				var e = this.container;
				e.innerHTML = "";

				var d = document.createElement("div");
				e.appendChild(d);

				this.render_controls(d);
				this.render_compare(d);
			},

			render_controls: function (d) {
				var self = this;
				var controls = document.createElement("div");
				controls.className = "controls";

				// panes
				// left options
				// right options
				// Compare button
				// Diff button

				function make_file_option(locator) {
					var entry = diff_tool.info_map[locator];

					var text = "";
					text += (entry.stage == "" ? "Game Archive" : entry.stage);
					text += " (span " + (entry.stage == "" ? ("#" + entry.span) : entry.span) + "): ";
					text += entry.name;

					var o = createElementWithTextNode("option", text);
					o.value = locator;
					return o;
				}

				function make_files_select(index, onchange) {
					var select = document.createElement("select");
					for (var f of self.local_files_to_compare)
						select.appendChild(make_file_option(f));
					
					select.selectedIndex = index;
					if (self.local_files_to_compare.length < 2) select.disabled = true;

					select.onchange = function () {
						onchange(select.selectedIndex);
					};
					return select;
				}

				var p1 = document.createElement("div");
				p1.className = "pane";

				var p1_left = document.createElement("div");
				p1_left.appendChild(make_files_select(this.left_index, function (index) { self.left_index = index; self.render(); }));
				p1.appendChild(p1_left);

				var p1_right = document.createElement("div");
				p1_right.appendChild(make_files_select(this.right_index, function (index) { self.right_index = index; self.render(); }));

				// `float: right` buttons
				var diff_button = createElementWithTextNode("button", "Diff");
				diff_button.onclick = this.diff_files.bind(this);
				p1_right.appendChild(diff_button);

				var cmp_button = createElementWithTextNode("button", "Compare");
				cmp_button.onclick = this.compare_files.bind(this);
				p1_right.appendChild(cmp_button);

				p1.appendChild(p1_right);

				controls.appendChild(p1);

				// panes
				// selected left info
				// selected right info

				function make_file_info(container, index) {
					if (index < 0 || index >= self.local_files_to_compare.length) return;

					var locator = self.local_files_to_compare[index];
					var entry = diff_tool.info_map[locator];
					container.appendChild(createElementWithTextNode("p", "Path: " + (entry.path == "" ? entry.name : entry.path)));
					container.appendChild(createElementWithTextNode("p", entry.aid));

					var desc = "";
					if (entry.type != null) {
						desc = entry.type + " (" + entry.sections + " sections)\n";
					}						
					desc += filesize(entry.size);
					container.appendChild(createElementWithTextNode("p", desc));
				}

				var p2 = document.createElement("div");
				p2.className = "pane info";

				var p2_left = document.createElement("div");
				make_file_info(p2_left, this.left_index);
				p2.appendChild(p2_left);

				var p2_right = document.createElement("div");
				make_file_info(p2_right, this.right_index);
				p2.appendChild(p2_right);

				controls.appendChild(p2);

				d.appendChild(controls);
			},

			render_compare: function (d) {
				if (this.compare_dom != null) {
					d.appendChild(this.compare_dom);
					classListSetIf(this.compare_dom, "not_actual", (this.left_index != this.compare_dom_left_index || this.right_index != this.compare_dom_right_index));
					return;
				}

				var self = this;
				var compare = document.createElement("div");
				compare.className = "compare";
				d.appendChild(compare);
				this.compare_dom = compare;

				if (this.loading > 0) {
					compare.appendChild(createElementWithTextNodeAndClass("span", "loading", "Loading..."));
					return;
				}

				if (this.error != null) {
					compare.appendChild(createElementWithTextNodeAndClass("b", "error", "Error:\n" + this.error));
					return;
				}

				if (this.message != null) {
					compare.appendChild(createElementWithTextNodeAndClass("span", "message", this.message));
					return;
				}

				if (this.mode == "compare")
					this.render_mode_compare(compare);
				else if (this.mode == "diff")
					this.render_mode_diff(compare);
			},

			render_mode_compare: function (compare) {
				if (this.left_info == null && this.right_info == null) {
					return;
				}

				if (this.left_info == null || this.right_info == null) {
					this.error = "Failed to get information on some of the selected files";
					this.render();
					return;
				}

				compare.classList.add("sections_viewer");

				// make headers

				var p1 = document.createElement("div");
				p1.className = "pane";

				var p1_left = document.createElement("div");
				p1_left.className = "header";
				p1.appendChild(p1_left);

				var p1_right = document.createElement("div");
				p1_right.className = "header";
				p1.appendChild(p1_right);

				compare.appendChild(p1);

				// make spoilers

				function make_spoiler_onclick(sections, other_sections, key) {
					return function () {
						var s1 = null;
						if (key in sections) s1 = sections[key];

						var s2 = null;
						if (key in other_sections) s2 = other_sections[key];

						if (s1 != null) {
							s1.classList.toggle("open");
							if (s1.classList.contains("open") && !isScrolledIntoView(s1))
								s1.scrollIntoView({behavior: "smooth", block: "start"});
						}

						if (s2 != null) {
							s2.classList.toggle("open");
							if (s1 == null && s2.classList.contains("open") && !isScrolledIntoView(s2))
								s2.scrollIntoView({behavior: "smooth", block: "start"});
						}
					};
				}

				var left_sections_order = sections_viewer._make_sections_order(this.left_info);
				var right_sections_order = sections_viewer._make_sections_order(this.right_info);

				var left_sections = {};
				var right_sections = {};

				function make_section_pane(compare, k, left, right, left_sections, right_sections) {
					if (left != null) {
						left.children[0].onclick = make_spoiler_onclick(left_sections, right_sections, k);
						left_sections[k] = left;
					}

					if (right != null) {
						right.children[0].onclick = make_spoiler_onclick(left_sections, right_sections, k);
						right_sections[k] = right;
					}

					if (left != null || right != null) {
						var p = document.createElement("div");
						p.className = "pane";

						var p_left = document.createElement("div");
						if (left == null) {
							var m = document.createElement("div");
							m.className = "missing";
							m.appendChild(createElementWithTextNode("span", "Not present in this asset"));
							p_left.appendChild(m);
						}
						else p_left.appendChild(left);
						p.appendChild(p_left);

						var p_right = document.createElement("div");
						if (right == null) {
							var m = document.createElement("div");
							m.className = "missing";
							m.appendChild(createElementWithTextNode("span", "Not present in this asset"));
							p_right.appendChild(m);
						}
						else p_right.appendChild(right);
						p.appendChild(p_right);

						compare.appendChild(p);
					}
				}

				var left_strings = null;
				if (this.left_info.strings.strings.length > 0) {
					left_strings = sections_viewer._make_strings_block_spoiler(this.left_info);
				}

				var right_strings = null;
				if (this.right_info.strings.strings.length > 0) {
					right_strings = sections_viewer._make_strings_block_spoiler(this.right_info);
				}

				make_section_pane(compare, "SB", left_strings, right_strings, left_sections, right_sections);

				for (var sect of left_sections_order) {
					var k = "" + sect[0];
					var left = sections_viewer._make_section_spoiler(this.left_info, sect);
					var right = null;
					for (var sect2 of right_sections_order) {
						var k2 = "" + sect2[0];
						if (k == k2) {
							right = sections_viewer._make_section_spoiler(this.right_info, sect2);
							break;
						}
					}
					make_section_pane(compare, k, left, right, left_sections, right_sections);
				}

				for (var sect of right_sections_order) {
					var k = "" + sect[0];
					if (k in left_sections) continue;

					var right = sections_viewer._make_section_spoiler(this.right_info, sect);
					var left = null;
					for (var sect2 of left_sections_order) {
						var k2 = "" + sect2[0];
						if (k == k2) {
							left = sections_viewer._make_section_spoiler(this.left_info, sect2);
							break;
						}
					}
					make_section_pane(compare, k, left, right, left_sections, right_sections);
				}

				// fill headers

				function fill_header(h, report, sections, other_sections, sections_order) {
					h.appendChild(createElementWithTextNode("b", report.header.length + " sections"));

					if (report.strings.strings.length > 0) {
						var x = sections_viewer._make_header_strings_block_button();
						x.onclick = make_spoiler_onclick(sections, other_sections, "SB");
						h.appendChild(x);
					}
		
					for (var s of sections_order) {
						var x = sections_viewer._make_header_section_button(report, s);
						x.onclick = make_spoiler_onclick(sections, other_sections, s[0]);
						h.appendChild(x);
					}
				}

				fill_header(p1_left, this.left_info, left_sections, right_sections, left_sections_order);
				fill_header(p1_right, this.right_info, left_sections, right_sections, right_sections_order);
			},

			render_mode_diff: function (compare) {
				if (this.diff_info.length == 0) {
					compare.appendChild(createElementWithTextNodeAndClass("span", "message", "Files are the same"));
					return;
				}

				compare.classList.add("sections_viewer");
				compare.classList.add("diff");

				this._fill_diff(compare, this.diff_info);
			},

			_fill_diff: function (container, info) {
				function make_spoiler_onclick(s) {
					return function () {
						s.classList.toggle("open");
					};
				}

				for (var d of info) {
					if ("message" in d) {
						container.appendChild(createElementWithTextNodeAndClass("span", "message", d.message));
						continue;
					}

					if ("group" in d) {
						var s = document.createElement("div");
						s.className = "spoiler";

						var sh = document.createElement("div");
						var clr = document.createElement("span");
						clr.style.background = "#BBB";
						sh.appendChild(clr);
						sh.appendChild(createElementWithTextNode("span", d.group));
						s.appendChild(sh);

						var c = document.createElement("div");
						this._fill_diff(c, d.differences);
						s.appendChild(c);

						sh.onclick = make_spoiler_onclick(s);

						container.appendChild(s);
						continue;
					}

					var p = document.createElement("div");
					p.className = "pane diff_left_right";

					var p_left = document.createElement("div");
					p_left.appendChild(createElementWithTextNode("span", (d.left == null ? "" : d.left)));
					p.appendChild(p_left);

					var p_right = document.createElement("div");
					p_right.appendChild(createElementWithTextNode("span", (d.right == null ? "" : d.right)));
					p.appendChild(p_right);

					container.appendChild(p);
				}
			},

			//

			compare_files: function () {
				var i1 = this.left_index;
				var i2 = this.right_index;
				if (i1 < 0 || i2 < 0 || i1 >= this.local_files_to_compare.length || i2 >= this.local_files_to_compare.length) return;

				this.error = null;
				this.message = null;
				this.left_info = null;
				this.right_info = null;
				this.mode = "compare";
				this.compare_dom = null;
				this.compare_dom_left_index = i1;
				this.compare_dom_right_index = i2;

				if (i1 == i2) {
					this.message = "Selected files are the same";
					this.render();
					return;
				}

				var left_locator = this.local_files_to_compare[i1];
				var right_locator = this.local_files_to_compare[i2];
				var left_entry = diff_tool.info_map[left_locator];
				var right_entry = diff_tool.info_map[right_locator];
				if (left_entry.type == null || right_entry.type == null) {
					this.message = "Some of the selected files are not comparable";
					this.render();
					return;
				}

				this.loading = 2;

				function load_info(self, locator, on_success) {
					ajax.postAndParseJson(
						"api/sections_viewer/make", { locator: locator },
						function(r) {
							self.loading -= 1;
							self.compare_dom = null;

							if (r.error) {
								if (self.error == null) self.error = r.message;
								else self.error += "\n" + r.message;
								self.render();
								return;
							}

							on_success(r.report);
							self.render();
						},
						function(e) {
							self.loading -= 1;
							self.compare_dom = null;

							if (self.error == null) self.error = e;
							else self.error += "\n" + e;
							self.render();
						}
					);
				}

				var self = this;
				load_info(self, left_locator, function (info) { self.left_info = info; });
				load_info(self, right_locator, function (info) { self.right_info = info; });

				this.render();
			},

			diff_files: function () {
				var i1 = this.left_index;
				var i2 = this.right_index;
				if (i1 < 0 || i2 < 0 || i1 >= this.local_files_to_compare.length || i2 >= this.local_files_to_compare.length) return;

				this.error = null;
				this.message = null;
				this.left_info = null;
				this.right_info = null;
				this.mode = "diff";
				this.compare_dom = null;
				this.compare_dom_left_index = i1;
				this.compare_dom_right_index = i2;

				if (i1 == i2) {
					this.message = "Selected files are the same";
					this.render();
					return;
				}

				var left_locator = this.local_files_to_compare[i1];
				var right_locator = this.local_files_to_compare[i2];				
				this.loading = 1;

				var self = this;
				ajax.postAndParseJson(
					"api/diff_tool/diff", { locator1: left_locator, locator2: right_locator },
					function(r) {
						self.loading = 0;
						self.compare_dom = null;

						if (r.error) {
							self.error = r.message;
							self.render();
							return;
						}

						self.error = null;
						self.diff_info = r.differences;
						self.render();
					},
					function(e) {
						self.loading = 0;
						self.compare_dom = null;
						self.error = e;
						self.render();
					}
				);

				this.render();
			}
		};

		viewer_instance.init(this.free_viewer_id);
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

	show_viewer: function () {
		this.construct_viewer();
	},

	add_to_compare: function (locator, entry, info) {
		if (!this.is_in_compare(locator))
			this.files_to_compare.push(locator);
		this.info_map[locator] = {
			stage: entry.stage,
			span: entry.span,
			aid: entry.aid,
			size: entry.size,
			name: entry.name,
			path: entry.path,

			type: info.type,
			sections: info.sections
		};
	},

	remove_from_compare: function (locator) {
		var index = this.files_to_compare.indexOf(locator);
		if (index != -1)
			this.files_to_compare.splice(index, 1);
	},

	is_in_compare: function (locator) {
		return this.files_to_compare.includes(locator);
	}
};

diff_tool.init();
