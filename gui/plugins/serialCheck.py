import json
import re
import style
import tkinter as tk
import urllib.request
from gui.plugins import basePlugin
from gui.widgets import basePage
from appstore import Appstore
from asyncthreader import threader

ABOUT = "~Switch Serial Number Checker~\nOriginal Script by Anthony Da Mota\n\nChecks your Switch's serial number to see if is patched."

def download_object(remote_name):
	"""Downloads a file to memory"""
	try:
		r = urllib.request.urlopen(remote_name)
		if r.getcode() == 200:
			return r.read()
	except Exception as e:
		print(e)

class serialPage(basePage.BasePage):
	def __init__(self, app, container, plugin):
		basePage.BasePage.__init__(self, app, container, "Switch ~ SERIAL")
		self.plugin = plugin
		self.priority = 3

		self.about_label = tk.Label(self, text = ABOUT, background = style.secondary_color, font = style.smalltext, foreground = "#888888")
		self.about_label.place(relwidth = 1, x = style.offset, width = - 2 * style.offset, rely = 0.5, height = 70, y = - 110)

		self.entry_box = tk.Entry(self, foreground = "white", background = style.primary_color, justify = "center", font = style.mediumboldtext)
		self.entry_box.place(relwidth = 1, x = style.offset, width = - 2 * style.offset, rely = 0.5, height = 20, y = - 10)
		self.entry_box.bind("<KeyRelease>", self.on_key)

		self.results_variable = tk.StringVar()
		self.results_label = tk.Label(self, textvariable = self.results_variable, background = style.secondary_color, font = style.hugeboldtext)
		self.results_label.place(relwidth = 1, x = style.offset, width = - 2 * style.offset, rely = 0.5, height = 30, y = + 40)

	def on_key(self, event = None):
		self.results_variable.set(self.plugin.check(self.entry_box.get()))

class serialCheckPlugin(basePlugin.BasePlugin):
	def __init__(self, app, container):
		basePlugin.BasePlugin.__init__(self, app, "Switch Serial Checker", container)
		threader.do_async(self.get_serials)

	def get_serials(self):
		self.serials = json.loads(download_object("https://damota.me/ssnc/serials.json"))

	def get_pages(self):
		return [serialPage(self.app, self.container, self)]

	def exit(self):
		pass

	def check(self, serial_input):
		status = None
		digit_regex = r"\D"

		first_part = serial_input[0:4].upper()
		second_part = serial_input[3:10].upper()
		category_serials = self.serials.get(first_part)

		if len(serial_input) == 0:
			return ""

		status = "Too short" if len(serial_input) < 11 else ("Too long" if len(serial_input) > 14 else None)
		if status:
			return status

		if category_serials:
			second_part = re.sub(digit_regex, '0', second_part)
			serial_part = int(second_part)
			for serial in sorted(category_serials.keys()):
				if serial_part > int(serial):
					continue
				else:
					status = self.serials.get(first_part, {}).get(serial, 'patched')
					break

			if status is None:
				status = 'patched'
		else:
			status = "incorrect"
		return status

def setup(app, container):
	print("Setting up Switch Serial Checker...")
	return serialCheckPlugin(app, container)