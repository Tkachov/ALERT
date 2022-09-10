var ajax = {};
ajax.x = function () { return new XMLHttpRequest(); };

ajax.send = function (url, callback, errorCallback, method, data, async) {
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
	return ajax.send(url + (query.length ? '?' + query.join('&') : ''), callback, errorCallback, 'GET', null, async)
};

ajax.post = function (url, data, callback, errorCallback, async) {
	var query = [];
	for (var key in data) {
		query.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
	}
	return ajax.send(url, callback, errorCallback, 'POST', query.join('&'), async)
};

ajax.getAndParseJson = function (url, data, callback, errorCallback) {
	return ajax.get(
		url, data,
		function (responseText) {
			try {
				callback(JSON.parse(responseText));
			} catch (e) {
				console.log(e.name+": "+e.message);
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
				console.log(e.name+": "+e.message);
				console.log(responseText);
				if (errorCallback !== undefined) errorCallback(e);
			}
		},
		function (x) { if (errorCallback !== undefined) errorCallback("error: " + x.status); }
	);
};
