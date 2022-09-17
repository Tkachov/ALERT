const USER_STORED_FIELDS = ["toc_path", "locale"];
const USER_STORAGE_KEY = "user";
const POSSIBLE_STATES = ["editor"];

/* TODO: asset editor: 
	- header with size field
	- strings block: keep, replace, append
	- sections: keep, replace
*/

var viewer = { ready: false };
var controller = {
	user: {
		toc_path: "",
		locale: "en"
	},

	state: "editor",
	sending_input: false,

	// editor

	toc: null,
	assets: new Map(),
	asset_ids: new Map(),

	// submit forms

	splashes: {
		load_toc: {
			loading: false,
			error: null
		}
	},

	editor: {
		search: {
			error: null,
			results: []
		},

		editor: {
			index: null,
			report: null,
			edited: null
		}
	},

	init: function () {
		this.load_user();
		this.render();

		document.body.onkeyup = function(e) {
			var k = e.keyCode || e.which;
			if (k == 27) { // escape
				e.preventDefault();
				document.getElementById("settings").classList.toggle("open");
			}
		};
	},

	load_user: function () {
		var v = load_from_storage(USER_STORAGE_KEY);
		if (v == null) return;
		for (var f of USER_STORED_FIELDS) {
			this.user[f] = v[f];
		}
	},

	save_user: function () {
		var fields = {};
		for (var f of USER_STORED_FIELDS) {
			fields[f] = this.user[f];
		}
		save_into_storage(USER_STORAGE_KEY, fields);
	},

	get_localized: function (k) {
		return localization.get_localized(k, this.user.locale);
	},

	first_render: true,

	initial_render: function () {
		document.title = this.get_localized("ui/title");

		function replace_text(e, t) {
			e.innerHTML = "";
			e.appendChild(document.createTextNode(t));
		}

		/* load_toc */

		replace_text(document.getElementById("form_description"), this.get_localized("ui/splashes/load_toc/form_description"));
		var e = document.getElementById("toc_path");
		e.placeholder = this.get_localized("ui/splashes/load_toc/path_placeholder");
		e.value = this.user.toc_path;

		e = document.getElementById("load_toc_form");
		e.onsubmit = this.trigger_toc_load.bind(this);

		/* editor */

		e = document.getElementById("search_form");
		e.onsubmit = this.search_assets.bind(this);

		/* options */

		var self = this;

		document.getElementById("settings").onclick = function (ev) {
			var el = document.getElementById("settings");
			if (el == ev.target)
				el.classList.remove("open");
		};

		replace_text(document.getElementById("settings_title"), this.get_localized("ui/settings/title"));

		// language
		replace_text(document.getElementById("settings_language_label"), this.get_localized("ui/settings/language"));
		var select = document.getElementById("settings_language_select");
		for (var ch of select.children)
			replace_text(ch, this.get_localized("ui/settings/language_option_" + ch.value));
		select.value = this.user.locale;
		select.onchange = function () {
			var lang = document.getElementById("settings_language_select");
			self.user.locale = lang.value;
			self.save_user();
			self.initial_render();
			self.render();
		};
	},

	render: function () {
		if (this.first_render) {
			this.first_render = false;
			this.initial_render();
		}

		for (var s of POSSIBLE_STATES) {
			var e = document.getElementById(s);
			e.className = "locale_" + this.user.locale;
			if (s == this.state)
				e.classList.add("open");
		}

		this._render_splashes();
		if (this.state == "editor") this._render_editor();
	},

	_render_splashes: function () {
		var splash_load_toc = false;
		var splash_toc_loading = false;

		if (this.toc == null) {
			if (!this.splashes.load_toc.loading) splash_load_toc = true;
			else splash_toc_loading = true;
		}

		//

		var e = document.getElementById("load_toc");
		if (splash_load_toc) e.classList.add("open");
		else e.classList.remove("open");

		if (splash_load_toc) {
			var errmsg = "";
			if (this.splashes.load_toc.error != null) errmsg = this.splashes.load_toc.error;
			e = document.getElementById("load_toc_warning");
			e.innerHTML = "";
			e.appendChild(document.createTextNode(errmsg));
		}

		//

		e = document.getElementById("toc_loading");
		if (splash_toc_loading) e.classList.add("open");
		else e.classList.remove("open");
	},

	_render_editor: function () {
		if (this.toc == null) return;

		// search

		var e = document.getElementById("results");
		e.innerHTML = "";

		if (this.editor.search.error == null) {
			var sp = createElementWithTextNode("span", (this.editor.search.results.length == 0 ? "No results found" : this.editor.search.results.length + " results found:"));
			sp.style.display = "block";
			sp.style.padding = "2pt";
			sp.style.marginBottom = "10pt";
			e.appendChild(sp);

			for (var r of this.editor.search.results) {
				e.appendChild(this.make_search_result(e, r));
			}
		} else {
			e.appendChild(createElementWithTextNode("b", "Error: " + this.editor.search.error));
		}

		/*
		// gray out if this.sending_input
		if (this.sending_input)
			document.body.classList.add("sending_input");
		else
			document.body.classList.remove("sending_input");
		*/

		this._render_asset_editor();
	},

	_render_asset_editor: function () {
		var e = document.getElementById("asset_editor");
		var show = (this.editor.editor.index != null);
		
		if (show) e.classList.add("open");
		else e.classList.remove("open");
		
		if (!show) return;

		var self = this;
		e.onclick = function (ev) {
			if (ev.target == e) {
				self.editor.editor.index = null;
				self.render();
			}
		};

		//

		if (this.editor.editor.edited == null) {
			var edited = {
				header: {
					magic: this.editor.editor.report.header.magic,
					size: this.editor.editor.report.header.size,
					recalculate_size: true,
					rest: []
				},
				strings: {
					option: 0
				},
				sections: []
			};

			for (var r of this.editor.editor.report.header.rest) {
				edited.header.rest.push(r);
			}

			this.editor.editor.edited = edited;
		}

		//
		
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
		input.value = this.editor.editor.report.header.magic;
		input.disabled = true;
		h.appendChild(input);

		input = document.createElement("input");
		input.type = "number";
		input.value = this.editor.editor.report.header.size;
		input.disabled = true;
		h.appendChild(input);

		h.appendChild(document.createElement("br"));

		for (var r of this.editor.editor.report.header.rest) {
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
		s.appendChild(createElementWithTextNode("span", "Strings block (" + this.editor.editor.report.strings.count + " strings/" + this.editor.editor.report.strings.size + " bytes)"));
		
		var a = createElementWithTextNode("a", "Save raw");
		a.href = "/api/editor/save_strings?index=" + this.editor.editor.index;
		a.target = "_blank";
		s.appendChild(a);
		original.appendChild(s);

		for (var section of this.editor.editor.report.sections) {
			var tag = section.tag.toString(16).toUpperCase();
			var color = tag.substr(1, 6);

			s = document.createElement("div");
			s.className = "section";

			clr = document.createElement("span");
			clr.style.background = "#" + color;
			s.appendChild(clr);
			s.appendChild(createElementWithTextNode("span", tag + " (" + section.size + " bytes)"));
			
			a = createElementWithTextNode("a", "Save raw");
			a.href = "/api/editor/save_section?index=" + this.editor.editor.index + "&section=" + section.tag;
			a.target = "_blank";
			s.appendChild(a);
			original.appendChild(s);
		}

		a = createElementWithTextNode("a", "Extract asset (" + this.editor.editor.report.total_size + " bytes)");
		a.className = "bottom_button";
		a.href = "/api/editor/extract?index=" + this.editor.editor.index;
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
		input.value = this.editor.editor.edited.header.magic;
		input.disabled = true;
		h.appendChild(input);

		input = document.createElement("input");
		input.type = "number";
		input.value = this.editor.editor.edited.header.size;
		input.disabled = this.editor.editor.edited.header.recalculate_size;
		h.appendChild(input);

		input = document.createElement("input");
		input.type = "checkbox";
		input.name = "recalculate_size";
		input.id = "recalculate_size";
        input.checked = this.editor.editor.edited.header.recalculate_size;
        h.appendChild(input);

        var label = createElementWithTextNode("label", "Put final size in this field automatically");
        label.htmlFor = "recalculate_size";
        h.appendChild(label);

		h.appendChild(document.createElement("br"));

		for (var r of this.editor.editor.edited.header.rest) {
			input = document.createElement("input");
			input.type = "number";
			input.value = r;
			h.appendChild(input);
		}

		a = createElementWithTextNode("a", "Save edited asset");
		a.className = "bottom_button";
		// TODO: onclick
		edited.appendChild(a);
	},

	/* search */

	make_search_result: function (container, r) {
		var e = document.createElement("div");
		e.className = "result_entry";
		e.appendChild(createElementWithTextNode("b", r.name));
		e.appendChild(createElementWithTextNode("span", this.toc.archives_map[r.archive]));
		e.title = r.aid + (r.path != "" ? " - " + r.path : "");

		var self = this;
		e.onclick = function () {
			self.change_selected(container, e);
			self.make_asset_details(r);
			if (r.path != "") self.make_entry_onclick(r.path, false)();
		}

		return e;
	},

	change_selected: function (container, e) {
		for (var c of container.children) {
			if (c == e) c.classList.add("selected");
			else c.classList.remove("selected");
		}
		e.classList.add("selected");
	},

	/* details tab */

	make_toc_details: function () {
		if (this.toc == null) return;

		var e = document.getElementById("details");
		e.innerHTML = "";

		e.appendChild(createElementWithTextNode("b", "TOC"));
		e.appendChild(createElementWithTextNode("p", this.toc.archives + " archives, " + this.toc.assets + " assets"));
	},

	make_asset_details: function (entry) {
		var e = document.getElementById("details");
		e.innerHTML = "";

		e.appendChild(createElementWithTextNode("b", entry.name));
		if (entry.path != "") {
			e.appendChild(createElementWithTextNode("p", entry.path + " (" + this.toc.archives_map[entry.archive] + ")"));
			e.appendChild(createElementWithTextNode("span", entry.aid));
		} else {
			e.appendChild(createElementWithTextNode("p", this.toc.archives_map[entry.archive]));
		}

		if (this.assets.has(entry.index)) {
			var info = this.assets.get(entry.index);
			e.appendChild(document.createElement("hr"));
			e.appendChild(createElementWithTextNode("p", "size: " + info.size));
			if (info.type != null) {
				e.appendChild(createElementWithTextNode("p", "type: " + info.type));
				e.appendChild(createElementWithTextNode("p", "magic: " + info.magic));
				e.appendChild(createElementWithTextNode("p", "sections: " + info.sections));

				e.appendChild(document.createElement("hr"));

				{
					var btn = createElementWithTextNode("a", "Sections report");
					e.appendChild(btn);
					var self = this;
					btn.onclick = function () {
						self.get_asset_report(entry.index);
					};
				}

				{
					var btn = createElementWithTextNode("a", "Edit asset");
					e.appendChild(btn);
					var self = this;
					btn.onclick = function () {
						self.get_asset_editor(entry.index);
					};
				}

				if (info.type == "Model") {
					var btn = createElementWithTextNode("a", "Open in viewer");
					e.appendChild(btn);
					var self = this;
					btn.onclick = function () {
						viewer.show_mesh("/api/model?index=" + entry.index);
					};
				}
			}
		} else {
			var self = this;
			this.extract_asset(entry.index, function () { self.make_asset_details(entry); }, function () {});
		}
	},

	/* directories tree / content browser */

	traverse_tree: function (tree, current_path) {
		for (var k in tree) {
			if (is_array(tree[k])) {
				this.asset_ids.set(tree[k][0], current_path + k);
			} else {
				this.traverse_tree(tree[k], current_path + k + "/");
			}
		}
	},

	fill_structs: function () {
		for (var k in this.toc.assets_map) {
			this.asset_ids.set(k, "");
		}

		this.traverse_tree(this.toc.tree, "");
	},

	get_entry_info: function (path) {
		var result = {
			path: path,
			tree_node: null,
			crumbs: [],
			is_file: false,
			aid: "",
			basedir: ""
		};

		if (path != "") result.crumbs = path.split("/");

		result.tree_node = this.toc.tree;
		if (result.crumbs.length > 0) {
			for (var i=0; i<result.crumbs.length-1; ++i) {
				var p = result.crumbs[i];
				if (is_array(result.tree_node[p])) break;
				result.tree_node = result.tree_node[p];
			}

			var last = result.crumbs[result.crumbs.length-1];
			if (is_array(result.tree_node[last])) {
				result.is_file = true;
				result.aid = result.tree_node[last][0];
			} else {
				result.tree_node = result.tree_node[last];
			}
		}

		var len = result.crumbs.length - (result.is_file ? 1 : 0);
		for (var i=0; i<len; ++i) {
			result.basedir += result.crumbs[i] + "/";
		}

		return result;
	},

	make_entry_onclick: function (path, update_search) {
		var self = this;
		return function (ev) {
			var e = self.get_entry_info(path);
			self.make_content_browser(e);
			self.select_tree_node(e);

			if (e.is_file && update_search) {
				var s = document.getElementById("search");
				if (s.value != e.aid) {
					s.value = e.aid;
					self.search_assets();
				}
			}
		};
	},

	_browser_made_for_entry: null,

	make_content_browser: function (entry) {
		var remake_browser = true;
		if (this._browser_made_for_entry != null && this._browser_made_for_entry.basedir == entry.basedir) {
			remake_browser = false;
		}

		this._browser_made_for_entry = entry;

		if (remake_browser) {
			var e = document.getElementById("browser");
			e.innerHTML = "";

			var crumbs = document.createElement("div");
			crumbs.className = "breadcrumbs";

			function add_breadcrumb(parent, self, full_path, crumb) {
				if (parent.children.length > 0) {
					var sep = document.createElement("span");
					sep.className = "separator";
					parent.appendChild(sep);
				}

				var b = createElementWithTextNode("span", crumb);
				b.className = "breadcrumb";
				b.onclick = self.make_entry_onclick(full_path, true);
				parent.appendChild(b);
			}

			var self = this;
			add_breadcrumb(crumbs, self, "", "home");

			var full_path = "";
			var len = entry.crumbs.length - (entry.is_file ? 1 : 0);
			if (len > 0) {		
				for (var i=0; i<len; ++i) {
					var p = entry.crumbs[i];
					full_path += p;
					add_breadcrumb(crumbs, self, full_path, p);
					full_path += "/";
				}
			}

			var directories = [];
			var files = [];
			var n = entry.tree_node;
			for (var k in n) {
				if (is_array(n[k])) {
					files.push(k);
				} else {
					directories.push(k);
				}
			}
			directories.sort();
			files.sort();

			var folder = document.createElement("div");
			folder.className = "contents";

			for (var d of directories) {
				var item = document.createElement("span");
				item.className = "directory";
				item.appendChild(createElementWithTextNode("span", d));
				item.onclick = this.make_entry_onclick(entry.basedir + d, true);
				folder.appendChild(item);
			}

			var is_multiple;
			for (var f of files) {
				is_multiple = (entry.tree_node[f][1].length > 1);
				var item = document.createElement("span");
				item.className = "file" + (is_multiple ? " multiple" : "");
				item.appendChild(createElementWithTextNode("span", f));
				item.onclick = this.make_entry_onclick(entry.basedir + f, true);
				if (is_multiple) {
					var badge = createElementWithTextNode("span", "" + entry.tree_node[f][1].length);
					badge.className = "multiple_badge";
					item.appendChild(badge);
				}
				folder.appendChild(item);
			}

			e.appendChild(crumbs);
			e.appendChild(folder);
		}

		if (entry.is_file) {
			var e = document.getElementById("browser");
			
			var files = e.querySelectorAll(".directory");
			for (var f of files) {
				f.classList.remove("selected");
			}

			var selected = null;
			files = e.querySelectorAll(".file");
			for (var f of files) {
				f.classList.remove("selected");
				
				if (f.children[0].innerText == entry.crumbs[entry.crumbs.length-1])
					selected = f;
			}

			if (selected != null) {
				selected.classList.add("selected");
				selected.scrollIntoView({behavior: "smooth", block: "center"});
			}
		}
	},

	_selected_tree_node: null,

	select_tree_node: function (e) {
		if (this._selected_tree_node != null)
			this._selected_tree_node.classList.remove("selected");

		var n = document.getElementById("left_column").children[0];
		if (e.path == "") {
			n = n.children[0].children[0];
		} else {
			var next = n;
			for (var c of e.crumbs) {
				n.classList.remove("closed");
				n = next;
				for (var i=0; i<n.children.length; ++i) {
					if (n.children[i].innerText == c) {
						if (n.children[i].classList.contains("directory"))
							next = n.children[i+1].children[0];
						
						n = n.children[i];
						break;
					}
				}
			}
		}

		this._selected_tree_node = n;
		this._selected_tree_node.classList.add("selected");
		this._selected_tree_node.scrollIntoView({behavior: "smooth", block: "center"});
	},

	make_directories_tree: function () {
		function is_array(s) {
			return (s.constructor === Array);
		}

		function build_tree(self, tree, prefix, depth=0) {
			var directories = [];
			var files = [];
			for (var k in tree) {
				if (is_array(tree[k])) {
					files.push(k);
				} else {
					directories.push(k);
				}
			}
			directories.sort();
			files.sort();

			function make_dir_onclick(self, p, path) {
				return function (ev) {
					if (ev.target == p) {
						p.classList.toggle("closed");
					}
				};
			}

			var c = document.createElement("div");
			for (var d of directories) {
				var p = document.createElement("p");
				p.className = "entry directory closed";
				p.style.marginLeft = "-" + (5 + depth*20) + "pt";
				p.style.paddingLeft = (5 + depth*20) + "pt";
				p.onclick = make_dir_onclick(self, p, prefix + d);

				var s = document.createElement("span");
				s.className = "fname";
				s.innerHTML = d;
				s.title = d;
				s.onclick = self.make_entry_onclick(prefix + d, true);
				p.appendChild(s);
				c.appendChild(p);

				var ct = document.createElement("div");
				ct.className = "directory_contents";
				ct.appendChild(build_tree(self, tree[d], prefix + d + "/", depth+1));
				c.appendChild(ct);
			}

			function make_file_onclick(self, p, aid, path) {
				return function () {
					self._select_tree_node(p);
					self.make_content_browser(path);

					var e = document.getElementById("search");
					e.value = aid;
					self.search_assets();
				};
			}

			for (var f of files) {
				var p = document.createElement("p");
				p.className = "entry file";
				p.style.marginLeft = "-" + (5 + depth*20) + "pt";
				p.style.paddingLeft = (5 + depth*20) + "pt";
				// p.onclick = make_file_onclick(self, p, tree[f][0], prefix + f);
				p.onclick = self.make_entry_onclick(prefix + f, true);

				var s = document.createElement("span");
				s.className = "fname";
				s.innerHTML = f;
				s.title = f;
				p.appendChild(s);
				c.appendChild(p);
			}

			return c;
		}

		var e = document.getElementById("left_column");
		e.innerHTML = "";
		e.appendChild(build_tree(this, this.toc.tree, ""));

		// home + separator

		var first = (e.children.length > 0 ? e.children[0] : e);

		var sep = document.createElement("div");
		sep.className = "separator";
		first.insertBefore(sep, first.firstChild);

		{
			var self = this;
			var depth = 0;
			var f = "home";
			var c = document.createElement("div");
			var p = document.createElement("p");
				p.className = "entry file";
				p.style.marginLeft = "-" + (5 + depth*20) + "pt";
				p.style.paddingLeft = (5 + depth*20) + "pt";
				// p.onclick = function () { self.make_content_browser(""); };
				p.onclick = this.make_entry_onclick("", false);

				var s = document.createElement("span");
				s.className = "fname";
				s.innerHTML = f;
				s.title = f;
				p.appendChild(s);
				c.appendChild(p);
				first.insertBefore(c, first.firstChild);
		}

		this.make_content_browser(this.get_entry_info(""));
	},

	/* asset report */

	make_asset_report: function (index, report) {
		var e = document.getElementById("asset_report");
		e.innerHTML = "";

		var d = document.createElement("div");
		e.appendChild(d);

		var h = document.createElement("div");
		h.className = "header";
		var sp = document.createElement("div");
		d.appendChild(h);
		sp.className = "content";
		d.appendChild(sp);

		var self = this;
		var oe = createElementWithTextNode("a", "Edit asset");
		oe.className = "editor_button";
		oe.onclick = function () { self.get_asset_editor(index); };
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

		e.classList.add("open");
		e.onclick = function (ev) { if (ev.target == e) e.classList.remove("open"); };
	},

	/* api calls */

	trigger_toc_load: function () {
		var e = document.getElementById("toc_path");
		var path = e.value;

		this.user.toc_path = path;
		this.save_user();

		this.sending_input = true;
		this.splashes.load_toc.loading = true;

		var self = this;
		ajax.postAndParseJson(
			"api/load_toc", {
				toc_path: path
			},
			function(r) {
				self.sending_input = false;
				self.splashes.load_toc.loading = false;

				if (r.error) {
					self.splashes.load_toc.error = r.message;
					self.render();
					return;
				}

				self.splashes.load_toc.error = null;
				self.state = "editor";
				self.toc = r.toc;
				self.fill_structs();
				self.make_toc_details();
				self.make_directories_tree();
				self.render();
			},
			function(e) {
				self.sending_input = false;
				self.splashes.load_toc.loading = false;
				self.splashes.load_toc.error = e;
				self.render();
			}
		);

		this.render();

		return false; // invalidate form anyways (so it won't refresh the page on submit)
	},

	search_assets: function () {
		var e = document.getElementById("search");
		var v = e.value;

		/*
		this.sending_input = true;

		var self = this;
		ajax.postAndParseJson(
			"api/search_assets", {
				needle: v
			},
			function(r) {
				self.sending_input = false;

				if (r.error) {
					self.editor.search.error = r.message;
					self.render();
					return;
				}

				self.editor.search.error = null;
				self.editor.search.results = r.entries;
				self.render();
			},
			function(e) {
				self.sending_input = false;
				self.editor.search.error = e;
				self.render();
			}
		);

		this.render();
		*/

		function add_results(self, array, aid, path) {
			if (path == "") {
				for (var i of self.toc.assets_map[aid])
					array.push({index: i[0], archive: i[1], aid: aid, name: aid, path: ""});
				return;
			}

			var e = self.get_entry_info(path);
			var basename = e.crumbs[e.crumbs.length-1];
			for (var i of e.tree_node[basename][1])
				array.push({index: i[0], archive: i[1], aid: e.aid, name: basename, path: path});
		}

		function meets_request(s, terms) {
			if (s == null || s == "") return false;

			for (var t of terms) {
				if (!s.includes(t))
					return false;
			}

			return true;
		}

		try {
			this.editor.search.results = [];

			if (this.asset_ids.has(v)) {
				add_results(this, this.editor.search.results, v, this.asset_ids.get(v));
			} else {
				var parts = v.split(" ");
				var terms = [];
				var hexonly = true;
				for (var p of parts) {
					if (p.trim() != "") {
						var normalized = p.trim().toLowerCase().replaceAll("\\", "/");
						terms.push(normalized);

						if (hexonly) {
							for (var c of normalized) {
								if (!"0123456789abcdef".includes(c)) {
									hexonly = false;
									break;
								}
							}
						}
					}
				}

				if (terms.length > 0)
				{
					for (let [k, path] of this.asset_ids.entries()) {
						if ((hexonly && meets_request(k.toLowerCase(), terms)) || (path != "" && meets_request(path, terms)))
							add_results(this, this.editor.search.results, k, path);
					}
				}
			}
		} catch (e) {
			console.log(e);
			this.editor.search.error = e.name + ": " + e.message;
		}

		this.render();

		if (this.editor.search.results.length == 1) {
			var e = document.getElementById("results");
			e = e.querySelector(".result_entry");
			if (e != null) e.onclick();
		}

		return false; // invalidate form anyways (so it won't refresh the page on submit)
	},

	extract_asset: function (index, success_cb, failure_cb) {
		var self = this;
		ajax.postAndParseJson(
			"api/extract_asset", {
				index: index
			},
			function(r) {
				if (r.error) {
					// TODO: self.editor.search.error = r.message;
					failure_cb();
					return;
				}

				// TODO: self.editor.search.error = null;
				self.assets.set(index, r.asset);
				success_cb();
			},
			function(e) {				
				// TODO: self.editor.search.error = e;
				failure_cb();
			}
		);
	},

	get_asset_report: function (index) {
		var self = this;
		ajax.postAndParseJson(
			"api/asset_report", {
				index: index
			},
			function(r) {
				if (r.error) {
					// TODO: self.editor.search.error = r.message;
					return;
				}

				// TODO: self.editor.search.error = null;
				self.make_asset_report(index, r.report);
			},
			function(e) {				
				// TODO: self.editor.search.error = e;
			}
		);
	},

	get_asset_editor: function (index) {
		var self = this;
		ajax.postAndParseJson(
			"api/asset_editor", {
				index: index
			},
			function(r) {
				if (r.error) {
					// TODO: self.editor.search.error = r.message;
					return;
				}

				// TODO: self.editor.search.error = null;
				self.editor.editor.index = index;
				self.editor.editor.report = r.report;
				self.editor.editor.edited = null;
				self.render();
			},
			function(e) {				
				// TODO: self.editor.search.error = e;
			}
		);
	}
};

this.onload = controller.init.bind(controller);

function save_into_storage(key, obj) {
	localStorage[key] = JSON.stringify(obj);
}

function load_from_storage(key) {
	var i = localStorage.getItem(key);
	if (i) return JSON.parse(i);
	return null;
}

function createElementWithTextNode(tag, text) {
	var e = document.createElement(tag);
	e.appendChild(document.createTextNode(text));
	return e;
}

//

function is_string(s) {
	return (typeof s === 'string' || s instanceof String);
}

function is_array(s) {
	return (s.constructor === Array);
}

function hexToLuma(hex) {
	const r = parseInt(hex.substr(0, 2), 16);
	const g = parseInt(hex.substr(2, 2), 16);
	const b = parseInt(hex.substr(4, 2), 16);
	return [0.299 * r, 0.587 * g, 0.114 * b].reduce((a, b) => a + b) / 255;
}
