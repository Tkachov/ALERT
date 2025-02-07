# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import importlib
import inspect
import os
import os.path

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

import dat1lib.types.dat1
import dat1lib.types.toc
import dat1lib.types.stg
import traceback

def _read_file(fn, method, *args):
	try:
		with open(fn, "rb") as f:
			return method(f, *args)
	except Exception as e:
		print(f"[!] Couldn't read '{fn}'")
		traceback.print_exc()
		return None

def read_dat1(f):
	if isinstance(f, str):
		return _read_file(f, read_dat1)

	return dat1lib.types.dat1.DAT1(f)

def read_toc(f):
	if isinstance(f, str):
		return _read_file(f, read_toc)

	return dat1lib.types.toc.TOC(f)

def read_stg(f, hint=None):
	if isinstance(f, str):
		return _read_file(f, read_stg, hint)

	if hint is not None:
		if hint in types.KNOWN_TYPES:
			return types.KNOWN_TYPES[hint](f)

	return dat1lib.types.stg.STG(f)
