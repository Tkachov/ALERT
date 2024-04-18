// ALERT: Amazing Luna Engine Research Tools
// This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
// For more details, terms and conditions, see GNU General Public License.
// A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

settings_window = {
	ready: false,

	init: function () {
		this.ready = true;

		var e = document.getElementById("settings_window");
		e.onclick = function (ev) { if (ev.target == e) e.classList.remove("open"); };

		var select = document.getElementById("settings_language_select");
		select.onchange = function () {
			controller.change_locale(select.value);
		};
	},

	localize: function () {
		replaceElementTextById("settings_title", controller.get_localized("ui/settings/title"));

		// language
		replaceElementTextById("settings_language_label", controller.get_localized("ui/settings/language"));
		var select = document.getElementById("settings_language_select");
		for (var ch of select.children)
			replaceElementText(ch, controller.get_localized("ui/settings/language_option_" + ch.value));
		select.value = controller.user.locale;
	},

	//

	show: function (e) {
		e = e || document.getElementById("settings_window");
		e.classList.add("open");
	},

	hide: function (e) {
		e = e || document.getElementById("settings_window");
		e.classList.remove("open");
	},

	toggle: function () {
		var e = document.getElementById("settings_window");
		e.classList.toggle("open");
	}
};

settings_window.init();
