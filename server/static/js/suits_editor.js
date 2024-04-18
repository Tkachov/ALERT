// ALERT: Amazing Luna Engine Research Tools
// This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
// For more details, terms and conditions, see GNU General Public License.
// A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

const BUILTIN_SUITS = ["SUIT_I20","SUIT_CLASSIC_DAMAGED","SUIT_CLASSIC","SUIT_NOIR","SUIT_SCARLET","SUIT_MK2","SUIT_SECRETWAR","SUIT_MCU","SUIT_NEGATIVEZONE","SUIT_ELECTRO","SUIT_PUNK","SUIT_WRESTLER","SUIT_FEARITSELF","SUIT_STEALTH","SUIT_MK3","SUIT_2099","SUIT_IRON","SUIT_ADI","SUIT_MK4","SUIT_SPIRIT","SUIT_2099_WHITE","SUIT_VINTAGE","SUIT_FINAL","SUIT_NAKED","SUIT_MAKESHIFT","SUIT_CASUAL","SUIT_ANTIOCK","SUIT_BLACK","SUIT_RESILIENT","SUIT_UK","SUIT_SCARLET2","SUIT_MK1","SUIT_IRONSPIDER","SUIT_SPIDERCLAN","SUIT_AIKMAN","SUIT_CYBORG","SUIT_SPIDERVERSE","SUIT_WEBBED","SUIT_BAGMAN","SUIT_FUTUREFOUNDATION","SUIT_UPGRADED","SUIT_FFHSTEALTH","SUIT_AMAZING","SUIT_ARACHNIDRIDER","SUIT_I20RTHIRD","SUIT_NWH","SUIT_NWHBLACK"];

