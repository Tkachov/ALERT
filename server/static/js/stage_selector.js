stage_selector = {
	ready: false,

	init: function () {
		this.ready = true;

		var e = document.getElementById("stage_selector");
		e.onclick = function (ev) { if (ev.target == e) e.classList.remove("open"); };
	},

	//

	show_selector: function (locator, shortname, fullname, is_directory) {
		var self = this;
		var e = document.getElementById("stage_selector");
		e.innerHTML = "";

		var d = document.createElement("div");
		e.appendChild(d);

		var p = createElementWithTextNode("p", "Adding " + fullname + " to stage...");
		d.appendChild(p);

		// TODO: don't show checkbox if no variants exist
		var cb;
		if (!is_directory) {
			var cb_id = "all_spans";

			cb = document.createElement("input");
			cb.type = "checkbox";
			cb.name = "display_suits";
			cb.id = cb_id;
			cb.checked = true;

			var lb = createElementWithTextNode("label", "Add asset's variants from all spans"); // TODO: count of variants
			lb.htmlFor = cb_id;

			var p = document.createElement("p");
			p.className = "checkbox_line";
			p.appendChild(cb);
			p.appendChild(lb);
			d.appendChild(p);
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
			self.add_asset_to_stage(input.value, locator, cb.checked);
		};

		d.appendChild(d2);

		if (assets_browser.stages.length > 0) {
			var d3 = document.createElement("div");
			d3.className = "existing_stages";

			d3.appendChild(createElementWithTextNode("p", "To existing stage:"));
			
			var d4 = document.createElement("div");
			d3.appendChild(d4);

			function make_stage_onclick(self, stage, locator, cb) {
				return function () {
					self.add_asset_to_stage(stage, locator, cb.checked);
				}
			}

			for (var s of assets_browser.stages) {
				var sb = createElementWithTextNode("span", s);
				sb.onclick = make_stage_onclick(self, s, locator, cb);
				d4.appendChild(sb);
			}

			d.appendChild(d3);
		}

		this._show(e);
	},

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
		// TODO
		// TODO: open this directory in this stage?
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
