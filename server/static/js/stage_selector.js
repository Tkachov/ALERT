// ALERT: Amazing Luna Engine Research Tools
// This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
// For more details, terms and conditions, see GNU General Public License.
// A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

stage_selector = {
	ready: false,

	options: null,
	variants_checkbox: null,

	list: [],
	list_index: 0,
	error: null,

	init: function () {
		this.ready = true;

		var e = document.getElementById("stage_selector");
		e.onclick = function (ev) { if (ev.target == e) e.classList.remove("open"); };
	},

	//

	show_selector: function (locator, shortname, fullname, is_directory) {
		this._show_selector(
			"Adding " + fullname + " to stage...",
			{
				"type": (is_directory ? "directory" : "asset"),
				"locator": locator
			}
		);
	},

	show_selector_for_list: function (title, asset_ids_list) {
		this._show_selector(
			"Adding " + title + " to stage...",
			{
				"type": "list",
				"list": asset_ids_list
			}
		);
	},

	_show_selector: function (title, options) {
		this.options = options;

		var self = this;
		var e = document.getElementById("stage_selector");
		e.innerHTML = "";

		var d = document.createElement("div");
		e.appendChild(d);

		var p = createElementWithTextNode("p", title);
		d.appendChild(p);

		// TODO: don't show checkbox if no variants exist
		var show_variants_checkbox = true;
		if (options.type == "directory") show_variants_checkbox = false;
		else if (options.type == "list") show_variants_checkbox = false;

		var cb;
		if (show_variants_checkbox) {
			var cb_id = "all_spans";

			cb = document.createElement("input");
			cb.type = "checkbox";
			cb.id = cb_id;
			cb.checked = true;

			var lb = createElementWithTextNode("label", "Add asset's variants from all spans"); // TODO: count of variants
			lb.htmlFor = cb_id;

			var p = document.createElement("p");
			p.className = "checkbox_line";
			p.appendChild(cb);
			p.appendChild(lb);
			d.appendChild(p);

			this.variants_checkbox = cb;
		}

		var d2 = document.createElement("div");
		d2.className = "new_stage";

		d2.appendChild(createElementWithTextNode("p", "To new stage:"));

		var input = document.createElement("input");
		input.placeholder = "Name";
		input.value = "";
		input.pattern = ".+";
		d2.appendChild(input);

		var button = createElementWithTextNode("button", "Create & add");
		d2.appendChild(button);
		button.onclick = function () {
			if (input.value == "") {
				input.focus();
				return;
			}
			if (assets_browser.stages.includes(input.value)) {
				if (!confirm("Stage with this name exists, asset(s) will be added there. Proceed?"))
					return;
			}
			self.stage_selected(input.value);
		};

		d.appendChild(d2);

		if (assets_browser.stages.length > 0) {
			var d3 = document.createElement("div");
			d3.className = "existing_stages";

			d3.appendChild(createElementWithTextNode("p", "To existing stage:"));
			
			var d4 = document.createElement("div");
			d3.appendChild(d4);

			function make_stage_onclick(self, stage) {
				return function () {
					self.stage_selected(stage);
				}
			}

			for (var s of assets_browser.stages) {
				var sb = createElementWithTextNode("span", s);
				sb.onclick = make_stage_onclick(self, s);
				d4.appendChild(sb);
			}

			d.appendChild(d3);
		}

		this._show(e);
	},

	stage_selected: function (stage) {
		if (this.options.type == "directory")
			this.add_directory_to_stage(stage, this.options.locator);
		else if (this.options.type == "asset")
			this.add_asset_to_stage(stage, this.options.locator, this.variants_checkbox.checked);
		else
			this.add_list_to_stage(stage, this.options.list);
	},

	//

	render_list_adding: function (stage) {
		var e = document.getElementById("stage_selector");
		e.innerHTML = "";

		var d = document.createElement("div");
		e.appendChild(d);

		var p = createElementWithTextNode("p", "Adding " + this.list.length + " assets to '" + stage + "'...");
		d.appendChild(p);

		var p2 = createElementWithTextNode("p", "#" + this.list_index + ": " + get_basename(this.list[this.list_index-1].filename));
		d.appendChild(p2);

		// TODO: progress bar

		if (this.error != null) {
			var p3 = createElementWithTextNode("b", "Error: " + this.error);
			d.appendChild(p3);
		}
		
		// TODO: disable popup closing
		this._show();
	},

	//

	add_asset_to_stage: function (stage, locator, all_spans) {
		var self = this;
		ajax.postAndParseJson(
			"api/stages/add_asset", {
				stage: stage,
				locator: locator,
				all_spans: all_spans
			},
			function(r) {
				if (r.error) {
					// TODO: self.editor.search.error = r.message;
					return;
				}

				// TODO: self.editor.search.error = null;
				// TODO: open this asset in this stage?
				assets_browser.refresh_stages();
				self._hide();
			},
			function(e) {				
				// TODO: self.editor.search.error = e;
			}
		);
	},

	add_directory_to_stage: function (stage, path) {
		var self = this;
		ajax.postAndParseJson(
			"api/stages/add_directory", {
				stage: stage,
				path: path
			},
			function(r) {
				if (r.error) {
					// TODO: self.editor.search.error = r.message;
					return;
				}

				// TODO: self.editor.search.error = null;
				assets_browser._refresh_stages({stage: stage, path: path, update_search: true});
				self._hide();
			},
			function(e) {				
				// TODO: self.editor.search.error = e;
			}
		);
	},

	add_list_to_stage: function (stage, list) {
		this.list = list;
		this.list_index = 0;
		this.error = null;

		this.add_one_from_list_to_stage(stage);

		this.render_list_adding(stage);
	},

	add_one_from_list_to_stage: function (stage) {
		if (this.list_index >= this.list.length) {
			assets_browser.refresh_stages();
			this._hide();
			return;
		}

		var asset = this.list[this.list_index];
		this.list_index += 1;

		var self = this;
		ajax.postAndParseJson(
			"api/stages/add_asset", {
				stage: stage,
				locator: asset.locator,
				all_spans: true
			},
			function(r) {
				if (r.error) {
					self.error = r.message;
					return;
				}

				self.add_one_from_list_to_stage(stage);
			},
			function(e) {				
				self.error = e;
			}
		);

		this.render_list_adding(stage);
	},

	//

	_show: function (e) {
		e = e || document.getElementById("stage_selector");
		e.classList.add("open");
	},

	_hide: function (e) {
		e = e || document.getElementById("stage_selector");
		e.classList.remove("open");
	},

	_toggle: function () {
		var e = document.getElementById("stage_selector");
		e.classList.toggle("open");
	}
};

stage_selector.init();