suits_editor = {
	ready: false,

	init: function () {
		this.ready = true;
	},

	construct_editor: function () {
		return {
			stage: null,
			info: null,
			container: null,

			preview_dom: null,
			controls_dom: null,
			suit_details_dom: null,

			selected_suit: null,
			display_default_suits: true,
			refreshing_icons: false,

			init: function (stage, info) {
				this.stage = stage;
				this.info = info;
				this.edited = null;

				var title = "Suits Editor";
				var e = windows.new_window(title, title);
				e.classList.add("suits_editor");
				this.container = e;

				this.render();
			},

			render: function () {
				var self = this;
				var e = this.container;
				e.innerHTML = "";

				var d = document.createElement("div");
				e.appendChild(d);

				var preview = document.createElement("div");
				preview.className = "preview" + (this.display_default_suits ? "" : " no_builtins");
				d.appendChild(preview);
				this.preview_dom = preview;

				var controls = document.createElement("div");
				controls.className = "controls";
				d.appendChild(controls);
				this.controls_dom = controls;

				function normalize_path(path) {
					return path.toLowerCase().replaceAll('\\', '/');
				}

				var references = {};
				for (var r of this.info.references) {
					var aid = r[0];
					var path = r[1];
					references[normalize_path(path)] = aid;
				}

				function make_suit_onclick(self, i) {
					return function () {
						self.change_selected_suit(i);
					};
				}

				var suits_count = this.info.suits.length;
				for (var i=0; i<suits_count; ++i) {
					var s = this.info.suits[i];
					var suit_button = document.createElement("img");
					suit_button.className = "suit" + (i == this.selected_suit ? " selected" : "") + (BUILTIN_SUITS.includes(s.Name) ? " builtin" : "");
					suit_button.src = "/api/suits_editor/icon?stage=" + this.stage + "&aid=" + references[normalize_path(s.PreviewImage)] + "#" + Date.now();
					suit_button.onclick = make_suit_onclick(this, i);
					preview.appendChild(suit_button);
				}

				var ab = document.createElement("img");
				ab.className = "suit add_button";
				ab.src = "/img/add_button.png";
				preview.appendChild(ab);
				ab.onclick = function () { self.show_adding_popup(); };

				// controls column

				this.render_details();

				var bottom_pane = document.createElement("div");
				bottom_pane.className = "bottom_pane";
				controls.appendChild(bottom_pane);

				bottom_pane.appendChild(createElementWithTextNode("p", this.info.suits.length + " suits"));

				{
					var cb_id = "display_suits_" + Date.now();

					var cb = document.createElement("input");
					cb.type = "checkbox";
					cb.name = "display_suits";
					cb.id = cb_id;
					cb.checked = (this.display_default_suits);
					cb.onchange = function () {
						self.display_default_suits = cb.checked;
						if (self.display_default_suits)
							self.preview_dom.classList.remove("no_builtins");
						else
							self.preview_dom.classList.add("no_builtins");
					};

					var lb = createElementWithTextNode("label", "Display built-in suits");
					lb.htmlFor = cb_id;

					var p = document.createElement("p");
					p.className = "checkbox_line";
					p.appendChild(cb);
					p.appendChild(lb);
					bottom_pane.appendChild(p);
				}

				var refresh_button = createElementWithTextNode("button", "Refresh icons");
				refresh_button.disabled = (this.refreshing_icons);
				refresh_button.style.marginTop = "auto";
				refresh_button.onclick = function () {
					refresh_button.disabled = true;
					self.refresh_icons();
				};
				bottom_pane.appendChild(refresh_button);
			},

			change_selected_suit: function (index) {
				if (this.preview_dom == null) return;

				if (this.selected_suit != null) {
					this.preview_dom.children[this.selected_suit].classList.remove("selected");
				}

				this.selected_suit = index;
				this.preview_dom.children[this.selected_suit].classList.add("selected");

				this.render_details();
			},

			render_details: function () {
				if (this.details_dom == null) {
					this.details_dom = document.createElement("div");
				}

				if (this.details_dom.parentNode != this.controls_dom) {
					this.controls_dom.appendChild(this.details_dom);
				}

				var e = this.details_dom;
				e.innerHTML = "";

				if (this.selected_suit == null || this.selected_suit < 0 || this.selected_suit >= this.info.suits.length)
					return;

				var s = this.info.suits[this.selected_suit];
				var p = document.createElement("p");
				e.appendChild(p);
				p.appendChild(createElementWithTextNode("b", s.Name));

				if (s.hasOwnProperty("GivesItems")) {
					p = createElementWithTextNode("p", "Gives:");
					if (is_array(s.GivesItems)) {
						for (var g of s.GivesItems) {
							p.appendChild(document.createElement("br"));
							p.appendChild(document.createTextNode(g.Item));
						}
					} else {
						p.appendChild(document.createElement("br"));
						p.appendChild(document.createTextNode(s.GivesItems.Item));
					}
					e.appendChild(p);
				}
			},

			show_adding_popup: function () {
				var popup = {
					dom: null,
					input_dom: null,

					sending: false,
					sent_success: false,
					log: "",

					init: function (container) {
						var d = document.createElement("div");
						d.className = "popup";
						container.appendChild(d);
						this.dom = d;

						this.render();
					},

					render: function () {
						var closable = (!this.sending && !this.sent_success);
						var self = this;

						var d = this.dom;
						d.innerHTML = "";
						if (closable)
							d.onclick = function (ev) { if (ev.target == d) d.parentNode.removeChild(d); };
						else
							d.onclick = function () {};

						var d2 = document.createElement("div");
						d2.className = "install_suit";
						d.appendChild(d2);

						{
							var f = document.createElement("div");
							f.className = "install_form";
							d2.appendChild(f);

							var h = createElementWithTextNode("b", "Install suit");
							f.appendChild(h);

							if (this.input_dom == null) {
								var input = document.createElement("input");
								input.type = "file";
								input.name = "suit";
								this.input_dom = input;
							}
							this.input_dom.disabled = (!closable);
							f.appendChild(this.input_dom);

							if (this.sent_success) {
								f.appendChild(createElementWithTextNode("span", "Installed!"));
							} else {
								var b = createElementWithTextNode("button", "Install");
								b.disabled = (this.sending);
								f.appendChild(b);
								b.onclick = function () { self.install_suit(); };
							}
						}

						if (this.sent_success) {
							var f = document.createElement("div");
							f.className = "post_install";
							d2.appendChild(f);

							var t = document.createElement("textarea");
							t.readonly = "";
							t.disabled = "";
							t.value = this.log;
							f.appendChild(t);

							var b = createElementWithTextNode("button", "Reload");
							f.appendChild(b);
							b.onclick = function () { document.location = ""; };
						}
					},

					install_suit: function () {
						this.sending = true;

						var input = this.input_dom;
						var form_data = new FormData();
						form_data.set(input.name, input.files[0]);
						form_data.set("stage", this.stage);

						var self = this;
						ajax.postFormAndParseJson(
							"api/suits_editor/install_suit", form_data,
							function(r) {
								self.sending = false;
								self.sent_success = false;

								if (r.error) {
									// TODO: self.editor.search.error = r.message;
									return;
								}

								// TODO: self.editor.search.error = null;
								self.sent_success = true;
								self.log = r.log;
								self.render();
							},
							function(e) {				
								// TODO: self.editor.search.error = e;
								self.sending = false;
								self.sent_success = false;
								self.render();
							}
						);

						this.render();
					}
				};
				popup.init(this.container);
			},

			//

			refresh_icons: function () {
				var self = this;
				self.refreshing_icons = true;
				ajax.postAndParseJson(
					"api/suits_editor/refresh_icons", { stage: this.stage },
					function(r) {
						if (r.error) {
							// TODO: self.editor.search.error = r.message;
							return;
						}

						// TODO: self.editor.search.error = null;
						self.refreshing_icons = false;
						self.render();
					},
					function(e) {				
						// TODO: self.editor.search.error = e;
					}
				);
			}
		};
	},

	show_editor: function (stage) {
		var self = this;
		ajax.postAndParseJson(
			"api/suits_editor/make", { stage: stage },
			function(r) {
				if (r.error) {
					// TODO: self.editor.search.error = r.message;
					return;
				}

				// TODO: self.editor.search.error = null;
				var e = self.construct_editor();
				e.init(stage, r);
			},
			function(e) {				
				// TODO: self.editor.search.error = e;
			}
		);
	}
};

suits_editor.init();
