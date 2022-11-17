const USER_STORED_FIELDS = ["toc_path", "locale", "history", "favorites", "__configs_editor_enabled", "__hexview_experimental"];
const USER_STORAGE_KEY = "user";

// TODO: make windows title path a link to browse back to the details
// TODO: fix bigger models
// TODO: model viewer materials preview
// TODO: scaleable and moveable windows?
// TODO: localization

var assets_browser = { ready: false };
var configs_editor = { ready: false };
var models_viewer = { ready: false };
var sections_editor = { ready: false };
var sections_viewer = { ready: false };
var settings_window = { ready: false };
var suits_editor = { ready: false };
var textures_viewer = { ready: false };
var windows = { ready: false };

var controller = {
	user: {
		toc_path: "",
		locale: "en",
		history: {
			limit: 10,
			entries: [] // [[asset, timestamp], ...]
		},
		favorites: [],

		__configs_editor_enabled: false,
		__hexview_experimental: {
			enabled: false,
			sections: {}
		}
	},

	init: function () {
		this.load_user();
		this.localize();

		var self = this;
		document.body.onkeyup = function(e) {
			var k = e.keyCode || e.which;
			if (k == 27) { // escape
				self.escape_pressed(e);
			}
		};
	},

	localize: function () {
		document.title = this.get_localized("ui/title");
		document.body.className = "locale_" + this.user.locale;

		if (boot_splash.ready) boot_splash.localize();
		if (settings_window.ready) settings_window.localize();
	},

	// events handling

	toc_loaded: function (toc) {
		assets_browser.toc_loaded(toc);
	},

	escape_pressed: function (e) {
		e.preventDefault();
		// settings_window.toggle();
	},

	// module-to-app requests

	change_locale: function (lang) {
		this.user.locale = lang;
		this.save_user();
		this.localize();
	},

	remember_toc_path: function (path) {
		this.user.toc_path = path;
		this.save_user();
	},

	remember_in_history: function (asset) {
		var entries = this.user.history.entries;
		
		var index = -1;
		for (var i=0; i<entries.length; ++i) {
			if (entries[i][0] == asset) {
				index = i;
				break;
			}
		}

		var timestamp = Date.now();
		if (index == -1) entries.push([asset, timestamp]);
		else entries[index][1] = timestamp;

		entries.sort((a, b) => {
			if (a[1] == b[1]) {
				return a[0].localeCompare(item2.attr);
			}

			return b[1] - a[1];
		});

		if (entries.length > this.user.history.limit)
			entries = entries.slice(0, this.user.history.limit);

		this.user.history.entries = entries;
		this.save_user();
	},

	add_to_favorites: function (asset) {
		if (!this.user.favorites.includes(asset)) {
			this.user.favorites.push(asset);
			this.save_user();
		}
	},

	remove_from_favorites: function (asset) {
		var index = this.user.favorites.indexOf(asset);
		if (index != -1) {
			this.user.favorites.splice(index, 1);
			this.save_user();
		}
	},

	// utils

	get_localized: function (k) {
		return localization.get_localized(k, this.user.locale);
	},

	// save/load

	load_user: function () {
		var v = load_from_storage(USER_STORAGE_KEY);
		if (v == null) return;
		for (var f of USER_STORED_FIELDS) {
			if (v.hasOwnProperty(f))
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

	clear: function () {
		save_into_storage(USER_STORAGE_KEY, {});
		document.location = "";
	}
};

controller.init();
