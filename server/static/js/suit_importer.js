// ALERT: Amazing Luna Engine Research Tools
// This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
// For more details, terms and conditions, see GNU General Public License.
// A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

suit_importer = {
	ready: false,

	form_dom: null,
	sending: false,
	error: null,

	init: function () {
		this.ready = true;
		this.render();
	},

	show_importer: function () {
		this.form_dom = null;
		this.sending = false;
		this.error = null;
		this.render();
		this._show();
	},

	//

	render: function () {
		var closable = (!this.sending);
		var self = this;

		var e = document.getElementById("suit_importer");
		e.innerHTML = "";
		if (closable)
			e.onclick = function (ev) { if (ev.target == e) e.classList.remove("open"); };
		else
			e.onclick = function () {};

		//

		var d = document.createElement("div");
		e.appendChild(d);

		if (this.form_dom == null) {
			var f = document.createElement("div");
			f.className = "import_form";
			this.form_dom = f;

			var h = createElementWithTextNode("b", "Import .suit into stage");
			f.appendChild(h);
			
			var file_input = document.createElement("input");
			file_input.type = "file";
			file_input.name = "suit";
			f.appendChild(file_input);

			var stage_input = document.createElement("input");
			stage_input.type = "text";
			stage_input.name = "stage";
			stage_input.placeholder = "Stage to import into";
			stage_input.value = "";
			stage_input.pattern = ".+";
			f.appendChild(stage_input);

			var stage_autocomplete = document.createElement("datalist");
			stage_autocomplete.id = "suit_importer_stage_autocomplete";
			f.appendChild(stage_autocomplete);

			stage_input.setAttribute('list', stage_autocomplete.id);

			file_input.onchange = function () {
				if (stage_input.value == "" && file_input.files.length > 0)
					stage_input.value = file_input.files[0].name.replace(".suit", "");
			};

			var b = createElementWithTextNode("button", "Import");
			f.appendChild(b);
			b.onclick = function () {
				if (file_input.files.length < 1) {
					file_input.focus();
					self.error = "Select a file to import!";
					self.render();
					return;
				}

				if (stage_input.value == "") {
					stage_input.focus();
					self.error = "Specify a stage to import into!";
					self.render();
					return;
				}
				if (assets_browser.stages.includes(stage_input.value)) {
					if (!confirm("Stage with this name exists, asset(s) will be added there. Proceed?"))
						return;
				}

				self.import_suit(file_input, stage_input.value);
			};
		}

		//

		var form_disabled = (this.sending);

		var input = this.get_file_input();
		if (input != null) input.disabled = form_disabled;

		input = this.get_stage_input();
		if (input != null) input.disabled = form_disabled;

		input = this.get_submit_button();
		if (input != null) input.disabled = form_disabled;

		//

		var stage_autocomplete = this.get_stage_autocomplete();
		if (stage_autocomplete != null) {
			stage_autocomplete.innerHTML = "";

			if (assets_browser.stages.length > 0) {
				for (var s of assets_browser.stages) {
					var op = document.createElement("option");
					op.value = s;
					stage_autocomplete.appendChild(op);
				}
			}
		}

		//

		d.appendChild(this.form_dom);

		if (this.error != null) {
			d.appendChild(createElementWithTextNode("b", "Error: " + this.error));
		}
	},

	import_suit: function (file_input, stage) {
		this.sending = true;

		var form_data = new FormData();
		form_data.set(file_input.name, file_input.files[0]);
		form_data.set("stage", stage);

		var self = this;
		ajax.postFormAndParseJson(
			"api/stages/import_suit", form_data,
			function(r) {
				self.sending = false;

				if (r.error) {
					self.error = r.message;
					self.render();
					return;
				}

				self.error = null;
				assets_browser._refresh_stages({stage: stage, path: "", update_search: true});
				self._hide();
			},
			function(e) {				
				self.sending = false;
				self.error = e;
				self.render();
			}
		);

		this.render();
	},

	//

	get_file_input: function () {
		if (this.form_dom == null) return null;
		return this.form_dom.querySelector("input[type=\"file\"]");
	},

	get_stage_input: function () {
		if (this.form_dom == null) return null;
		return this.form_dom.querySelector("input[type=\"text\"]");
	},

	get_stage_autocomplete: function () {
		if (this.form_dom == null) return null;
		return this.form_dom.querySelector("datalist");
	},

	get_submit_button: function () {
		if (this.form_dom == null) return null;
		return this.form_dom.querySelector("button");
	},

	//

	_show: function (e) {
		e = e || document.getElementById("suit_importer");
		e.classList.add("open");
	},

	_hide: function (e) {
		e = e || document.getElementById("suit_importer");
		e.classList.remove("open");
	},

	_toggle: function () {
		var e = document.getElementById("suit_importer");
		e.classList.toggle("open");
	}
};

suit_importer.init();
