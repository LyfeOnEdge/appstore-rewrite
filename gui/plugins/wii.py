from gui.plugins import basePlugin
from gui.widgets import categoryPage
from appstore import Appstore

REPO = "http://brewtools.dev/osc-redist/"
LIBGET_DIR = "wii/apps/appstore/.get/packages"

class Plugin(basePlugin.BasePlugin):
	def __init__(self, app, container):
		basePlugin.BasePlugin.__init__(self, app, "Wii", container)
		self.handler = Appstore("Wii", REPO, LIBGET_DIR)

	def get_pages(self):
		all_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "Wii - All", self.handler.all)
		tools_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "Wii - Tools", self.handler.tools)
		emus_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "Wii - Emus", self.handler.emus)
		games_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "Wii - Games", self.handler.games)
		misc_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "Wii - Misc.", self.handler.misc)
		print("TODO: Reimplement installed_frame in plugins")
		return [all_frame, tools_frame, emus_frame, games_frame, misc_frame]

	def exit(self):
		pass

def setup(app, container):
	return Plugin(app, container)