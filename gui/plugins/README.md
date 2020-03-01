Each plugin comes in the form of an object called "Plugin"
At the bottom of the file is a function called "setup"
The setup function is called when the plugin is loaded,
the setup function is passed the tkinter root as a positional argument.
The get_pages function returns a list of pages to add to the side-bar.

Example:
```py
from .basePlugin import BasePlugin 
class Plugin(BasePlugin):
	def __init__(self, app):
		BasePlugin.__init__(self, app)
	#Should return a list of pages subclassed from the BasePage object found in ../widgets/basePage
	#OK to return an empty list if plugin runs in the background
	def get_pages(self):
		pass

	#Exit is called when the app is exited properly, helps to shut down background scripts.
	#TODO: Figure out how to make background threads exit gracefully when exited by bad means
	def exit(self):
		pass

def setup(app):
	app = plugin
	return Plugin(app)
```