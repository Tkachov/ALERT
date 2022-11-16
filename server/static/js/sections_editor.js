sections_editor = {
	ready: false,

	init: function () {
		this.ready = true;
	},

	construct_editor: function () {
		return {
			locator: null,
			info: null,
			edited: null,
			container: null,

			init: function (locator, info, shortname, fullname) {
				this.locator = locator;
				this.info = info;
				this.edited = null;

				var title = fullname + " — Sections Editor";
				var button_title = shortname + " — Sections Editor";
				var e = windows.new_window(title, button_title);
				e.classList.add("sections_editor");
				this.container = e;

				this.render();
			},

			render: function () {
				var self = this;
				if (this.edited == null) {
					var edited = {
						header: {
							magic: this.info.header.magic,
							size: this.info.header.size,
							recalculate_size: true,
							rest: []
						},
						strings: {
							option_index: 0,
							appended: "",
							dom: null
						},
						sections: []
					};

					for (var r of this.info.header.rest) {
						edited.header.rest.push(r);
					}

					for (var section of this.info.sections) {
						edited.sections.push({tag: section.tag, type: section.type, option_index: 0, dom: null});
					}

					this.edited = edited;
				}

				//
				
				var e = this.container;
				e.innerHTML = "";

				var d = document.createElement("div");
				e.appendChild(d);

				var original = document.createElement("div");
				original.className = "original";
				d.appendChild(original);

				var h = document.createElement("div");
				h.className = "header";
				original.appendChild(h);

				h.appendChild(createElementWithTextNode("b", "Original asset header"));
				h.appendChild(document.createElement("br"));

				var input = document.createElement("input");
				input.type = "number";
				input.value = this.info.header.magic;
				input.disabled = true;
				h.appendChild(input);

				input = document.createElement("input");
				input.type = "number";
				input.value = this.info.header.size;
				input.disabled = true;
				h.appendChild(input);

				h.appendChild(document.createElement("br"));

				for (var r of this.info.header.rest) {
					input = document.createElement("input");
					input.type = "number";
					input.value = r;
					input.disabled = true;
					h.appendChild(input);
				}

				var s = document.createElement("div");
				s.className = "section";

				var clr = document.createElement("span");
				clr.style.background = "#EEE";
				s.appendChild(clr);
				s.appendChild(createElementWithTextNode("span", "Strings block (" + this.info.strings.count + " strings/" + this.info.strings.size + " bytes)"));
				
				var a = createElementWithTextNode("a", "Save raw");
				a.href = "/api/sections_editor/strings?locator=" + this.locator;
				a.target = "_blank";
				s.appendChild(a);
				original.appendChild(s);

				for (var section of this.info.sections) {
					var tag = section.tag.toString(16).toUpperCase();
					var color = tag.substr(1, 6);

					s = document.createElement("div");
					s.className = "section";

					clr = document.createElement("span");
					clr.style.background = "#" + color;
					s.appendChild(clr);
					s.appendChild(createElementWithTextNode("span", tag + " (" + section.size + " bytes)"));
					
					a = createElementWithTextNode("a", "Save raw");
					a.href = "/api/sections_editor/section?locator=" + this.locator + "&section=" + section.tag;
					a.target = "_blank";
					s.appendChild(a);
					original.appendChild(s);
				}

				a = createElementWithTextNode("a", "Save original as...");
				a.className = "bottom_button";
				a.href = "/api/assets/asset?locator=" + this.locator;
				a.target = "_blank";
				original.appendChild(a);

				//

				var edited = document.createElement("div");
				edited.className = "edited";
				d.appendChild(edited);

				h = document.createElement("div");
				h.className = "header";
				edited.appendChild(h);

				h.appendChild(createElementWithTextNode("b", "Edited asset header"));
				h.appendChild(document.createElement("br"));

				var input = document.createElement("input");
				input.type = "number";
				input.value = this.edited.header.magic;
				input.disabled = true;
				h.appendChild(input);

				input = document.createElement("input");
				input.type = "number";
				input.value = this.edited.header.size;
				input.disabled = this.edited.header.recalculate_size;
				h.appendChild(input);

				var size_input = input;
				size_input.onchange = function () { self.edited.header.size = size_input.value; }

				var cb_id = "recalculate_size_" + Date.now();

				input = document.createElement("input");
				input.type = "checkbox";
				input.name = "recalculate_size";
				input.id = cb_id;
				input.checked = this.edited.header.recalculate_size;
				h.appendChild(input);

				var size_checkbox = input;
				size_checkbox.onchange = function () {
					self.edited.header.recalculate_size = size_checkbox.checked;
					size_input.disabled = self.edited.header.recalculate_size;
				}

				var label = createElementWithTextNode("label", "Put final size in this field automatically");
				label.htmlFor = cb_id;
				h.appendChild(label);

				h.appendChild(document.createElement("br"));

				function make_rest_input_onchange(self, input, index) {
					return function () { self.edited.header.rest[index] = input.value; };
				}

				for (var i=0; i<this.edited.header.rest.length; ++i) {
					input = document.createElement("input");
					input.type = "number";
					input.value = this.edited.header.rest[i];
					h.appendChild(input);
					input.onchange = make_rest_input_onchange(this, input, i);
				}

				function make_option(text, value) {
					var o = createElementWithTextNode("option", text);
					o.value = value;
					return o;
				}

				function make_file_upload(name) {
					var input = document.createElement("input");
					input.type = "file";
					input.name = name;
					return input;			
				}

				const STRINGS_OPTION_KEEP = "keep";
				const STRINGS_OPTION_REPLACE = "replace";
				const STRINGS_OPTION_APPEND = "append";

				if (this.edited.strings.dom == null) {
					s = document.createElement("div");
					s.className = "section";
					this.edited.strings.dom = s;

					clr = document.createElement("span");
					clr.style.background = "#EEE";
					s.appendChild(clr);
					s.appendChild(createElementWithTextNode("span", "Strings block"));

					var arrd = document.createElement("span");
					arrd.className = "arrows";
					s.appendChild(arrd);

					select = document.createElement("select");
					select.appendChild(make_option("Keep as is", STRINGS_OPTION_KEEP));
					select.appendChild(make_option("Replace raw", STRINGS_OPTION_REPLACE));
					select.appendChild(make_option("Add strings", STRINGS_OPTION_APPEND));
					select.selectedIndex = this.edited.strings.option_index;
					s.appendChild(select);

					var strings_select = select;
					strings_select.onchange = function () {
						self.edited.strings.option_index = strings_select.selectedIndex;
						self.edited.strings.dom = null;
						self.render();
					}

					switch (strings_select.options[strings_select.selectedIndex].value) {
						case STRINGS_OPTION_KEEP: s.classList.add("closed"); break;
						case STRINGS_OPTION_REPLACE:
							s.appendChild(document.createElement("br"));
							s.appendChild(make_file_upload("strings"));
						break;
						case STRINGS_OPTION_APPEND:
							s.appendChild(document.createElement("br"));
							var ta = createElementWithTextNode("textarea", this.edited.strings.appended);
							ta.onchange = function () { self.edited.strings.appended = ta.value; }
							s.appendChild(ta);
						break;
					}

					edited.appendChild(s);
				}

				edited.appendChild(this.edited.strings.dom);

				const TYPE_OPTIONS = {
					"raw": ["keep", "replace"]
				};

				function get_section_by_tag(sections, tag) {
					for (var s of sections) {
						if (s.tag == tag) return s;
					}
					return null;
				}

				function make_section_option_select(self, select, tag) {
					return function () {
						var sct = get_section_by_tag(self.edited.sections, tag);
						sct.option_index = select.selectedIndex;
						sct.dom = null;
						self.render();
					};
				}

				function make_section_arrow_swap(self, tag, offset) {
					return function () {
						var target = -1;
						for (var i=0; i<self.edited.sections.length; ++i) {
							if (self.edited.sections[i].tag == tag) {
								target = i;
								break;
							}
						}

						if (target == -1 || target+offset < 0 || target+offset >= self.edited.sections.length) return;

						var a = self.edited.sections[i];
						var b = self.edited.sections[i+offset];
						self.edited.sections[i] = b;
						self.edited.sections[i+offset] = a;
						self.render();
					};
				}

				for (var section of this.edited.sections) {
					if (section.dom == null) {
						var tag = section.tag.toString(16).toUpperCase();
						var color = tag.substr(1, 6);

						s = document.createElement("div");
						s.className = "section";
						section.dom = s;

						clr = document.createElement("span");
						clr.style.background = "#" + color;
						s.appendChild(clr);
						s.appendChild(createElementWithTextNode("span", tag));

						var arrd = document.createElement("span");
						arrd.className = "arrows";
						s.appendChild(arrd);

						var arrup = createElementWithTextNode("a", "↑");
						arrup.onclick = make_section_arrow_swap(this, section.tag, -1);
						arrd.appendChild(arrup);

						var arrdown = createElementWithTextNode("a", "↓");
						arrdown.onclick = make_section_arrow_swap(this, section.tag, 1);
						arrd.appendChild(arrdown);

						var available_options = TYPE_OPTIONS[section.type];

						select = document.createElement("select");
						for (var op of available_options)
							select.appendChild(make_option(controller.get_localized("ui/editor/sections_editor/section_edit_option_" + op), op));
						select.selectedIndex = section.option_index;
						s.appendChild(select);
						select.onchange = make_section_option_select(this, select, section.tag);

						switch (select.options[select.selectedIndex].value) {
							case "keep": s.classList.add("closed"); break;
							case "replace":
								s.appendChild(document.createElement("br"));
								s.appendChild(make_file_upload(tag));
							break;
						}

						edited.appendChild(s);
					}

					edited.appendChild(section.dom);
				}

				a = createElementWithTextNode("a", "Save edited as...");
				a.className = "bottom_button";
				a.onclick = function () { self.edit_asset(); }
				edited.appendChild(a);
			},

			//

			edit_asset: function () {
				var form_data = new FormData();
				form_data.set("locator", this.locator);
				form_data.set("header", JSON.stringify(this.edited.header));

				var strings_dom = this.edited.strings.dom;
				var strings_select = strings_dom.querySelector("select");
				var strings_option = strings_select.options[strings_select.selectedIndex].value;
				var strings_data = {"option": strings_option};
				if (strings_option == "append")
					strings_data["appended"] = this.edited.strings.appended;
				form_data.set("strings", JSON.stringify(strings_data));
				if (strings_option == "replace")
					form_data.set("strings_raw", strings_dom.querySelector("input[type=\"file\"]").files[0]);

				var sections_data = [];
				for (var s of this.edited.sections) {
					var section_select = s.dom.querySelector("select");
					var section_option = section_select.options[section_select.selectedIndex].value;
					sections_data.push({"tag": s.tag, "option": section_option});
					if (section_option == "replace") {
						var f = s.dom.querySelector("input[type=\"file\"]");
						form_data.set(f.name + "_raw", f.files[0]);
					}
				}
				form_data.set("sections", JSON.stringify(sections_data));

				var self = this;
				ajax.postFormAndParseJson(
					"api/sections_editor/edit_asset", form_data,
					function(r) {
						if (r.error) {
							// TODO: self.editor.search.error = r.message;
							return;
						}

						// TODO: self.editor.search.error = null;
						var a = document.createElement("a");
						a.href = "/api/sections_editor/edited_asset";
						a.target = "_blank";
						a.click();
					},
					function(e) {				
						// TODO: self.editor.search.error = e;
					}
				);
			}
		};
	},

	show_editor: function (locator, shortname, fullname) {
		var self = this;
		ajax.postAndParseJson(
			"api/sections_editor/make", {
				locator: locator
			},
			function(r) {
				if (r.error) {
					// TODO: self.editor.search.error = r.message;
					return;
				}

				// TODO: self.editor.search.error = null;
				var e = self.construct_editor();
				e.init(locator, r.report, shortname, fullname);
			},
			function(e) {				
				// TODO: self.editor.search.error = e;
			}
		);
	}
};

sections_editor.init();
