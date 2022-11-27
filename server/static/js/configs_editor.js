configs_editor = {
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

				var title = fullname + " — Configs Editor";
				var button_title = shortname + " — Configs Editor";
				var e = windows.new_window(title, button_title);
				e.classList.add("configs_editor");
				this.container = e;

				this.render();
			},

			render: function () {
				var e = this.container;
				e.innerHTML = "";

				var d = document.createElement("div");
				e.appendChild(d);

				make_json_editor(d, this.info["content"]);
			}
		};
	},

	show_editor: function (locator, shortname, fullname) {
		var self = this;
		ajax.postAndParseJson(
			"api/configs_editor/make", {
				locator: locator
			},
			function(r) {
				if (r.error) {
					// TODO: self.editor.search.error = r.message;
					return;
				}

				// TODO: self.editor.search.error = null;
				var e = self.construct_editor();
				e.init(locator, r, shortname, fullname);
			},
			function(e) {				
				// TODO: self.editor.search.error = e;
			}
		);
	}
};

configs_editor.init();

const NT_ARRAY			= -1;
const NT_UINT8 			= 0x00;
const NT_UINT16 		= 0x01;
const NT_UINT32 		= 0x02;
const NT_INT8 			= 0x04;
const NT_INT16 			= 0x05;
const NT_INT32 			= 0x06;
const NT_FLOAT 			= 0x08;
const NT_STRING 		= 0x0A;
const NT_OBJECT 		= 0x0D;
const NT_BOOLEAN 		= 0x0F;
const NT_INSTANCE_ID 	= 0x11;
const NT_NULL 			= 0x13;

var options_select_html = "";
{
	function make_option(v, t) {
		var o = createElementWithTextNode("option", t);
		o.value = v;
		return o;
	}

	var options = document.createElement("select");
	options.appendChild(make_option(NT_ARRAY, "array"));
	options.appendChild(make_option(NT_OBJECT, "object"));
	options.appendChild(make_option(NT_STRING, "string"));
	options.appendChild(make_option(NT_BOOLEAN, "boolean"));
	options.appendChild(make_option(NT_FLOAT, "float"));
	options.appendChild(make_option(NT_UINT8, "uint8"));
	options.appendChild(make_option(NT_UINT16, "uint16"));
	options.appendChild(make_option(NT_UINT32, "uint32"));
	options.appendChild(make_option(NT_INT8, "int8"));
	options.appendChild(make_option(NT_INT16, "int16"));
	options.appendChild(make_option(NT_INT32, "int32"));
	options.appendChild(make_option(NT_INSTANCE_ID, "instance_id"));
	options.appendChild(make_option(NT_NULL, "null"));
	options_select_html = options.innerHTML;
}

function make_json_editor(e, j) {
	var ed = {
		node_type: null,
		node: null,
		dom: null,
		children: null,

		make: function (e, j) {
			this.node_type = j["type"];
			this.dom = document.createElement("div");
			this.dom.className = "object";

			var options = document.createElement("select");
			options.innerHTML = options_select_html;
			options.value = j["type"];
			var options_wrap = document.createElement("div");
			options_wrap.className = "object_type";
			options_wrap.appendChild(options);
			this.dom.appendChild(options_wrap);

			var c = document.createElement("div");
			c.className = "object_value type_" + options.options[options.selectedIndex].text;

			if (j["type"] == NT_ARRAY) {
				this.children = [];

				var w = createElementWithTextNode("span", "[");
				w.className = "container_mark";
				c.appendChild(w);

				// TODO: spoiler mechanic

				var cc = document.createElement("div");
				cc.className = "object_contents";
				c.appendChild(cc);

				var d;
				for (var v of j.value) {
					d = document.createElement("div");
					d.className = "object_field";
					this.children.push([k, make_json_editor(d, v)]);
					// TODO: d.appendChild() `-` button
					cc.appendChild(d);
				}

				// d = document.createElement("div");
				// TODO: d.appendChild() `+` button
				// cc.appendChild(d);

				w = createElementWithTextNode("span", "]");
				w.className = "container_mark";
				c.appendChild(w);
			} else if (j["type"] == NT_OBJECT) {
				this.children = [];

				var w = createElementWithTextNode("span", "{");
				w.className = "container_mark";
				c.appendChild(w);

				// TODO: spoiler mechanic

				var cc = document.createElement("div");
				cc.className = "object_contents";
				c.appendChild(cc);

				var d;
				for (var k in j.value) {
					d = document.createElement("div");
					d.className = "object_field";
					var key = document.createElement("input");
					key.className = "object_field_name";
					key.value = k;
					d.appendChild(key);
					this.children.push([k, make_json_editor(d, j.value[k])]);
					// TODO: d.appendChild() `-` button
					cc.appendChild(d);
				}

				// d = document.createElement("div");
				// TODO: d.appendChild() `+` button
				// cc.appendChild(d);

				w = createElementWithTextNode("span", "}");
				w.className = "container_mark";
				c.appendChild(w);
			} else {
				var inp = document.createElement("input");
				inp.value = ""+j.value;
				c.appendChild(inp);
			}
			this.dom.appendChild(c);

			e.appendChild(this.dom);
		},
	};
	ed.make(e, j);
	return ed;
}
