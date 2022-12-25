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
			left_index: 0,
			right_index: 0,

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

				if (diff_tool.files_to_compare.length > 1) {
					this.left_index = diff_tool.files_to_compare.length - 2;
					this.right_index = diff_tool.files_to_compare.length - 1;
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
					for (var f of diff_tool.files_to_compare)
						select.appendChild(make_file_option(f));
					
					select.selectedIndex = index;
					if (diff_tool.files_to_compare.length < 2) select.disabled = true;

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
				p1.appendChild(p1_right);

				controls.appendChild(p1);

				// panes
				// selected left info
				// selected right info

				function make_file_info(container, index) {
					if (index < 0 || index >= diff_tool.files_to_compare.length) return;

					var locator = diff_tool.files_to_compare[index];
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

			//

			/*
			get_references: function () {
				var self = this;
				self.info = null;

				ajax.postAndParseJson(
					"api/diff_tool/make", {
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
			*/
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
