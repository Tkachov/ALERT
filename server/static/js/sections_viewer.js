sections_viewer = {
	ready: false,

	init: function () {
		this.ready = true;
	},

	//

	show_viewer: function (locator, shortname, fullname) {
		var self = this;
		ajax.postAndParseJson(
			"api/sections_viewer/make", {
				locator: locator
			},
			function(r) {
				if (r.error) {
					// TODO: self.editor.search.error = r.message;
					return;
				}

				// TODO: self.editor.search.error = null;
				self.make_window(locator, r.report, shortname, fullname);
			},
			function(e) {				
				// TODO: self.editor.search.error = e;
			}
		);
	},

	make_window: function (locator, report, shortname, fullname) {
		var title = fullname + " — Sections Viewer";
		var button_title = shortname + " — Sections Viewer";
		var e = windows.new_window(title, button_title);
		e.classList.add("sections_viewer");

		var d = document.createElement("div");
		e.appendChild(d);

		var h = document.createElement("div");
		h.className = "header";
		var sp = document.createElement("div");
		d.appendChild(h);
		sp.className = "content";
		d.appendChild(sp);

		var self = this;
		var oe = createElementWithTextNode("a", "Edit sections");
		oe.className = "editor_button";
		oe.onclick = function () { sections_editor.show_editor(locator, shortname, fullname); };
		h.appendChild(oe);

		// spoilers with reports by section

		function make_spoiler_onclick(s) {
			return function () {
				s.classList.toggle("open");
				if (s.classList.contains("open") && !isScrolledIntoView(s))
					s.scrollIntoView({behavior: "smooth", block: "start"});
			};
		}

		var sections_order = this._make_sections_order(report);

		var sections = {};
		if (report.strings.strings.length > 0) {
			var s = this._make_strings_block_spoiler(report);
			s.children[0].onclick = make_spoiler_onclick(s);
			sp.appendChild(s);
			sections["SB"] = s;
		}

		for (var sect of sections_order) {
			var k = "" + sect[0];
			var s = this._make_section_spoiler(report, sect);
			s.children[0].onclick = make_spoiler_onclick(s);
			sp.appendChild(s);
			sections[k] = s;
		}

		// header

		h.appendChild(createElementWithTextNode("b", report.header.length + " sections"));

		if (report.strings.strings.length > 0) {
			var x = this._make_header_strings_block_button();
			x.onclick = make_spoiler_onclick(sections["SB"]);
			h.appendChild(x);
		}
		
		for (var s of sections_order) {
			var x = this._make_header_section_button(report, s);
			x.onclick = make_spoiler_onclick(sections[s[0]]);
			h.appendChild(x);
		}
	},

	_make_sections_order: function (report) {
		var sections_order = [];
		for (var s of report.header) {
			sections_order.push([s[0], s[1], s[2]]);
		}
		sections_order.sort(function(a, b) {
			return a[1] - b[1];
		});
		return sections_order;
	},

	_make_strings_block_spoiler: function (report) {
		var s = document.createElement("div");
		s.className = "spoiler";
		var sh = document.createElement("div");
		var clr = document.createElement("span");
		clr.style.background = "#EEE";
		sh.appendChild(clr);
		sh.appendChild(createElementWithTextNode("span", "Strings block"));
		s.appendChild(sh);
		this.make_strings_block_content(s, report);
		return s;
	},

	_make_section_spoiler: function (report, sect) {
		var k = "" + sect[0];
		var tag = sect[0].toString(16).toUpperCase();
		var color = tag.substr(1, 6);

		var section = report.sections[k];

		var s = document.createElement("div");
		s.className = "spoiler";
		var sh = document.createElement("div");
		var clr = document.createElement("span");
		clr.style.background = "#" + color;
		sh.appendChild(clr);
		sh.appendChild(createElementWithTextNode("span", section.name));
		s.appendChild(sh);
		
		if (section.type == "text") {
			if (section.content != "") {
				var c = createElementWithTextNode("pre", section.content);
				s.appendChild(c);
			}

			// TODO: not readonly => editable text
		} else if (section.type == "json") {
			var c = createElementWithTextNode("pre", JSON.stringify(section.content, null, 4));
			s.appendChild(c);

			// TODO: not readonly => editable json
		} else if (section.type == "bytes") {
			var raw = atob(section.content);
			var contents = document.createElement("div");

			var t = document.createElement("table");
			t.className = "hex_view";

			var section_settings = {
				width: 16,
				absolute: true
			};
			if (controller.user.__hexview_experimental.enabled) {
				var settings = controller.user.__hexview_experimental;
				if (settings.sections.hasOwnProperty(tag)) {
					section_settings = settings.sections[tag];
				}

				var controls = document.createElement("div");
				controls.className = "hex_view_controls";

				var gr = document.createElement("span");
				gr.className = "hex_view_absolute";
				var cb_id = "hex_view_offset_absolute_" + tag +  "_" + Date.now();
				var cb = document.createElement("input");
				cb.type = "checkbox";
				cb.id = cb_id;
				cb.checked = (section_settings.absolute);

				var lb = createElementWithTextNode("label", "Absolute offset");
				lb.htmlFor = cb_id;
				gr.appendChild(cb);
				gr.appendChild(lb);
				controls.appendChild(gr);

				gr = document.createElement("span");
				gr.className = "hex_view_width";
				var nm_id = "hex_view_width_" + tag +  "_" + Date.now();
				var nm = document.createElement("input");
				nm.type = "number";
				nm.id = nm_id;
				nm.value = section_settings.width;

				lb = createElementWithTextNode("label", "Row width");
				lb.htmlFor = nm_id;
				gr.appendChild(lb);
				gr.appendChild(nm);
				controls.appendChild(gr);

				var btn = createElementWithTextNode("button", "Apply");
				btn.onclick = this.make_hexview_settings_onclick(tag, cb, nm, t, section);
				controls.appendChild(btn);

				gr = document.createElement("span");
				gr.className = "separator";
				controls.appendChild(gr);

				btn = createElementWithTextNode("button", "Copy hex");
				btn.onclick = this.make_hexview_copy_onclick(t);
				controls.appendChild(btn);
				
				contents.appendChild(controls);
			}
			
			this.make_hexview(t, raw, section_settings.width, section_settings.absolute ? section.offset : 0);
			contents.appendChild(t)
			s.appendChild(contents);

			// TODO: not readonly => hex editor
		}

		return s;
	},

	_make_header_strings_block_button: function () {
		var x = createElementWithTextNode("span", "Strings block");
		x.style.background = "#EEE";
		return x;
	},

	_make_header_section_button: function (report, s) {
		var tag = s[0].toString(16).toUpperCase();
		var x = createElementWithTextNode("span", report.sections[s[0]].name + " - " + s[2] + " bytes");

		var color = tag.substr(1, 6);
		x.style.background = "#" + color;
		x.style.color = (hexToLuma(color) < 0.6 ? "#FFF" : "#000");
		return x;
	},

	make_hexview_settings_onclick: function (tag, absolute_checkbox, width_number, t, section) {
		var self = this;
		return function () {
			var raw = atob(section.content);
			var settings = controller.user.__hexview_experimental;
			if (!settings.sections.hasOwnProperty(tag)) {
				settings.sections[tag] = {};
			}

			settings.sections[tag].width = parseInt(width_number.value);
			settings.sections[tag].absolute = absolute_checkbox.checked;
			controller.save_user();
			self.make_hexview(t, raw, settings.sections[tag].width, settings.sections[tag].absolute ? section.offset : 0);
		};
	},

	make_hexview_copy_onclick: function (t) {
		function copyToClip(plain) {
			function listener(e) {
				e.clipboardData.setData("text/plain", plain);
				e.preventDefault();
			}

			document.addEventListener("copy", listener);
			document.execCommand("copy");
			document.removeEventListener("copy", listener);
		}

		return function () {
			var hx = "";
			var qs = t.querySelectorAll("td:nth-child(2)");
			for (var q of qs) {
				hx += q.innerText + "\n";
			}
			copyToClip(hx);
		};
	},

	make_hexview: function (t, raw, viewer_width, offset) {
		function padhex(n, l) {
			var r = n.toString(16).toUpperCase();
			while (r.length < l) {
				r = "0" + r;
			}
			return r;
		}

		t.innerHTML = "";

		var thd = document.createElement("tr");
		var html = "<th></th><th>";
		for (var o = 0; o < viewer_width; ++o) {
			if (o > 0) html += " ";
			html += padhex(o % 16, 2);
		}				
		html += "</th><th></th>";
		thd.innerHTML = html;
		t.appendChild(thd);

		for (var o = 0; o < raw.length; o += viewer_width) {
			var trw = document.createElement("tr");
			trw.appendChild(createElementWithTextNode("td", padhex(offset + o, 8)));

			var hex_bytes = "";
			var ascii_bytes = "";
			for (var oj = 0; oj < viewer_width; ++oj) {
				if (o + oj >= raw.length) break;
				if (oj > 0) hex_bytes += " ";
				var bt = raw.charCodeAt(o + oj);
				hex_bytes += padhex(bt, 2);
				if (bt >= 32 && bt < 128)
					ascii_bytes += String.fromCharCode(bt);
				else
					ascii_bytes += '.';
			}

			trw.appendChild(createElementWithTextNode("td", hex_bytes));
			trw.appendChild(createElementWithTextNode("td", ascii_bytes));

			t.appendChild(trw);
		}
	},

	make_strings_block_content: function (container, report) {
		var contents = document.createElement("div");

		var t = document.createElement("table");
		t.className = "strings_block";

		// controls
		var format_settings = {
			prefix: false,
			header: true,
			base: 10,
			pad: 0,
			little_endian: false
		};

		var settings = controller.user;
		if (settings.hasOwnProperty("__sb_overrides")) {
			format_settings = settings["__sb_overrides"];
		}

		// TODO: controls
		/*
		var controls = document.createElement("div");
		controls.className = "hex_view_controls";

		var gr = document.createElement("span");
		gr.className = "hex_view_absolute";
		var cb_id = "hex_view_offset_absolute_" + tag +  "_" + Date.now();
		var cb = document.createElement("input");
		cb.type = "checkbox";
		cb.id = cb_id;
		cb.checked = (section_settings.absolute);

		var lb = createElementWithTextNode("label", "Absolute offset");
		lb.htmlFor = cb_id;
		gr.appendChild(cb);
		gr.appendChild(lb);
		controls.appendChild(gr);

		gr = document.createElement("span");
		gr.className = "hex_view_width";
		var nm_id = "hex_view_width_" + tag +  "_" + Date.now();
		var nm = document.createElement("input");
		nm.type = "number";
		nm.id = nm_id;
		nm.value = section_settings.width;

		lb = createElementWithTextNode("label", "Base");
		lb.htmlFor = nm_id;
		gr.appendChild(lb);
		gr.appendChild(nm);
		controls.appendChild(gr);

		var btn = createElementWithTextNode("button", "Apply");
		btn.onclick = this.make_hexview_settings_onclick(tag, cb, nm, t, section);
		controls.appendChild(btn);

		gr = document.createElement("span");
		gr.className = "separator";
		controls.appendChild(gr);
		
		contents.appendChild(controls);
		*/

		function format_offset(offset, format_settings, report) {
			if (format_settings.prefix) offset += report.strings.prefix;
			if (format_settings.header) offset += report.strings.offset;

			if (format_settings.little_endian) {
				var s = offset.toString(16).toUpperCase();
				if (s.length % 2 == 1) s = "0" + s;

				var result = "";
				for (var i=0; i<s.length; i += 2) {
					result = s[i] + s[i+1] + " " + result;
				}
				return result;
			}

			var result = "" + offset;
			if (format_settings.base != 10) {
				result = offset.toString(format_settings.base).toUpperCase();
			}

			if (format_settings.pad > result.length) {
				while (result.length < format_settings.pad) {
					result = "0" + result;
				}
			}

			return result;
		}
		
		// strings
		t.innerHTML = "";

		var thd = document.createElement("tr");
		var html = "<th>#</th><th>offset</th><th>value</th>";
		thd.innerHTML = html;
		t.appendChild(thd);

		for (var i = 0; i < report.strings.strings.length; ++i) {
			var s = report.strings.strings[i];
			var offset = format_offset(s[0], format_settings, report);

			var trw = document.createElement("tr");
			trw.appendChild(createElementWithTextNode("td", i));
			trw.appendChild(createElementWithTextNode("td", offset));
			trw.appendChild(createElementWithTextNode("td", s[1]));
			t.appendChild(trw);
		}

		contents.appendChild(t);
		container.appendChild(contents);
	}
};

sections_viewer.init();
