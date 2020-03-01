from gui.plugins import basePlugin
from gui.widgets import categoryPage
from appstore import Appstore

WIIU_REPO = "http://wiiubru.com/appstore/"
LIBGET_DIR = "wiiu/apps/appstore/.get/packages"

class Plugin(basePlugin.BasePlugin):
	def __init__(self, app, container):
		basePlugin.BasePlugin.__init__(self, app, "WiiU", container)
		self.handler = Appstore("WiiU", WIIU_REPO, LIBGET_DIR)

	def get_pages(self):
		all_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "WiiU - All", self.handler.all)
		tools_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "WiiU - Tools", self.handler.tools)
		emus_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "WiiU - Emus", self.handler.emus)
		games_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "WiiU - Games", self.handler.games)
		advanced_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "WiiU - Advanced", self.handler.advanced)
		misc_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "WiiU - Misc.", self.handler.misc)
		print("TODO: Reimplement installed_frame in plugins")
		return [all_frame, tools_frame, emus_frame, games_frame, advanced_frame, misc_frame]

	def exit(self):
		pass

def setup(app, container):
	return Plugin(app, container)