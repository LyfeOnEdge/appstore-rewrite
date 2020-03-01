from gui.plugins import basePlugin
from gui.widgets import categoryPage
from appstore import Appstore

SWITCH_REPO = "https://www.switchbru.com/appstore/"
LIBGET_DIR = "switch/appstore/.get/packages"

class Plugin(basePlugin.BasePlugin):
	def __init__(self, app, container):
		basePlugin.BasePlugin.__init__(self, app, "Switch", container)
		self.handler = Appstore("Switch", SWITCH_REPO, LIBGET_DIR)

	def get_pages(self):
		all_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "Switch - All", self.handler.all)
		tools_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "Switch - Tools", self.handler.tools)
		emus_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "Switch - Emus", self.handler.emus)
		games_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "Switch - Games", self.handler.games)
		advanced_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "Switch - Advanced", self.handler.advanced)
		themes_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "Switch - Themes", self.handler.themes)
		legacy_frame = categoryPage.CategoryPage(self.app, self.container, self.handler, "Switch - Legacy", self.handler.legacy)
		print("TODO: Reimplement installed_frame in plugins")
		return [all_frame, tools_frame, emus_frame, games_frame, advanced_frame, themes_frame, legacy_frame]

	def exit(self):
		pass

def setup(app, container):
	return Plugin(app, container)