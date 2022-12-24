diff_tool = {
	ready: false,
	free_viewer_id: 0,
	viewers: [],

	files_to_compare: [],

	init: function () {
		this.ready = true;
	},

	//

	construct_viewer: function () {
		var viewer_instance = {
			viewer_id: -1,
			window_id: -1,

			container: null,

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

				this.render();
			},

			render: function () {
				var self = this;
				var e = this.container;
				e.innerHTML = "";

				var d = document.createElement("div");
				e.appendChild(d);
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

	add_to_compare: function (locator) {
		if (!this.is_in_compare(locator))
			this.files_to_compare.push(locator);
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
