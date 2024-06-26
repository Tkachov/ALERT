// ALERT: Amazing Luna Engine Research Tools
// This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
// For more details, terms and conditions, see GNU General Public License.
// A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

// DOM

function createElementWithTextNode(tag, text) {
	var e = document.createElement(tag);
	e.appendChild(document.createTextNode(text));
	return e;
}

function createElementWithTextNodeAndClass(tag, className, text) {
	var e = createElementWithTextNode(tag, text);
	e.className = className;
	return e;
}

function replaceElementText(e, t) {
	e.innerHTML = "";
	e.appendChild(document.createTextNode(t));
}

function replaceElementTextById(eid, t) {
	replaceElementText(document.getElementById(eid), t);
}

function classListSetIf(e, className, condition) {
	if (condition)
		e.classList.add(className);
	else
		e.classList.remove(className);
}

function isScrolledIntoView(el) {
	var rect = el.getBoundingClientRect();
	var elemTop = rect.top;
	var elemBottom = rect.bottom;

	return (elemTop < window.innerHeight && elemBottom >= 0);
}

// storage

function save_into_storage(key, obj) {
	localStorage[key] = JSON.stringify(obj);
}

function load_from_storage(key) {
	var i = localStorage.getItem(key);
	if (i) return JSON.parse(i);
	return null;
}

// types

function is_string(s) {
	return (typeof s === 'string' || s instanceof String);
}

function is_array(s) {
	return (s != null && s.constructor === Array);
}

function equal_arrays(a, b) {
    return (is_array(a) && is_array(b) && a.length === b.length && a.every((val, index) => val === b[index]));
}

// colors

function hexToLuma(hex) {
	const r = parseInt(hex.substr(0, 2), 16);
	const g = parseInt(hex.substr(2, 2), 16);
	const b = parseInt(hex.substr(4, 2), 16);
	return [0.299 * r, 0.587 * g, 0.114 * b].reduce((a, b) => a + b) / 255;
}

// units

function filesize(sz) {
	var units = "bytes"; // TODO: support localization here
	
	if (sz > 1024) {
		sz = sz / 1024;
		units = "KB";

		if (sz > 1024) {
			sz = sz / 1024;
			units = "MB";

			if (sz > 1024) {
				sz = sz / 1024;
				units = "GB";
			}
		}

		sz = (Math.round(sz * 100) / 100.0);
	}

	return sz + " " + units;
}

// paths

function get_basename(path) {
	var i1 = path.lastIndexOf('/');
	var i2 = path.lastIndexOf('\\');
	return path.substr(Math.max(i1, i2) + 1);
}
