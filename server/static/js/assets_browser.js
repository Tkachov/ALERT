assets_browser = {
	ready: false,

	toc: null,
	assets: new Map(),
	assets_info: new Map(),
	stages: [],
	trees: {}, // "stage" => {tree}

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

	toc_loaded: function (toc, stages) {
		this.toc = toc;
		this.fill_structs(stages);
		this.make_directories_tree();
		this.select_entry("", "", true);
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

		if (this.search.results.length > 0) {
			var t = document.createElement("table");

			var tr = document.createElement("tr");
			tr.appendChild(createElementWithTextNode("th", "Name"));
			tr.appendChild(createElementWithTextNode("th", "Stage"));
			tr.appendChild(createElementWithTextNode("th", "Span"));
			tr.appendChild(createElementWithTextNode("th", "Size"));
			t.appendChild(tr);

			for (var r of this.search.results) {
				t.appendChild(this.make_search_result(t, r));
			}

			e.appendChild(t);
		}
	},

	/* search */

	_get_archive_name: function (arch) {
		return this.toc.archives_map[arch].replaceAll("\x00", "");
	},

	make_search_result: function (container, r) {
		var tr = document.createElement("tr");
		tr.className = "result_entry";
		tr.title = r.aid + (r.path != "" ? " - " + r.path : "");

		var stage = "";
		var span = "";
		if (r.stage == "") {
			stage = "Game Archive: " + this._get_archive_name(r.archive);
			span = "#" + r.span;
		} else {
			stage = r.stage;
			span = r.span;
		}

		tr.appendChild(createElementWithTextNode("td", r.name));
		tr.appendChild(createElementWithTextNode("td", stage));
		tr.appendChild(createElementWithTextNode("td", span));
		tr.appendChild(createElementWithTextNode("td", filesize(r.size)));

		var self = this;
		tr.onclick = function () {
			self.change_selected(container, tr);
			self.make_asset_details(r);
			if (r.path != "") self.select_entry(r.stage, r.path, false);
			else {
				controller.remember_in_history(r.aid);
				self.refresh_collapsible_selection(r.aid);
			}
		}

		return tr;
	},

	change_selected: function (container, e) {
		for (var c of container.children) {
			if (c == e) c.classList.add("selected");
			else c.classList.remove("selected");
		}
		e.classList.add("selected");
	},

	/* details tab */

	make_directory_details: function (entry) {
		var e = document.getElementById("details");
		e.innerHTML = "";

		var path = (entry.stage == "" ? "Game Archive" : entry.stage) + (entry.path == "" ? "" : ": ") + entry.path;
		e.appendChild(createElementWithTextNode("b", path));

		if (entry.stage == "" && entry.path == "") {
			e.appendChild(createElementWithTextNode("p", this.toc.archives + " archives, " + this.toc.assets + " assets"));
		}

		//

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

		var message = "";
		if (directories.length > 0) message += directories.length + " directories";
		if (files.length > 0) {
			if (message != "") message += ", ";
			message += files.length + " assets";
		}
		if (message == "") message = "Empty";
		e.appendChild(createElementWithTextNode("p", message));

		//

		e.appendChild(document.createElement("hr"));

		var game_archives_actions = false;
		var stage_actions = false;
		var archived_directory_actions = false;
		var staged_directory_actions = false;

		if (entry.path == "") {
			if (entry.stage == "") {
				game_archives_actions = true;
			} else {
				stage_actions = true;
			}
		} else {
			if (entry.stage == "") {
				archived_directory_actions = true;
			} else {
				staged_directory_actions = true;
			}
		}

		var self = this;
		var links = document.createElement("p");
		links.className = "links";

		if (game_archives_actions) {
			// none yet
		}

		if (stage_actions) {
			// open in explorer
			{
				var btn = createElementWithTextNode("a", "Show in Explorer");
				btn.onclick = function () {
					self.open_explorer(entry.stage, "");
				};
				links.appendChild(btn);
			}

			// install as mod
		}

		if (archived_directory_actions) {
			// stage all files
			{
				var btn = createElementWithTextNode("a", "Add to stage...");
				btn.onclick = function () {
					stage_selector.show_selector(entry.path, "", entry.path, true);
				};
				links.appendChild(btn);
			}

			// stage recursively?
		}

		if (staged_directory_actions) {
			// open in explorer
			{
				var btn = createElementWithTextNode("a", "Show in Explorer");
				btn.onclick = function () {
					self.open_explorer(entry.stage, entry.path);
				};
				links.appendChild(btn);
			}
		}

		e.appendChild(links);
	},

	make_asset_details: function (entry) {
		var e = document.getElementById("details");
		e.innerHTML = "";

		e.appendChild(createElementWithTextNode("b", entry.name));

		// asset location info
		
		var pathline = "";
		pathline += (entry.stage == "" ? "Game Archive" : entry.stage) + " ("
		if (entry.stage == "") {
			pathline += this._get_archive_name(entry.archive);
			pathline += ", ";
		}
		pathline += "span " + (entry.stage == "" ? ("#" + entry.span) : entry.span);
		pathline += ")";

		if (entry.path != "") {
			pathline += ":";
		}

		var p = document.createElement("p");
		p.appendChild(document.createTextNode(pathline));
		if (entry.path != "") {
			p.appendChild(document.createElement("br"));
			p.appendChild(document.createTextNode(entry.path));
		}
		// TODO: if current_stage != "", and this asset is staged, display that here
		e.appendChild(p);

		if (entry.path != "") {
			e.appendChild(createElementWithTextNode("span", entry.aid));
		}

		//

		function get_asset_names(self) {
			// TODO: correct name for staged file
			var shortname = entry.name;
			var fullname = entry.name;
			if (entry.path != "")
				fullname = entry.path;
			fullname += " (" + self._get_archive_name(entry.archive) + ")";
			return [shortname, fullname];
		}

		var locator = "/" + entry.span + "/" + entry.aid;
		if (entry.stage != "") {
			locator = entry.stage + "/" + entry.span + "/" + entry.path;
		}

		if (this.assets.has(locator)) {
			var info = this.assets.get(locator);

			e.appendChild(document.createElement("hr"));
			var desc = "";
			var links = document.createElement("p");
			links.className = "links";

			// generic
			desc = filesize(entry.size);

			{
				var btn = createElementWithTextNode("a", "Save as...");
				btn.href = "/api/assets/asset?locator=" + locator;
				btn.target = "_blank";
				links.appendChild(btn);
			}

			if (entry.stage != "") {
				var btn = createElementWithTextNode("a", "Show in Explorer");
				btn.onclick = function () {
					self.open_explorer(entry.stage, entry.path, entry.span);
				};
				links.appendChild(btn);
			}

			if (entry.stage == "") {
				var btn = createElementWithTextNode("a", "Add to stage...");
				btn.onclick = function () {
					let [shortname, fullname] = get_asset_names(self);
					stage_selector.show_selector(locator, shortname, fullname, false);
				};
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
					var btn = createElementWithTextNode("a", "View sections");
					links.appendChild(btn);
					btn.onclick = function () {
						let [shortname, fullname] = get_asset_names(self);
						sections_viewer.show_viewer(locator, shortname, fullname);
					};
				}

				{
					var btn = createElementWithTextNode("a", "Edit sections");
					links.appendChild(btn);
					btn.onclick = function () {
						let [shortname, fullname] = get_asset_names(self);
						sections_editor.show_editor(locator, shortname, fullname);
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
					configs_editor.show_editor(locator, shortname, fullname);
				};
			}

			// configs/system/system_progression.config
			if (entry.aid == "9C9C72A303FCFA30") {
				var sep = document.createElement("span");
				sep.className = "separator";
				links.appendChild(sep);

				var btn = createElementWithTextNode("a", "Edit suits");
				links.appendChild(btn);
				btn.onclick = function () {
					suits_editor.show_editor(""); // TODO: stage
				};
			}

			// model
			if (info.type == "Model" || info.type == "Model2") {
				var sep = document.createElement("span");
				sep.className = "separator";
				links.appendChild(sep);

				var btn = createElementWithTextNode("a", "View");
				links.appendChild(btn);
				var self = this;
				btn.onclick = function () {
					let [shortname, fullname] = get_asset_names(self);
					models_viewer.show_mesh("/api/models_viewer/obj?locator=" + locator, shortname, fullname);
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
					textures_viewer.show_texture(locator, shortname, fullname);
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
				locator,
				function () { self.make_asset_details(entry); },
				function (error_message) {
					e.appendChild(document.createElement("hr"));
					e.appendChild(createElementWithTextNode("b", error_message));
				}
			);
		}
	},

	/* directories tree / content browser */

	make_info_entry: function (stage, path, info) {
		var vars = [];
		for (var o of info) {
			vars.push({
				stage: stage,
				span: o[0],
				archive: o[1],
				size: o[2]
			});
		};		
		return {
			path: path,
			variants: vars
		};
	},

	traverse_tree: function (stage, tree, current_path) {
		if (current_path == "") {
			this.trees[stage] = tree;
		}

		for (var k in tree) {
			if (is_array(tree[k])) {
				var info = this.make_info_entry(stage, current_path + k, tree[k][1]);
				if (!this.assets_info.has(tree[k][0])) {
					this.assets_info.set(tree[k][0], info);
				} else {
					var old_info = this.assets_info.get(tree[k][0]);
					if (old_info.path == "") old_info = info.path;
					for (var v of info.variants)
						old_info.variants.push(v);
				}
			} else {
				this.traverse_tree(stage, tree[k], current_path + k + "/");
			}
		}
	},

	fill_structs: function (stages) {
		this.assets_info = new Map();
		this.stages = [];
		this.trees = {};

		for (var k in this.toc.assets_map) {
			this.assets_info.set(k, this.make_info_entry("", "", this.toc.assets_map[k]));
		}
		this.traverse_tree("", this.toc.tree, "");
		for (var s in stages) {
			this.traverse_tree(s, stages[s].tree, "");
			this.stages.push(s);
		}
	},

	get_crumbs: function (path) {
		return path.split("/");
	},

	get_basename: function (path) {
		var c = this.get_crumbs(path);
		return c[c.length - 1];
	},

	get_entry_info: function (stage, path) {
		var result = {
			path: path,
			tree_node: null,
			crumbs: [],
			is_file: false,
			aid: "",
			basedir: "",
			thumbnails_info: null,
			stage: stage
		};

		if (path != "") result.crumbs = path.split("/");

		result.tree_node = this.trees[stage];
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

	select_entry: function (stage, path, update_search) {
		this.make_entry_onclick(stage, path, update_search)();
	},

	make_entry_onclick: function (stage, path, update_search) {
		var self = this;
		return function (ev) {
			var e = self.get_entry_info(stage, path);
			self.make_content_browser(e);
			self.select_tree_node(e);

			if (e.is_file) {
				if (update_search) {
					self.make_asset_search_callback(e.aid, stage)();
				}

				controller.remember_in_history(e.aid);
				self.refresh_history_entries();
			} else {
				self.make_directory_details(e);

				// deselect all search results, as none of these can be a directory, so .selected
				// might confuse user when everything else (tree, browser, details) show directory selected
				var container = document.querySelector("#results > table");
				if (container != null) {
					for (var c of container.children) {
						c.classList.remove("selected");
					}
				}
			}
		};
	},

	make_asset_search_callback: function (aid, stage_hint) {
		var self = this;
		return function () {
			var s = document.getElementById("search");
			s.value = aid;
			self.search_assets(stage_hint);
		};
	},

	_browser_made_for_entry: null,
	_browser_thumbnails_path: null,
	_browser_known_thumbnails: new Set(),

	make_content_browser: function (entry) {
		var remake_browser = true;
		if (this._browser_made_for_entry != null && this._browser_made_for_entry.basedir == entry.basedir && this._browser_made_for_entry.stage == entry.stage) {
			remake_browser = false;
		}

		this._browser_made_for_entry = entry;

		if (remake_browser) {
			var stage = entry.stage;

			var e = document.getElementById("browser");
			e.innerHTML = "";

			var crumbs = document.createElement("div");
			crumbs.className = "breadcrumbs";

			function add_breadcrumb(parent, self, stage, full_path, crumb) {
				if (parent.children.length > 0) {
					var sep = document.createElement("span");
					sep.className = "separator";
					parent.appendChild(sep);
				}

				var b = createElementWithTextNode("span", crumb);
				b.className = "breadcrumb";
				b.onclick = self.make_entry_onclick(stage, full_path, true);
				parent.appendChild(b);
			}

			var self = this;
			add_breadcrumb(crumbs, self, stage, "", stage == "" ? "home" : stage);

			var full_path = "";
			var len = entry.crumbs.length - (entry.is_file ? 1 : 0);
			if (len > 0) {		
				for (var i=0; i<len; ++i) {
					var p = entry.crumbs[i];
					full_path += p;
					add_breadcrumb(crumbs, self, stage, full_path, p);
					full_path += "/";
				}
			}

			if (this._browser_thumbnails_path != entry.basedir) {
				this._browser_thumbnails_path = entry.basedir;

				var self = this;
				ajax.postAndParseJson(
					"api/thumbnails/list", {
						stage: stage,
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
							if (self._browser_made_for_entry != null && self._browser_made_for_entry.basedir == entry.basedir && self._browser_made_for_entry.stage == entry.stage) {
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
				item.onclick = this.make_entry_onclick(stage, entry.basedir + d, true);
				folder.appendChild(item);
			}

			var is_multiple;
			for (var f of files) {
				is_multiple = (entry.tree_node[f][1].length > 1);
				var item = document.createElement("span");
				item.className = "file" + (is_multiple ? " multiple" : "");
				item.appendChild(createElementWithTextNode("span", f));
				item.onclick = this.make_entry_onclick(stage, entry.basedir + f, true);

				var aid = entry.tree_node[f][0];
				var taid = entry.stage + "_" + aid;
				if (this._browser_known_thumbnails.has(taid)) {
					var thumb = document.createElement("img");
					thumb.src = "/api/thumbnails/png?stage=" + entry.stage + "&aid=" + aid;
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

		var stages_headers = document.getElementById("left_column").querySelectorAll(".directories_tree .entry[data-stage]");

		var stage_header = null;
		for (var sh of stages_headers) {
			if (sh.dataset.stage == e.stage) {
				stage_header = sh;
				break;
			}
		}

		var n = stage_header;
		if (e.path != "") {
			var next = n.nextSibling;
			for (var c of e.crumbs) {
				n.classList.remove("closed");
				n = next;
				for (var i=0; i<n.children.length; ++i) {
					if (n.children[i].innerText == c) {
						if (n.children[i].classList.contains("directory"))
							next = n.children[i+1];
						
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

	make_stages_directories_tree: function () {
		var e = document.getElementById("left_column");
		var d2 = e.querySelector(".directories_tree > div");

		var container;
		e = document.getElementById("stages_tree");
		if (e == null) {
			let [stages_spoiler, stages_contents] = make_directory_element(d2, "Stages", "Stages", null, 0);
			stages_spoiler.classList.add("special");
			stages_spoiler.classList.remove("closed");
			stages_spoiler.id = "stages_tree";

			var refresh_button = createElementWithTextNode("a", "Refresh");
			refresh_button.className = "refresh_button";
			refresh_button.onclick = this.refresh_stages.bind(this);
			stages_spoiler.children[0].appendChild(refresh_button);

			container = stages_contents;
		} else {
			container = e.nextSibling;
			container.innerHTML = "";
		}

		for (var stage of this.stages) {
			let [stage_dir, stage_contents] = make_directory_element(container, stage, stage, this.make_entry_onclick(stage, "", false), 0);
			stage_dir.dataset.stage = stage;
			build_tree(this, stage_contents, this.trees[stage], stage, "", 1);
		}
	},

	make_directories_tree: function () {
		var e = document.getElementById("left_column");
		e.innerHTML = "";

		var d = document.createElement("div");
		d.className = "directories_tree";
		e.appendChild(d);

		var d2 = document.createElement("div");
		d.appendChild(d2);

		// stages

		this.make_stages_directories_tree();

		// archived

		let [home_spoiler, home_contents] = make_directory_element(d2, "Game Archive", "Game Archive", this.make_entry_onclick("", "", false), 0);
		home_spoiler.classList.add("special");
		home_spoiler.classList.remove("closed");
		home_spoiler.dataset.stage = "";
		build_tree(this, home_contents, this.trees[""], "", "", 0);

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
				if (!this.assets_info.has(aid)) continue;

				var info = this.assets_info.get(aid);
				var filepath = info.path;
				var filename = aid;
				var onclick = this.make_asset_search_callback(aid, "");
				
				if (filepath == "") {
					filepath = aid;
				} else {
					filename = this.get_basename(filepath);
				}

				make_file_element(c, filename, filepath, onclick, 0);
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

	search_assets: function (stage_hint) {
		var e = document.getElementById("search");
		var v = e.value;

		function add_results(self, array, aid, info) {
			function get_basename(path) {
				var i1 = path.lastIndexOf('/');
				var i2 = path.lastIndexOf('\\');
				return path.substr(Math.max(i1, i2) + 1);
			}

			var basename = aid;
			var path = "";
			if (info.path != "") {
				basename = get_basename(info.path);
				path = info.path;
			}

			for (var v of info.variants)
				array.push({aid: aid, span: v.span, archive: v.archive, size: v.size, name: basename, path: path, stage: v.stage});
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

			if (this.assets_info.has(v)) {
				add_results(this, this.search.results, v, this.assets_info.get(v));
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

				if (terms.length > 0) {
					for (let [k, info] of this.assets_info.entries()) {
						if ((hexonly && meets_request(k.toLowerCase(), terms)) || (info.path != "" && meets_request(info.path, terms)))
							add_results(this, this.search.results, k, info);
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
			var entries = e.querySelectorAll(".result_entry");
			var best_match = null;
			var best_match_stage = null;
			for (var i=0; i<this.search.results.length; ++i) {
				if (i >= entries.length) break;

				var entry = entries[i];
				if (entry == null) continue;

				var entry_stage = this.search.results[i].stage;
				if (best_match == null || (best_match_stage != stage_hint && stage_hint == entry_stage)) {
					best_match = entry;
					best_match_stage = entry_stage;

					if (best_match_stage == stage_hint) break; // can't find a better match according to condition above
				}
			}
			if (best_match != null) best_match.onclick();
		}

		return false; // invalidate form anyways (so it won't refresh the page on submit)
	},

	extract_asset: function (locator, success_cb, failure_cb) {
		var self = this;
		ajax.postAndParseJson(
			"api/assets/get_info", {
				locator: locator
			},
			function(r) {
				if (r.error) {
					// TODO: self.search.error = r.message;
					failure_cb(r.message);
					return;
				}

				// TODO: self.search.error = null;
				self.assets.set(locator, r.asset);
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
	},

	refresh_stages: function () {
		this._refresh_stages(null);
	},

	_refresh_stages: function (entry_select) {
		var self = this;
		ajax.postAndParseJson(
			"api/stages/refresh", {},
			function(r) {
				if (r.error) {
					// TODO: self.search.error = r.message;
					return;
				}

				// TODO: self.search.error = null;
				self.fill_structs(r.stages);
				self.make_stages_directories_tree();

				var search_stage_hint = "";				
				if (self._browser_made_for_entry != null) {
					var old_stage = self._browser_made_for_entry.stage;
					if (old_stage != "") {
						var new_stage = (self.stages.includes(old_stage) ? old_stage : "");
						self.select_entry(new_stage, "", true);
						search_stage_hint = new_stage;
					}
				}

				self.search_assets(search_stage_hint);
				if (entry_select != null) {
					self.select_entry(entry_select.stage, entry_select.path, entry_select.update_search);
				}
			},
			function(e) {				
				// TODO: self.search.error = e;
			}
		);
	},

	open_explorer: function (stage, path, span) {
		var self = this;
		ajax.postAndParseJson(
			"api/stages/open_explorer", {
				stage: stage,
				path: path,
				span: span||""
			},
			function(r) {
				if (r.error) {
					// TODO: self.search.error = r.message;
					return;
				}

				// TODO: self.search.error = null;
			},
			function(e) {				
				// TODO: self.search.error = e;
			}
		);
	}
};

//

function make_directory_element(container, text, title, onclick, depth) {
	var p = document.createElement("p");
	p.className = "entry directory closed";
	p.style.marginLeft = "-" + (5 + depth*20) + "pt";
	p.style.paddingLeft = (5 + depth*20) + "pt";
	p.onclick = function (ev) {
		if (ev.target == p) {
			p.classList.toggle("closed");
		}
	};

	var s = createElementWithTextNode("span", text);
	s.className = "fname";
	s.title = title;
	s.onclick = onclick;
	p.appendChild(s);
	container.appendChild(p);

	var ct = document.createElement("div");
	ct.className = "directory_contents";
	container.appendChild(ct);

	return [p, ct];
}

function make_file_element(container, text, title, onclick, depth) {
	var p = document.createElement("p");
	p.className = "entry file";
	p.style.marginLeft = "-" + (5 + depth*20) + "pt";
	p.style.paddingLeft = (5 + depth*20) + "pt";
	p.onclick = onclick;

	var s = document.createElement("span");
	s.className = "fname";
	s.innerHTML = text;
	s.title = title;
	p.appendChild(s);

	container.appendChild(p);
	return p;
}

//

function build_tree(self, container, tree, stage, prefix, depth=0) {
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

	for (var d of directories) {
		let [p, ct] = make_directory_element(container, d, d, self.make_entry_onclick(stage, prefix + d, true), depth);
		build_tree(self, ct, tree[d], stage, prefix + d + "/", depth+1);
	}

	for (var f of files) {
		make_file_element(container, f, f, self.make_entry_onclick(stage, prefix + f, true), depth);
	}
}

//

assets_browser.init();
