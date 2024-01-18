import importlib
import inspect
import os
import os.path

VERSION_OVERRIDE = None

VERSION_SO = 201800
VERSION_MSMR = 202200
VERSION_RCRA = 202300

TRY_SECOND_MAGIC = False

#

def __inspect_module(module):
	module_name = module.__name__
	module_dir = os.path.dirname(inspect.getfile(module))
	return (module_name, module_dir)

def __list_submodules(directory):
	result = []

	for m in os.listdir(directory):
		fn = os.path.join(directory, m)
		if m != "__init__.py" and m.endswith(".py") and not os.path.isdir(fn):
			result += [m[:-3]]

	return result

def __import_submodules(module):
	result = []

	mname, mdir = __inspect_module(module)
	for m in __list_submodules(mdir):
		try:
			md = importlib.import_module(mname + "." + m)
			result += [md]
		except:
			pass

	return result

def __list_classes(module):
	result = []

	for name, obj in inspect.getmembers(module):
		if inspect.isclass(obj):
			result += [obj]

	return result

#

import dat1lib.types.sections
types.sections.KNOWN_SECTIONS = {}

def __import_sections(module, directory):
	for m in __list_submodules(directory):
		try:
			md = importlib.import_module(module + "." + m)
			for c in __list_classes(md):
				try:
					if issubclass(c, types.sections.Section):
						types.sections.KNOWN_SECTIONS[c.TAG] = c
				except:
					pass
		except:
			pass

mname, mdir = __inspect_module(types.sections)
for d in os.listdir(mdir):
	subdir = os.path.join(mdir, d)
	if os.path.isdir(subdir):
		__import_sections(mname + "." + d, subdir)

#

import dat1lib.types
types.KNOWN_TYPES = {}

for md in __import_submodules(types):
	for c in __list_classes(md):
		try:
			types.KNOWN_TYPES[c.MAGIC] = c
		except:
			pass

#

import struct
import dat1lib.types.unknown

def read(f, try_unknown=True, version=None):
	magic, = struct.unpack("<I", f.read(4))
	f.seek(0)

	if version is None and VERSION_OVERRIDE is not None:
		version = VERSION_OVERRIDE

	if magic in types.KNOWN_TYPES:
		return types.KNOWN_TYPES[magic](f, version=version)

	if TRY_SECOND_MAGIC:
		try:
			f.seek(36)
			dat1_magic, magic = struct.unpack("<II", f.read(8))
			f.seek(0)

			if dat1_magic == 0x44415431:
				if magic in types.KNOWN_TYPES:
					return types.KNOWN_TYPES[magic](f, version=version)
		except:
			pass

	if try_unknown:
		try:
			obj = types.unknown.UnknownAsset(f, version=version)
			return obj
		except:
			pass

	return None
