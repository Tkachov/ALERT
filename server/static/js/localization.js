var localization = {
	get_localized: function (key, locale) {
		locale = locale || BASE_LOCALE;

		var path = key.split('/');
		var directory = ROOT_DIRECTORY;
		for (var i=0; i<path.length; ++i) {
			var level_key = path[i];
			if (!directory.hasOwnProperty(level_key))
				return "{" + key + "}";

			directory = directory[level_key];

			if (directory.hasOwnProperty(locale))
				return directory[locale];
			else if (directory.hasOwnProperty(BASE_LOCALE))
				return directory[BASE_LOCALE];
		}

		return "{" + key + "}";
	},
};

const BASE_LOCALE = "en";
const ROOT_DIRECTORY = {
	"ui": {
		"title": {
			"en": "MSMR Assets Browser"
		},

		"splashes": {
			"boot_splash": {
				"form_description": {
					"en": "Select 'toc' location:"
				},

				"path_placeholder": {
					"en": "asset_archive/toc"
				}
			}
		},

		"editor": {
			"sections_editor": {
				"section_edit_option_keep": {
					"en": "Keep as is"
				},

				"section_edit_option_replace": {
					"en": "Replace raw"
				}
			}
		},

		"settings": {
			"title": {
				"ru": "Настройки",
				"en": "Options"
			},

			"language": {
				"ru": "Язык",
				"en": "Language"
			},

			"language_option_ru": {
				"ru": "русский",
				"en": "Russian"
			},

			"language_option_en": {
				"ru": "английский",
				"en": "English"
			},

			"feature": {
				"ru": "- (бета)",
				"en": "- (experimental)"
			},

			"feature_option_true": {
				"ru": "включено",
				"en": "On"
			},

			"feature_option_false": {
				"ru": "отключено",
				"en": "Off"
			}
		}
	}
};
