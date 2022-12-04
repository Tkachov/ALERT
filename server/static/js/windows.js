windows = {
	ready: false,

	start_button: null,
	bar_dom: null,

	windows: [],
	focused: null,
	free_window_id: 1,

	init: function () {
		this.ready = true;

		this.make_bar_dom();

		var wnd = {
			title: "Assets Browser",
			button_title: "Assets Browser",
			element: document.getElementById("main_window"),
			button: null,
			z: -1,
			wid: 0
		};
		this.make_window_button(wnd);
		this.windows.push(wnd);
		wnd.button.click();
	},

	make_bar_dom: function () {
		var e = document.getElementById("windows_bar");
		e.innerHTML = "";

		var b = document.createElement("div");
		b.className = "window_button start_button";
		b.onclick = this.toggle_start_menu.bind(this);
		e.appendChild(b);
		this.start_button = b;

		// TODO: left/right scrolling buttons here?

		var d = document.createElement("div");
		d.className = "windows_bar_contents";
		e.appendChild(d);
		this.bar_dom = d;

		//

		var self = this;
		e = document.getElementById("start_menu");
		e.onclick = function (ev) { if (ev.target == e) self.hide_start_menu(); };
	},

	toggle_start_menu: function () {
		var e = document.getElementById("start_menu");

		if (e.classList.contains("animation_show") || e.classList.contains("animation_hide"))
			return;
		
		if (e.classList.contains("open")) {
			this.start_button.classList.remove("selected");
			e.classList.add("animation_hide");
			setTimeout(function () {
				e.classList.remove("open");
				e.classList.remove("animation_hide");
			}, 250);
		} else {
			this.start_button.classList.add("selected");
			e.classList.add("open");
			e.classList.add("animation_show");
			setTimeout(function () {
				e.classList.remove("animation_show");
			}, 250);
		}
	},

	hide_start_menu: function () {
		var e = document.getElementById("start_menu");
		if (e.classList.contains("open"))
			this.toggle_start_menu();
	},

	//

	new_window: function (title, button_title) {
		button_title = button_title || title;

		var w = document.createElement("div");
		w.className = "window";

		var h = document.createElement("div");
		h.className = "window_header";
		h.appendChild(createElementWithTextNode("span", title));
		w.appendChild(h);

		var c = document.createElement("div");
		c.className = "window_contents";
		w.appendChild(c);

		var e = document.getElementById("windows");
		e.appendChild(w);

		var wnd = {
			title: title,
			button_title: button_title,
			element: w,
			button: null,
			z: -1,
			wid: this.free_window_id
		};
		this.free_window_id += 1;
		this.make_window_button(wnd);
		this.windows.push(wnd);
		wnd.button.click();

		// `float: right` buttons

		var self = this;
		var b = document.createElement("div");
		b.className = "window_header_button close";
		b.onclick = function () { self.close_window(wnd); };
		h.appendChild(b);

		b = document.createElement("div");
		b.className = "window_header_button minimize";
		b.onclick = function () { self.minimize_window(wnd); };
		h.appendChild(b);

		return c;
	},

	make_window_button: function (wnd) {
		var self = this;
		var b = document.createElement("div");
		b.className = "window_button";
		b.appendChild(createElementWithTextNode("span", wnd.button_title));
		b.onclick = function () { self.toggle_window_focus(wnd); };
		b.title = wnd.button_title;
		wnd.button = b;

		this.bar_dom.appendChild(b);
	},

	toggle_window_focus: function (wnd) {
		wnd.z = (this.focused == wnd ? -1 : this.windows.length + 10);
		this.refresh_focus();
	},

	minimize_window: function (wnd) {
		wnd.z = -1;
		this.refresh_focus();
	},

	close_window: function (wnd) {
		wnd.element.parentNode.removeChild(wnd.element);
		wnd.button.parentNode.removeChild(wnd.button);
		this.windows.splice(this.windows.indexOf(wnd), 1);
		this.refresh_focus();
	},

	refresh_focus: function () {
		this.hide_start_menu();

		var new_focused = null;
		var windows_zordered = this.windows.slice();
		windows_zordered.sort((a, b) => {
			if (a.z == b.z) {
				return a.wid - b.wid;
			}

			return b.z - a.z;
		});
		
		var max_z = -1;
		for (var w of this.windows) {
			if (w.z > max_z) {
				new_focused = w;
				max_z = w.z;
			}
		}

		//

		if (new_focused == null) {
			new_focused = this.windows[this.windows.length > 1 ? 1 : 0];
		}

		if (new_focused != null) {
			this.focused = new_focused;

			//

			var new_z = this.windows.length + 1;
			var new_zs = {};
			new_zs[this.focused.wid] = new_z;
			new_z -= 1;

			for (var w of windows_zordered) {
				if (w.element == new_focused.element) continue;
				if (w.z == -1) {
					new_zs[w.wid] = -1;
					continue;
				}

				new_zs[w.wid] = new_z;
				new_z -= 1;
			}

			for (var w of this.windows) {
				w.z = new_zs[w.wid];
			}
		}

		//

		var e = document.getElementById("windows");
		for (var w of this.windows) {
			if (w.element.parentNode != e) {
				// special case, non-collapsible
				continue;
			}

			var is_collapsed = (w.z == -1);
			var is_selected = (w == this.focused);

			w.element.style.display = (is_collapsed ? "none" : "flex");
			w.element.style.zIndex = w.z;
			if (is_selected) w.element.classList.add("selected");
			else w.element.classList.remove("selected");
		}

		//

		var e = this.bar_dom;
		for (var c of e.children) {
			if (new_focused != null && c == new_focused.button) {
				c.classList.add("selected");
				c.scrollIntoView({behavior: "smooth", inline: "center"});
			} else {
				c.classList.remove("selected");
			}
		}

		var has_scrollbar = (e.scrollWidth > e.clientWidth);
		e = document.getElementById("windows_bar");
		classListSetIf(e, "has_scrollbar", has_scrollbar);
		classListSetIf(e, "sliding_scrollbar", controller.user.__windows_bar_sliding_scrollbar);
		e.style.zIndex = this.windows.length + 15; // above topmost window

		e = document.getElementById("start_menu");
		classListSetIf(e, "has_scrollbar", has_scrollbar);
	},

	//

	open_smpcmod_importer: function () {
		smpcmod_importer.show_importer();
		this.hide_start_menu();
	},

	open_suits_editor: function () {
		suits_editor.show_editor(); // TODO: open in current stage
		this.hide_start_menu();
	},

	open_suit_importer: function () {
		suit_importer.show_importer();
		this.hide_start_menu();
	}
};

windows.init();
