const USER_STORED_FIELDS = ["toc_path", "locale"];
const USER_STORAGE_KEY = "user";
const POSSIBLE_STATES = ["editor"];

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
	},

	make_search_result: function (container, r) {
		var e = document.createElement("div");
		e.className = "result_entry";
		e.appendChild(createElementWithTextNode("b", r.id));
		e.appendChild(createElementWithTextNode("span", r.index));

		var self = this;
		e.onclick = function () {
			self.change_selected(container, e);
			self.make_asset_details(r);
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

		e.appendChild(createElementWithTextNode("b", entry.id));
		e.appendChild(createElementWithTextNode("p", "size: " + entry.size));
		e.appendChild(createElementWithTextNode("p", "archive: " + entry.archive));

		if (this.assets.has(entry.index)) {
			var info = this.assets.get(entry.index);
			e.appendChild(createElementWithTextNode("p", "type: " + info.type));
			e.appendChild(createElementWithTextNode("p", "magic: " + info.magic));
			e.appendChild(createElementWithTextNode("p", "sections: " + info.sections));

			if (info.type == "Model") {
				var btn = createElementWithTextNode("a", "Open in viewer");
				e.appendChild(btn);
				var self = this;
				btn.onclick = function () {
					viewer.show_mesh("/api/model?index=" + entry.index);
				};
			}
		} else {
			var self = this;
			this.extract_asset(entry.index, function () { self.make_asset_details(entry); }, function () {});
		}
	},

	make_content_browser: function (path) {

		var parts = [];
		if (path != "") parts = path.split("/");

		var e = document.getElementById("browser");
		e.innerHTML = "";

		var crumbs = document.createElement("div");
		crumbs.className = "breadcrumbs";

		var self = this;
		var b = createElementWithTextNode("span", "home");
			b.className = "breadcrumb";
			b.onclick = function () { self.make_content_browser(""); };
			crumbs.appendChild(b);

function is_string(s) {
	return (typeof s === 'string' || s instanceof String);
}

function is_array(s) {
	return (s.constructor === Array);
}

var highlighted_file = null;

		var n = this.toc.tree;
		if (parts.length > 0) {
		// for (var p of parts) {
		for (var i=0; i<parts.length-1; ++i) {
			var p = parts[i];
			if (is_array(n[p])) {
				highlighted_file = p;
				break;
			}

			n = n[p];

			var sep = document.createElement("span");
			sep.className = "separator";
			crumbs.appendChild(sep);

			var b = createElementWithTextNode("span", p); // breadcrumb to <n>
			b.className = "breadcrumb";
			crumbs.appendChild(b);
		}

		var last = parts[parts.length-1];
		if (!is_array(n[last])) {
			n = n[last];

			var sep = document.createElement("span");
			sep.className = "separator";
			crumbs.appendChild(sep);

			var b = createElementWithTextNode("span", last); // breadcrumb to <n>
			b.className = "breadcrumb";
			crumbs.appendChild(b);
		}
	}

			var directories = [];
	var files = [];
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
			folder.appendChild(item);
		}

		for (var f of files) {
			var item = document.createElement("span");
			item.className = "file";
			item.appendChild(createElementWithTextNode("span", f));
			folder.appendChild(item);
		}

		e.appendChild(crumbs);
		e.appendChild(folder);
	},

	_selected_tree_node: null,

	_select_tree_node: function (e) {
		if (this._selected_tree_node != null)
			this._selected_tree_node.classList.remove("selected");

		this._selected_tree_node = e;
		this._selected_tree_node.classList.add("selected");
	},

	make_directories_tree: function () {

function sorted_tree(tree_list) {
	var items = [];
	for (var k in tree_list)
		items.push({"item": tree_list[k], "name": k});
	items.sort(function (a, b) {
		if (a.item.type != b.item.type) {
			if (a.item.type == "directory")
				return 1;
			return -1;
		}
		if (a.name > b.name)
			return 1;
		if (a.name < b.name)
			return -1;
		return 0;
	});
	return items;
}

/*
function build_tree(tree, filename, depth=0) {
	// console.log(tree, filename);
	if (tree.type == "file") {
		var p = document.createElement("p");
		p.className = "entry file";
		p.style.marginLeft = "-" + (5 + depth*20) + "pt";
		p.style.paddingLeft = (5 + depth*20) + "pt";
		var s = document.createElement("span");
		s.className = "fname";
		s.innerHTML = filename;
		s.title = filename;
		p.appendChild(s);
		s = document.createElement("span");
		s.className = "size";
		s.innerHTML = fix_size(tree.size);
		p.appendChild(s);
		return p;
	}

	if (filename == "") {
		if (tree.list.length < 2) {
			for (var k in tree.list)
				return build_tree(tree.list[k], k, depth+1)
			return document.createTextNode("");
		}

		var c = document.createElement("div");
		var sorted = sorted_tree(tree.list);
		for (var t of sorted) {
			c.appendChild(build_tree(t.item, t.name, depth+1));
		}
		return c;
	}

	var c = document.createElement("div");	
	var p = document.createElement("p");
	p.className = "entry directory";
	p.style.marginLeft = "-" + (5 + depth*20) + "pt";
	p.style.paddingLeft = (5 + depth*20) + "pt";
	p.onclick = function () {
		p.classList.toggle("closed");
	};
	var s = document.createElement("span");
	s.className = "fname";
	s.innerHTML = filename;
	s.title = filename;
	p.appendChild(s);
	c.appendChild(p);
	var ct = document.createElement("div");
	ct.className = "directory_contents";
	var sorted = sorted_tree(tree.list);
		for (var t of sorted) {
			ct.appendChild(build_tree(t.item, t.name, depth+1));
		}
	c.appendChild(ct);
	return c;
}
*/

function is_string(s) {
	return (typeof s === 'string' || s instanceof String);
}

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

	/*
	var c = document.createElement("div");
	var p = document.createElement("p");
	p.className = "entry directory";
	p.style.marginLeft = "-" + (5 + depth*20) + "pt";
	p.style.paddingLeft = (5 + depth*20) + "pt";
	p.onclick = function () {
		p.classList.toggle("closed");
	};
	var s = document.createElement("span");
	s.className = "fname";
	s.innerHTML = filename;
	s.title = filename;
	p.appendChild(s);
	c.appendChild(p);
	var ct = document.createElement("div");
	ct.className = "directory_contents";
	var sorted = sorted_tree(tree.list);
		for (var t of sorted) {
			ct.appendChild(build_tree(t.item, t.name, depth+1));
		}
	c.appendChild(ct);
	return c;
	*/

	function make_dir_onclick(self, p, path) {
		return function () {
			self._select_tree_node(p);
			self.make_content_browser(path);
			p.classList.toggle("closed");
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
		p.onclick = make_file_onclick(self, p, tree[f][0], prefix + f);

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
		p.onclick = function () { self.make_content_browser(""); };

		var s = document.createElement("span");
		s.className = "fname";
		s.innerHTML = f;
		s.title = f;
		p.appendChild(s);
		c.appendChild(p);
		first.insertBefore(c, first.firstChild);
}

/*
var en = e.querySelector(".entry");
if (en != null) en.onclick();
*/
this.make_content_browser("");

	},

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
