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
		} else {
			var self = this;
			this.extract_asset(entry.index, function () { self.make_asset_details(entry); }, function () {});
		}
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
