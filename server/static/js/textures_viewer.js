// ALERT: Amazing Luna Engine Research Tools
// This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
// For more details, terms and conditions, see GNU General Public License.
// A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

textures_viewer = {
	ready: false,

	init: function () {
		this.ready = true;
	},

	//

	show_texture: function (locator, shortname, fullname) {
		var self = this;
		ajax.postAndParseJson(
			"api/textures_viewer/make", {
				locator: locator
			},
			function(r) {
				if (r.error) {
					// TODO: self.editor.search.error = r.message;
					return;
				}

				// TODO: self.editor.search.error = null;
				self.make_window(locator, r.viewer, shortname, fullname);
			},
			function(e) {				
				// TODO: self.editor.search.error = e;
			}
		);
	},

	make_window: function (locator, info, shortname, fullname) {
		var title = fullname + " — Textures Viewer";
		var button_title = shortname + " — Textures Viewer";
		var e = windows.new_window(title, button_title);
		e.classList.add("textures_viewer");

		var d = document.createElement("div");
		e.appendChild(d);

		var preview = document.createElement("div");
		preview.className = "preview";
		d.appendChild(preview);

		var img = document.createElement("img");
		img.src = "/api/textures_viewer/mipmap?locator=" + locator + "&mipmap_index=0#" + (+Date.now());
		preview.appendChild(img);

		var controls = document.createElement("div");
		controls.className = "controls";
		d.appendChild(controls);

		function make_option(text, value) {
			var o = createElementWithTextNode("option", text);
			o.value = value;
			return o;
		}

		var select = document.createElement("select");
		for (var i=0; i<info.mipmaps.length; ++i) {
			var w = info.mipmaps[i][0];
			var h = info.mipmaps[i][1];
			select.appendChild(make_option(w + " × " + h, i));
		}
		select.selectedIndex = 0;
		if (info.mipmaps.length < 2) select.disabled = true;
		controls.appendChild(select);

		var btn = createElementWithTextNode("a", "Open in new tab");
		btn.target = "_blank";
		btn.href = img.src;
		controls.appendChild(btn);

		select.onchange = function () {
			img.src = "/api/textures_viewer/mipmap?locator=" + locator + "&mipmap_index=" + select.selectedIndex + "#" + (+Date.now());
			btn.href = img.src;
		};
	}
};

textures_viewer.init();
