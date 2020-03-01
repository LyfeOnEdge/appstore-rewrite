from .appstore import appstore_handler
from .appstore_parser import parser
from .appstore_web import appstore_webhandler
# from .appstore_web import getImage, getPackageIcon, getPackage, getScreenImage

from webhandler import getJson

class Appstore(appstore_handler, parser, appstore_webhandler):
	def __init__(self, handler_name, repo_domain, libget_dir):
		self.name = handler_name
		self.repo_domain = repo_domain
		self.libget_dir = libget_dir
		appstore_webhandler.__init__(self, repo_domain)
		appstore_handler.__init__(self, self, libget_dir)
		parser.__init__(self)
		
		self.load_repo()

	def load_repo(self):
		repo = self.get_file()
		if not repo:
			raise "Failed to get repo"
		self.load_file(repo)

	def get_file(self):
		return getJson(self.name, self.repo_domain + "repo.json")