// ALERT: Amazing Luna Engine Research Tools
// This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
// For more details, terms and conditions, see GNU General Public License.
// A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

var ajax = {};
ajax.x = function () { return new XMLHttpRequest(); };

ajax.send = function (url, callback, errorCallback, method, post_urlencoded, data, async) {
	if (async === undefined) async = true;

	var x = ajax.x();
	x.open(method, url, async);
	x.onreadystatechange = function () {
		if (x.readyState == XMLHttpRequest.DONE) {
			if (x.status == 200)
				callback(x.responseText);
			else
				errorCallback(x);
		}
	};
	if (method == 'POST') {
		if (post_urlencoded)
			x.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	}
	x.send(data);
	return x;
};

ajax.get = function (url, data, callback, errorCallback, async) {
	var query = [];
	for (var key in data) {
		query.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
	}
	return ajax.send(url + (query.length ? '?' + query.join('&') : ''), callback, errorCallback, 'GET', false, null, async)
};

ajax.post = function (url, data, callback, errorCallback, async) {
	var query = [];
	for (var key in data) {
		query.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
	}
	return ajax.send(url, callback, errorCallback, 'POST', true, query.join('&'), async)
};

ajax.postForm = function (url, form_data, callback, errorCallback, async) {
	return ajax.send(url, callback, errorCallback, 'POST', false, form_data, async);
};

ajax.getAndParseJson = function (url, data, callback, errorCallback) {
	return ajax.get(
		url, data,
		function (responseText) {
			try {
				callback(JSON.parse(responseText));
			} catch (e) {
				console.log(e);
				console.log(responseText);
				if (errorCallback !== undefined) errorCallback(e);
			}
		},
		function (x) { if (errorCallback !== undefined) errorCallback("error: " + x.status); },
		true // async
	);
};

ajax.postAndParseJson = function (url, data, callback, errorCallback) {
	return ajax.post(
		url, data,
		function (responseText) {
			try {
				callback(JSON.parse(responseText));
			} catch (e) {
				console.log(e);
				console.log(responseText);
				if (errorCallback !== undefined) errorCallback(e);
			}
		},
		function (x) { if (errorCallback !== undefined) errorCallback("error: " + x.status); }
	);
};

ajax.postFormAndParseJson = function (url, data, callback, errorCallback) {
	return ajax.postForm(
		url, data,
		function (responseText) {
			try {
				callback(JSON.parse(responseText));
			} catch (e) {
				console.log(e);
				console.log(responseText);
				if (errorCallback !== undefined) errorCallback(e);
			}
		},
		function (x) { if (errorCallback !== undefined) errorCallback("error: " + x.status); }
	);
};
