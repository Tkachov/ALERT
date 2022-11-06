sections_viewer = {
	ready: false,

	init: function () {
		this.ready = true;
	},

	//

	show_viewer: function (index, shortname, fullname) {
		var self = this;
		ajax.postAndParseJson(
			"api/sections_viewer/make", {
				index: index
			},
			function(r) {
				if (r.error) {
					// TODO: self.editor.search.error = r.message;
					return;
				}

				// TODO: self.editor.search.error = null;
				self.make_window(index, r.report, shortname, fullname);
			},
			function(e) {				
				// TODO: self.editor.search.error = e;
			}
		);
	},

	make_window: function (index, report, shortname, fullname) {
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
		oe.onclick = function () { sections_editor.show_editor(index, shortname, fullname); };
		h.appendChild(oe);

		// spoilers with reports by section

		function make_spoiler_onclick(s) {
			return function () { s.classList.toggle("open"); };
		}

		var sections_order = [];
		for (var s of report.header) {
			sections_order.push([s[0], s[1], s[2]]);
		}
		sections_order.sort(function(a, b) {
			return a[1] - b[1];
		});

		var sections = {};
		if (report.strings.length > 0) {
			var s = document.createElement("div");
			s.className = "spoiler";
			var sh = document.createElement("div");
			var clr = document.createElement("span");
			clr.style.background = "#EEE";
			sh.appendChild(clr);
			sh.appendChild(createElementWithTextNode("span", "Strings block"));
			s.appendChild(sh);
			sh.onclick = make_spoiler_onclick(s);
			var c = createElementWithTextNode("pre", report.strings);
			s.appendChild(c);
			sp.appendChild(s);
			sections["SB"] = s;
		}

		for (var sect of sections_order) {
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
			sh.onclick = make_spoiler_onclick(s);
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

				var t = document.createElement("table");
				t.className = "hex_view";
				var thd = document.createElement("tr");
				thd.innerHTML = "<th></th><th>00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F</th><th></th>";
				t.appendChild(thd);

				function padhex(n, l) {
					var r = n.toString(16).toUpperCase();
					while (r.length < l) {
						r = "0" + r;
					}
					return r;
				}

				for (var o = 0; o < raw.length; o += 16) {
					var trw = document.createElement("tr");
					trw.appendChild(createElementWithTextNode("td", padhex(o, 8)));

					var hex_bytes = "";
					var ascii_bytes = "";
					for (var oj = 0; oj < 16; ++oj) {
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
				
				s.appendChild(t);

				// TODO: not readonly => hex editor
			}
			sp.appendChild(s);
			sections[k] = s;
		}

		// header

		h.appendChild(createElementWithTextNode("b", report.header.length + " sections"));

		if (report.strings.length > 0) {
			var x = createElementWithTextNode("span", "Strings block");
			x.style.background = "#EEE";
			x.onclick = make_spoiler_onclick(sections["SB"]);
			h.appendChild(x);
		}
		
		for (var s of sections_order) {
			var tag = s[0].toString(16).toUpperCase();
			var x = createElementWithTextNode("span", report.sections[s[0]].name + " - " + s[2] + " bytes");

			var color = tag.substr(1, 6);
			x.style.background = "#" + color;
			x.style.color = (hexToLuma(color) < 0.6 ? "#FFF" : "#000");
			x.onclick = make_spoiler_onclick(sections[s[0]]);
			h.appendChild(x);
		}
	}
};

sections_viewer.init();
