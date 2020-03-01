from gui.plugins import basePlugin
from gui.widgets import categoryPage
from gui.detailPage import DetailPage
import os
from appstore import Appstore
from .fusee_wrapper import fusee_object
import style

#Wrapper to objectify fusee script, passed print function for stdout
fusee = fusee_object(print)

PAYLOAD_REPO = "https://www.brewtools.dev/switch-payloads/"
LIBGET_DIR = ".get/packages"

#payload injector, a subclass of the Appstore/libget handler that
#handles payloads distributed via a libget repo
class PayloadHandler(Appstore):
	def __init__(self, repo_url: str, libget_dir: str):
		Appstore.__init__(self, "rcmPayloads", repo_url, libget_dir)

	def trigger_inject(self, package: dict):
		payload = self.get_payload(package)
		print(payload)
		self.inject_payload(payload)

	def get_payload(self, package: dict):
		if not package["version"] == self.get_package_version(package["name"]): #compare to local version
			#If they don't match, update payload
			self.install_package(package)

		return self.base_install_path + package["binary"]

	def inject_payload(self, payload):
		fusee.inject(payload)
		
class PayloadsPage(categoryPage.CategoryPage):
	def __init__(self, app, container, handler, title : str = "Switch ~ INJECTOR"):
		categoryPage.CategoryPage.__init__(self, app, container, handler, title, handler.all)

	#Redefine to show injector page, which is a subclass of the detail page modifed to inject a payload 
	#Instead of installing a package
	def open_details(self, package: str):
		self.app.injector_page.show(package, self.appstore_handler)
		# self.controller.frames["detailPage"].show(package)

	def configure(self, event = None, force = False):
		if self.picked or force:
			self.rebuild()


class InjectorPage(DetailPage):
	def __init__(self, frame):
		DetailPage.__init__(self, frame)
		self.place(relwidth = 1, relheight = 1)

	def trigger_install(self):
		if self.package:
			self.appstore_handler.trigger_inject(self.package)
			self.reload_function()
		else:
			print("No rcm package specified")

	def update_buttons(self, package):
		#Hides or places the uninstalll button if not installed or installed respectively
		#get_package_entry returns none if no package is found or if the sd path is not set
		if self.appstore_handler.get_package_entry(package["name"]):
			self.column_uninstall_button.place(rely=1,relwidth = 1, x = + style.offset, y = - 1 * (style.buttonsize + style.offset), width = - (3 * style.offset + style.buttonsize), height = style.buttonsize)
			self.column_install_button.settext("INJECT")
		else:
			self.column_uninstall_button.place_forget()
			if self.column_install_button:
				self.column_install_button.settext("DOWNLOAD & INJECT")

class Plugin(basePlugin.BasePlugin):
	def __init__(self, app, container):
		basePlugin.BasePlugin.__init__(self, app, "rcmPlugin", container)
		self.handler = PayloadHandler(PAYLOAD_REPO, LIBGET_DIR)
		self.handler.set_path("tools")
		if not self.handler.check_if_get_init(silent = True):
			self.handler.init_get()

	def get_pages(self):
		injector_page = PayloadsPage(self.app, self.container, self.handler,)
		return [injector_page]

	def exit(self):
		pass

def setup(app, container):
	print("Loading RCM injector...")
	app.injector_page = InjectorPage(app)
	return Plugin(app, container)