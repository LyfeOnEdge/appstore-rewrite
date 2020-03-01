import os
import sys
import importlib.util
import tkinter as tk

import style
from .pages import __pages__
from .detailPage import DetailPage
from .plugins import __plugins__
from .widgets import *

from gui.widgets import scrollingWidgets
from asyncthreader import threader

#Frame handler, raises and pages in z layer,
class window(tk.Tk):
	def __init__(self, args, geometry):
		tk.Tk.__init__(self)
		self.args = args
		self.geometry(geometry)
		self.frame_titles = None
		self.current_frame = None
		self.last_selection = None
		self.path = None
		self.pagelist = []
		self.has_update = None
		# self.resizable(False, False)

		self.detail_page = DetailPage(self)
		self.detail_page.place(relwidth = 1, relheight = 1)

		self.main_page = themedFrame.ThemedFrame(self, background = style.primary_color)
		self.main_page.place(relwidth = 1, relheight = 1)

		#Left column 
		self.column = themedFrame.ThemedFrame(self.main_page, background = style.primary_color)
		self.column.place(relx = 0, rely = 0, width = style.sidecolumnwidth, relheight = 1)

		self.column_title = themedLabel.ThemedLabel(self.column,"Appstore\nWorkbench\nGPLv3",anchor="center",font=style.largeboldtext, background = style.primary_color)
		self.column_title.place(relx = 0, y = + style.offset, relwidth = 1, height = style.column_headerheight - 2 * style.offset)

		self.column_title_separator = themedLabel.ThemedLabel(self.column, "", background=style.separator_color)
		self.column_title_separator.place(x = style.offset, y = style.column_headerheight - 1.5 * style.offset, relwidth = 1, width = -2 * style.offset, height = 1)

		self.category_listbox = scrollingWidgets.ScrolledThemedListBox(self.column, foreground = style.lg, borderwidth = 0, highlightthickness = 0)
		self.category_listbox.configure(activestyle = "none")
		self.category_listbox.place(relx = 0, relwidth = 1, y = style.column_headerheight, relheight = 1, height = - (2 * style.listbox_footer_height + style.column_headerheight + 2 * style.offset), width = - style.offset)
		self.category_listbox.bind('<<ListboxSelect>>',self.select_frame)

		self.column_footer_separator = themedLabel.ThemedLabel(self.column, "", background=style.separator_color)
		self.column_footer_separator.place(x = style.offset, rely = 1, y = - (2 * style.listbox_footer_height + style.offset), relwidth = 1, width = -2 * style.offset, height = 1)

		self.column_footer = themedFrame.ThemedFrame(self.column, background = style.primary_color)
		self.column_footer.place(relx = 0, rely = 1, relwidth = 1, height = 2 * style.listbox_footer_height, y = - 2 * style.listbox_footer_height)

		self.column_set_sd = button.Button(self.column_footer, 
			callback = self.set_sd, 
			text_string = "- Select SD Root -", 
			font=style.mediumtext, 
			background=style.set_sd_button_background,
			foreground=style.set_sd_button_foreground
			).place(relwidth = 1, y = 0, x = style.offset, width = - 2 * style.offset, height = style.listbox_footer_height)

		self.column_sd_status_label = themedLabel.ThemedLabel(self.column_footer,"SD - Not Set",anchor="center",font=style.smalltext, background = style.primary_color, foreground= style.pathdisplaytextcolor)
		self.column_sd_status_label.place(x = style.offset, relwidth = 1, width = - 2 * style.offset, y = -style.listbox_footer_height, height = style.listbox_footer_height, rely=1,  )

		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		self.container = themedFrame.ThemedFrame(self.main_page)
		self.container.place(x = style.sidecolumnwidth, width = - style.sidecolumnwidth, relwidth = 1, relheight = 1)

		self.frames = {}

		self.load_plugins()
		#Stack pages in container	
		self.load_utility_pages()

		self.category_listbox.select_set(0) #sets focus on the first item in listbox
		self.category_listbox.event_generate("<<ListboxSelect>>")

		self.show_frame(self.pagelist[0].name)

		#Pull the main page to focus
		self.main_page.tkraise()

	def select_frame(self, event):
		try:
			widget = event.widget
			selection = widget.curselection()
			picked = widget.get(selection[0])
			if not picked == self.last_selection:
				frame = None
				for f in self.frames:
					self.frames[f].picked = False
					if self.frames[f].name.strip() == picked.strip():
						self.frames[f].picked = True #Only reload frame if it's visible, saves a lot of unnecessary page rebuilds and makes resizing faster
						self.show_frame(self.frames[f].name)
				self.last_selection = picked
		except Exception as e:
			print(e)
			pass

	def show(self):
		self.tkraise()

	def show_frame(self, page_name):
		#Show frame for the given page name
		frame = self.frames[page_name]
		frame.event_generate("<<ShowFrame>>")
		frame.tkraise()
		print("Raised frame - {}".format(page_name))

	def set_version(self, version_string):
		self.version = version_string

	def load_plugins(self):
		global __plugins__
		if not __plugins__:
			return
		pagelist = []
		
		def load_plugin(plugin):
			print("==============================")
			print(f"Loading plugin at {plugin}")
			spec = importlib.util.spec_from_file_location(os.path.basename(plugin)[:-3], plugin)
			p = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(p)
			print(f"Running plugin setup.")
			plug = p.setup(self, self.container)
			print(f"Plugin - {plug.name}")
			pages = plug.get_pages()
			if pages:
				numpages = len(pages)
				print(f"Adding {numpages} pages")
			else:
				print("No pages to load")

			pagelist.extend(pages)

		print("\nLoading plugins.")

		for plugin in __plugins__:
			try:
				load_plugin(plugin)
			except Exception as e:
				print(f"Exception loading plugin {plugin} - {e}")

		print("==============================")
		print("TODO: add 'requirements' attribute to plugin to verify with importlib that they all exist to avoid a crash caused by a plugin failing to import")
		print("Done loading plugins.\n")
		self.load_pages(pagelist)

	def load_pages(self, pagelist):
		"""Sort pages in alphabetical order"""
		#Add pages as frames to dict, with keyword being the name of the frame
		pagelist.sort(key=lambda x: x.name, reverse=False)
		if pagelist:
			for F in pagelist:
				page_name = F.name
				self.frames[page_name] = F
				self.category_listbox.insert("end", " {}".format(page_name))

				#place the frame to fill the whole window, stack them all in the same place
				F.place(relwidth = 1, relheight = 1)
				self.pagelist.append(F)
		else:
			print("No pages to initialize.")

	def load_utility_pages(self):
		pagelist = []
		if __pages__:
			for page in __pages__:
				spec = importlib.util.spec_from_file_location(os.path.basename(page)[:-3], page)
				p = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(p)
				pagelist.append(p.setup(self, self.container))
		self.load_pages(pagelist)

	def reload_category_frames(self, force):
		print("Reloading frames")
		for frame in self.frames:
			try:
				self.frames[frame].configure(event = None, force = force)
			except Exception as e:
				pass

	def set_sd(self):
		chosensdpath = tk.filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
		self.path = chosensdpath
		self.reload_category_frames(True)
		self.update_sd_path()

	def update_sd_path(self, path = None):
		if not path:
			path = self.path
		chosensdpath = path
		if chosensdpath:
			#Get the basename
			basepath = os.path.basename(os.path.normpath(chosensdpath))
			#If we didn't find it, assume it's a root dir and just return the whole path
			if not basepath:
				basepath = chosensdpath
		else:
			basepath = "Not Set"
		self.column_sd_status_label.set("SD - {}".format(basepath))