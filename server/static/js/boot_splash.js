boot_splash = {
	ready: false,

	loading: false,
	error: null,

	init: function () {
		this.ready = true;

		var e = document.getElementById("toc_path");
		e.value = controller.user.toc_path;
		setTimeout(function () { e.focus(); }, 100);

		this.render();
		this.show();
	},

	localize: function () {
		replaceElementTextById("form_description", controller.get_localized("ui/splashes/boot_splash/form_description"));
		var e = document.getElementById("toc_path");
		e.placeholder = controller.get_localized("ui/splashes/boot_splash/path_placeholder");

		e = document.getElementById("load_toc_form");
		e.onsubmit = this.boot.bind(this);
	},

	render: function () {
		var e = document.getElementById("load_toc");
		e.style.display = (this.loading ? "none" : "block");

		var errmsg = "";
		if (this.error != null) errmsg = this.error;
		e = document.getElementById("load_toc_warning");
		e.innerHTML = "";
		e.appendChild(document.createTextNode(errmsg));

		//

		e = document.getElementById("toc_loading");
		e.style.display = (this.loading ? "block" : "none");
	},

	//

	boot: function () {
		var e = document.getElementById("toc_path");
		var path = e.value;

		controller.remember_toc_path(path);
		this.loading = true;

		var self = this;
		ajax.postAndParseJson(
			"api/boot", {
				toc_path: path
			},
			function(r) {
				self.loading = false;

				if (r.error) {
					self.error = r.message;
					self.render();
					return;
				}

				self.error = null;
				controller.toc_loaded(r.toc, r.stages);
				self.hide();
			},
			function(e) {
				self.loading = false;
				self.error = e;
				self.render();
			}
		);

		this.render();
		return false; // invalidate form anyways (so it won't refresh the page on submit)
	},

	//

	show: function (e) {
		e = e || document.getElementById("boot_splash");
		e.classList.add("open");
	},

	hide: function (e) {
		e = e || document.getElementById("boot_splash");
		e.classList.remove("open");
	}
};

boot_splash.init();
