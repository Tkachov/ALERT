assets_browser = {
	ready: false,

	toc: null,
	assets: new Map(),
	asset_ids: new Map(),

	search: {
		error: null,
		results: []
	},

	init: function () {
		this.ready = true;

		var e = document.getElementById("search_form");
		e.onsubmit = this.search_assets.bind(this);
	},

	//

	toc_loaded: function (toc) {
		this.toc = toc;
		this.fill_structs();
		this.make_toc_details();
		this.make_directories_tree();
		this.render();
	},

	//

	render: function () {
		this.render_search();
	},

	render_search: function () {
		var e = document.getElementById("results");
		e.innerHTML = "";

		if (this.search.error != null) {
			e.appendChild(createElementWithTextNode("b", "Error: " + this.search.error));
			return;
		}

		var sp = createElementWithTextNode("span", (this.search.results.length == 0 ? "No results found" : this.search.results.length + " results found:"));
		sp.style.display = "block";
		sp.style.padding = "2pt";
		sp.style.marginBottom = "10pt";
		e.appendChild(sp);

		for (var r of this.search.results) {
			e.appendChild(this.make_search_result(e, r));
		}
	},

	/* search */

	_get_archive_name: function (arch) {
		return this.toc.archives_map[arch].replaceAll("\x00", "");
	},

	make_search_result: function (container, r) {
		var e = document.createElement("div");
		e.className = "result_entry";
		e.appendChild(createElementWithTextNode("b", r.name));
		e.appendChild(createElementWithTextNode("span", this._get_archive_name(r.archive)));
		e.title = r.aid + (r.path != "" ? " - " + r.path : "");

		var self = this;
		e.onclick = function () {
			self.change_selected(container, e);
			self.make_asset_details(r);
			if (r.path != "") self.make_entry_onclick(r.path, false)();
			else {
				controller.remember_in_history(r.aid);
				self.refresh_collapsible_selection(r.aid);
			}
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
			e.appendChild(createElementWithTextNode("p", entry.path + " (" + this._get_archive_name(entry.archive) + ")"));
			e.appendChild(createElementWithTextNode("span", entry.aid));
		} else {
			e.appendChild(createElementWithTextNode("p", this._get_archive_name(entry.archive)));
		}

		function get_asset_names(self) {
			var shortname = entry.name;
			var fullname = entry.name;
			if (entry.path != "")
				fullname = entry.path;
			fullname += " (" + self._get_archive_name(entry.archive) + ")";
			return [shortname, fullname];
		}

		if (this.assets.has(entry.index)) {
			var info = this.assets.get(entry.index);

			e.appendChild(document.createElement("hr"));
			var desc = "";
			var links = document.createElement("p");
			links.className = "links";

			// generic
			desc = filesize(info.size);

			{
				var btn = createElementWithTextNode("a", "Save as...");
				btn.href = "/api/assets/asset?index=" + entry.index;
				btn.target = "_blank";
				links.appendChild(btn);
			}

			{
				var is_favorite = controller.user.favorites.includes(entry.aid);				
				var btn = createElementWithTextNode("a", (is_favorite ? "Remove from favorites" : "Add to favorites"));
				var self = this;
				btn.onclick = function () {
					if (is_favorite) controller.remove_from_favorites(entry.aid);
					else controller.add_to_favorites(entry.aid);

					self.make_asset_details(entry);
					self.refresh_favorites_entries();
				};
				links.appendChild(btn);
			}

			// dat1
			if (info.type != null) {
				desc = info.type + " (" + info.sections + " sections)\n" + desc;

				var sep = document.createElement("span");
				sep.className = "separator";
				links.appendChild(sep);

				{
					var self = this;
					var btn = createElementWithTextNode("a", "Sections report");
					links.appendChild(btn);
					btn.onclick = function () {
						let [shortname, fullname] = get_asset_names(self);
						sections_viewer.show_viewer(entry.index, shortname, fullname);
					};
				}

				{
					var btn = createElementWithTextNode("a", "Edit sections");
					links.appendChild(btn);
					btn.onclick = function () {
						let [shortname, fullname] = get_asset_names(self);
						sections_editor.show_editor(entry.index, shortname, fullname);
					};
				}
			}

			// config
			if (info.type == "Config" && controller.user.__configs_editor_enabled) {
				var sep = document.createElement("span");
				sep.className = "separator";
				links.appendChild(sep);

				var btn = createElementWithTextNode("a", "Edit");
				links.appendChild(btn);
				btn.onclick = function () {
					let [shortname, fullname] = get_asset_names(self);
					configs_editor.show_editor(entry.index, shortname, fullname);
				};
			}

			// model
			if (info.type == "Model") {
				var sep = document.createElement("span");
				sep.className = "separator";
				links.appendChild(sep);

				var btn = createElementWithTextNode("a", "View");
				links.appendChild(btn);
				var self = this;
				btn.onclick = function () {
					let [shortname, fullname] = get_asset_names(self);
					models_viewer.show_mesh("/api/models_viewer/obj?index=" + entry.index, shortname, fullname);
				};
			}

			// texture
			if (info.type == "Texture") {
				var sep = document.createElement("span");
				sep.className = "separator";
				links.appendChild(sep);

				var btn = createElementWithTextNode("a", "View");
				links.appendChild(btn);
				var self = this;
				btn.onclick = function () {
					let [shortname, fullname] = get_asset_names(self);
					textures_viewer.show_texture(entry.index, shortname, fullname);
				};
			}

			var p = document.createElement("p");
			var parts = desc.split("\n");
			for (var i=0; i<parts.length; ++i) {
				if (i > 0)
					p.appendChild(document.createElement("br"));
				p.appendChild(document.createTextNode(parts[i]));
			}

			e.appendChild(p);
			e.appendChild(links);
		} else {
			var self = this;
			this.extract_asset(
				entry.index,
				function () { self.make_asset_details(entry); },
				function (error_message) {
					e.appendChild(document.createElement("hr"));
					e.appendChild(createElementWithTextNode("b", error_message));
				}
			);
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
			basedir: "",
			thumbnails_info: null
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
				self.make_asset_search_callback(e.aid)();
			}

			if (e.is_file) {
				controller.remember_in_history(e.aid);
				self.refresh_history_entries();
			}
		};
	},

	make_asset_search_callback: function (aid) {
		var self = this;
		return function () {
			var s = document.getElementById("search");
			if (s.value != aid) {
				s.value = aid;
				self.search_assets();
			}
		};
	},

	_browser_made_for_entry: null,
	_browser_thumbnails_path: null,
	_browser_known_thumbnails: new Set(),

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

			if (this._browser_thumbnails_path != entry.basedir) {
				this._browser_thumbnails_path = entry.basedir;

				var self = this;
				ajax.postAndParseJson(
					"api/thumbnails/list", {
						path: full_path
					},
					function(r) {
						if (r.error) {
							// TODO: self.search.error = r.message;
							return;
						}

						// TODO: self.search.error = null;
						for (var taid of r.list) {
							self._browser_known_thumbnails.add(taid);
						}
						if (r.list.length > 0) {
							if (self._browser_made_for_entry != null && self._browser_made_for_entry.basedir == entry.basedir) {
								self._browser_made_for_entry = null; // to trigger remake
								self.make_content_browser(entry);
							}
						}
					},
					function(e) {				
						// TODO: self.search.error = e;
					}
				);
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

				var aid = entry.tree_node[f][0];
				if (this._browser_known_thumbnails.has(aid)) {
					var thumb = document.createElement("img");
					thumb.src = "/api/thumbnails/png?aid=" + aid;
					item.appendChild(thumb);
					item.className += " with_thumbnail";
				}

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

		var n = document.getElementById("left_column").children[0].children[0];
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

		//

		this.refresh_collapsible_selection(e.path);
	},

	make_directories_tree: function () {
		var e = document.getElementById("left_column");
		e.innerHTML = "";

		var d = document.createElement("div");
		d.appendChild(build_tree(this, this.toc.tree, ""));

		// home + separator

		var first = (d.children.length > 0 ? d.children[0] : d);

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
		e.appendChild(d);

		// history & favorites

		d = document.createElement("div");
		d.className = "history collapsible collapsed";
		e.appendChild(d);
		this.refresh_history_entries();

		d = document.createElement("div");
		d.className = "favorites collapsible collapsed";
		e.appendChild(d);
		this.refresh_favorites_entries();
	},

	make_left_column_collapsible_section: function (d, name, assets, assets_function) {
		d.innerHTML = "";

		var h = createElementWithTextNode("span", name);
		h.onclick = function () {
			d.classList.toggle("collapsed");
		};
		d.appendChild(h);

		var c = document.createElement("div");
		c.className = "content";
		d.appendChild(c);

		if (assets.length == 0) {
			var m = createElementWithTextNode("span", "Nothing here yet");
			m.className = "empty_message";
			c.appendChild(m);
		} else {
			for (var a of assets) {
				var aid = assets_function(a);
				if (!this.asset_ids.has(aid)) continue;

				var filepath = this.asset_ids.get(aid);
				var filename = aid;
				var onclick;
				
				if (filepath == "") {
					filepath = aid;
					onclick = this.make_asset_search_callback(aid);
				} else {
					var einfo = this.get_entry_info(filepath);
					filename = einfo.crumbs[einfo.crumbs.length-1];
					onclick = this.make_entry_onclick(filepath, true);
				}

				c.appendChild(make_file_entry_generic(onclick, filename, filepath, 0));
			}
		}
	},

	_selected_collapsible_path: null,

	refresh_history_entries: function () {
		var e = document.getElementById("left_column");
		var d = e.children[1];
		this.make_left_column_collapsible_section(d, "Recently viewed", controller.user.history.entries, function (x) { return x[0]; });

		var d = d.children[1];
		for (var c of d.children) {
			if (c.classList.contains("entry") && c.children[0].title == this._selected_collapsible_path) c.classList.add("selected");
			else c.classList.remove("selected");
		}
	},

	_favorites: null,

	refresh_favorites_entries: function () {
		var e = document.getElementById("left_column");
		var d = e.children[2];

		if (!equal_arrays(this._favorites, controller.user.favorites)) {
			this.make_left_column_collapsible_section(d, "Favorites", controller.user.favorites, function (x) { return x; });
			this._favorites = controller.user.favorites.slice();
		}

		var d = d.children[1];
		var selected = null;
		for (var c of d.children) {
			if (c.classList.contains("entry") && c.children[0].title == this._selected_collapsible_path) {
				c.classList.add("selected");
				selected = c;
			} else {
				c.classList.remove("selected");
			}
		}

		if (selected != null)
			selected.scrollIntoView({behavior: "smooth", block: "center"});
	},

	refresh_collapsible_selection: function (path) {
		this._selected_collapsible_path = path;
		this.refresh_history_entries();
		this.refresh_favorites_entries();
	},

	search_assets: function () {
		var e = document.getElementById("search");
		var v = e.value;

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
			this.search.results = [];

			if (this.asset_ids.has(v)) {
				add_results(this, this.search.results, v, this.asset_ids.get(v));
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
							add_results(this, this.search.results, k, path);
					}
				}
			}
		} catch (e) {
			console.log(e);
			this.search.error = e.name + ": " + e.message;
		}

		this.render();

		if (this.search.results.length >= 1) {
			var e = document.getElementById("results");
			e = e.querySelector(".result_entry");
			if (e != null) e.onclick();
		}

		return false; // invalidate form anyways (so it won't refresh the page on submit)
	},

	extract_asset: function (index, success_cb, failure_cb) {
		var self = this;
		ajax.postAndParseJson(
			"api/assets/get_info", {
				index: index
			},
			function(r) {
				if (r.error) {
					// TODO: self.search.error = r.message;
					failure_cb(r.message);
					return;
				}

				// TODO: self.search.error = null;
				self.assets.set(index, r.asset);
				success_cb();

				if (r.thumbnail != null) {
					self._browser_known_thumbnails.add(r.thumbnail);

					// refresh content browser now
					var entry = self._browser_made_for_entry;
					self._browser_made_for_entry = null;
					self.make_content_browser(entry);
				}
			},
			function(e) {				
				// TODO: self.search.error = e;
				failure_cb(e);
			}
		);
	}
};

//

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

	for (var f of files) {		
		c.appendChild(make_file_entry(self, prefix, f, depth));
	}

	return c;
}

function make_dir_onclick(self, p, path) {
	return function (ev) {
		if (ev.target == p) {
			p.classList.toggle("closed");
		}
	};
}

function make_file_entry_generic(onclick, name, tooltip, depth) {
	var p = document.createElement("p");
	p.className = "entry file";
	p.style.marginLeft = "-" + (5 + depth*20) + "pt";
	p.style.paddingLeft = (5 + depth*20) + "pt";
	p.onclick = onclick;

	var s = document.createElement("span");
	s.className = "fname";
	s.innerHTML = name;
	s.title = tooltip;
	p.appendChild(s);

	return p;
}

function make_file_entry(self, prefix, f, depth) {
	return make_file_entry_generic(self.make_entry_onclick(prefix + f, true), f, f, depth);
}

//

assets_browser.init();
