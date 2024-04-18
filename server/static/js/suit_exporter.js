// ALERT: Amazing Luna Engine Research Tools
// This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
// For more details, terms and conditions, see GNU General Public License.
// A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

suit_exporter = {
	ready: false,

	stage: null,
	info: null,

	form_dom: null,
	sending: false,
	error: null,

	init: function () {
		this.ready = true;
		this.render();
	},

	show_exporter: function (stage) {
		this.stage = stage;
		this.info = null;

		this.form_dom = null;
		this.sending = true;
		this.error = null;

		var self = this;
		ajax.postAndParseJson(
			"api/stages/make_export_suit", {"stage": stage},
			function(r) {
				self.sending = false;

				if (r.error) {
					self.error = r.message;
					self.render();
					return;
				}

				self.error = null;
				self.prepare_info(stage, r);
				self.render();
			},
			function(e) {
				self.sending = false;
				self.error = e;
				self.render();
			}
		);

		this.render();
		this._show();
	},

	//

	prepare_info: function (stage, info) {
		this.stage = stage;
		this.info = info;

		const TARGETS = [[360, 260], [256, 204], [404, 160]]; // MSMR, MM thumb, MM chest
		this.info.textures.sort((a, b) => {
			var aw = a.width;
			var ah = a.height;
			var bw = b.width;
			var bh = b.height;

			// full match

			var at = -1;
			var bt = -1;

			for (var i=0; i<TARGETS.length; ++i) {
				var tw = TARGETS[i][0];
				var th = TARGETS[i][1];

				if (aw == tw && ah == th) at = i;
				if (bw == tw && bh == th) bt = i;
			}

			if (at == -1 || bt == -1) {
				if (at == bt) {
					// continue with other checks
				} else {
					return (at == -1 ? 1 : -1); // first goes the one that matched
				}
			} else {
				return (bt - at); // first goes the one that matches earlier target
			}

			// aspect ratio match

			var aar = (ah != 0 ? aw/ah : 1);
			var bar = (bh != 0 ? bw/bh : 1);
			at = -1;
			bt = -1;

			function float_equal(x, y) {
				var precision = 0.001;
				return (Math.abs(x - y) <= precision);
			}

			for (var i=0; i<TARGETS.length; ++i) {
				var tw = TARGETS[i][0];
				var th = TARGETS[i][1];
				var tar = (th != 0 ? tw/th : 1);

				if (float_equal(aar, tar)) at = i;
				if (float_equal(bar, tar)) bt = i;
			}

			if (at == -1 || bt == -1) {
				if (at == bt) {
					// continue with other checks
				} else {
					return (at == -1 ? 1 : -1); // first goes the one that matched
				}
			} else {
				return (bt - at); // first goes the one that matches earlier target
			}

			// area match

			var aa = aw*ah;
			var ba = bw*bh;
			at = -1;
			bt = -1;

			for (var i=0; i<TARGETS.length; ++i) {
				var tw = TARGETS[i][0];
				var th = TARGETS[i][1];
				var ta = tw*th;

				if (aa == ta) at = i;
				if (ba == ta) bt = i;
			}

			if (at == -1 || bt == -1) {
				if (at == bt) {
					// continue with other checks
				} else {
					return (at == -1 ? 1 : -1); // first goes the one that matched
				}
			} else {
				return (bt - at); // first goes the one that matches earlier target
			}

			// if no matches, generic filename sort

			return a.locator.localeCompare(b.locator);
		});
	},

	//

	render: function () {
		var closable = (!this.sending);
		var self = this;

		var e = document.getElementById("suit_exporter");
		e.innerHTML = "";
		if (closable)
			e.onclick = function (ev) { if (ev.target == e) e.classList.remove("open"); };
		else
			e.onclick = function () {};

		//

		var d = document.createElement("div");
		e.appendChild(d);

		var h = document.createElement("b");
		h.appendChild(document.createTextNode("Exporting as .suit:"));
		h.appendChild(document.createElement("br"));
		h.appendChild(document.createTextNode(this.stage));
		d.appendChild(h);

		if (this.info == null) {
			if (this.sending) {
				d.appendChild(createElementWithTextNodeAndClass("span", "loading", "Scanning staged files..."));
				return;
			}

			if (this.error != null) {
				d.appendChild(createElementWithTextNodeAndClass("b", "error", "Error: " + this.error));
			}

			return;
		}

		if (this.form_dom == null) {
			var f = document.createElement("div");
			f.className = "export_form";
			this.form_dom = f;

			//

			var suit_id = document.createElement("input");
			suit_id.type = "text";
			suit_id.name = "suit_id";
			suit_id.placeholder = "Unique internal ID";
			suit_id.value = "";
			suit_id.pattern = ".+";
			suit_id.required = true;
			f.appendChild(suit_id);

			var suit_name = document.createElement("input");
			suit_name.type = "text";
			suit_name.name = "suit_name";
			suit_name.placeholder = "In-game name (optional)";
			suit_name.value = "";
			f.appendChild(suit_name);

			//

			function create_option(text, value) {
				var o = createElementWithTextNode("option", text);
				o.value = value;
				return o;
			}

			//			

			f.appendChild(createElementWithTextNode("label", "Target game:"));
			
			var game_format = document.createElement("select");
			game_format.name = "game";
			game_format.required = true;
			game_format.appendChild(create_option("Spider-Man PC", "msmr"));
			game_format.appendChild(create_option("Miles Morales PC", "mm"));
			game_format.onchange = function () { self.render(); };
			f.appendChild(game_format);

			//

			function get_basename(path) {
				var i1 = path.lastIndexOf('/');
				var i2 = path.lastIndexOf('\\');
				return path.substr(Math.max(i1, i2) + 1);
			}

			f.appendChild(createElementWithTextNode("label", "Suit .model:"));
			
			var suit_model = document.createElement("select");
			suit_model.name = "model";
			suit_model.required = true;
			suit_model.size = 5;
			for (var m of this.info.models) {
				var bn = get_basename(m.locator);
				var o = createElementWithTextNode("option", bn + " (" + m.details + ")");
				o.value = m.locator;
				suit_model.appendChild(o);
			}
			f.appendChild(suit_model);

			//

			function make_icon_select(f, textures, label, title, name, format) {
				var l = createElementWithTextNode("label", label);
				l.title = title;
				l.dataset.game_format = format;
				f.appendChild(l);
			
				var suit_icon = document.createElement("select");
				suit_icon.name = name;
				suit_icon.size = 5;
				for (var t of textures) {
					var bn = get_basename(t.locator);
					var o = createElementWithTextNode("option", bn + " (" + t.width + " × " + t.height + ")");
					o.value = t.locator;
					suit_icon.appendChild(o);
				}
				suit_icon.dataset.game_format = format;
				f.appendChild(suit_icon);
			}

			make_icon_select(f, this.info.textures, "Suit icon (optional):", "Typically 360 × 260", "msmr_icon", "msmr");
			make_icon_select(f, this.info.textures, "Suit thumbnail (optional):", "Typically 256 × 204", "mm_thumb_icon", "mm");
			make_icon_select(f, this.info.textures, "Suit chest icon (optional):", "Typically 404 × 160", "mm_chest_icon", "mm");

			var b = createElementWithTextNode("button", "Export");
			f.appendChild(b);
			b.onclick = function () {
				if (suit_id.value == "") {
					suit_id.focus();
					self.error = "Specify the suit ID!";
					self.render();
					return;
				}

				if (suit_model.value == "") {
					suit_model.focus();
					self.error = "Select a model!";
					self.render();
					return;
				}

				self.export_suit();
			};
		}

		//

		var input = this.get_game_format_input();
		var selected_game_format = (input == null ? null : input.value);
		var form_disabled = (this.sending);

		for (var c of this.form_dom.children) {
			if (c.dataset.hasOwnProperty("game_format")) {
				classListSetIf(c, "hidden", c.dataset.game_format != selected_game_format);
			}

			if (c.tagName == "SELECT" || c.tagName == "INPUT" || c.tagName == "BUTTON") {
				c.disabled = form_disabled;
			}
		}

		//

		d.appendChild(this.form_dom);

		if (this.error != null) {
			d.appendChild(createElementWithTextNodeAndClass("b", "error", "Error: " + this.error));
		}
	},

	export_suit: function () {
		this.sending = true;
		this.error = null;

		var form_data = new FormData();
		form_data.set("stage", this.stage);
		for (var c of this.form_dom.children) {
			if (c.tagName == "SELECT" || c.tagName == "INPUT") {
				form_data.set(c.name, c.value);
			}
		}

		var self = this;
		ajax.postFormAndParseJson(
			"api/stages/export_suit", form_data,
			function(r) {
				self.sending = false;

				if (r.error) {
					self.error = r.message;
					self.render();
					return;
				}

				self.error = null;

				var a = document.createElement("a");
				a.href = "/api/stages/exported_suit?filename=" + r.download;
				a.target = "_blank";
				a.click();

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

	get_game_format_input: function () {
		if (this.form_dom == null) return null;
		return this.form_dom.querySelector("select[name=\"game\"]");
	},

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
		e = e || document.getElementById("suit_exporter");
		e.classList.add("open");
	},

	_hide: function (e) {
		e = e || document.getElementById("suit_exporter");
		e.classList.remove("open");
	},

	_toggle: function () {
		var e = document.getElementById("suit_exporter");
		e.classList.toggle("open");
	}
};

suit_exporter.init();
