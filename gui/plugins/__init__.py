from os.path import dirname, basename, isfile, join
import glob
import importlib.util

wd = dirname(__file__)
modules = glob.glob(join(wd,"*"))

__plugins__ = []
for m in modules:
	if (isfile(m) and not m.endswith('__init__.py') and not m.endswith('basePlugin.py') and not m.endswith('.md')):
		__plugins__.append(m)
	elif isfile(join(m, "__init__.py")):
		__plugins__.append(join(m, "__init__.py"))
	else:
		print(f"Ingoring plugins folder item {m}")

# __plugins__ = [""]