// DOM

function createElementWithTextNode(tag, text) {
	var e = document.createElement(tag);
	e.appendChild(document.createTextNode(text));
	return e;
}

function replaceElementText(e, t) {
	e.innerHTML = "";
	e.appendChild(document.createTextNode(t));
}

function replaceElementTextById(eid, t) {
	replaceElementText(document.getElementById(eid), t);
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
