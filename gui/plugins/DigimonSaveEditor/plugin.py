#!/usr/bin/env python3
# Author: LyfeOnEdge
# Modified Date: 2020-02-26
# Purpose: Make a gui for DigimonSaveEditor.py 

from os import remove
from shutil import copy2
import struct
import tkinter as tk

import style
from gui.plugins import basePlugin
from gui.widgets import basePage, button
from gui.widgets import scrollingWidgets

#Hate me, idc. This made life easy.
from .DigimonSaveEditor import *

LABELWIDTH = 125
ABOUT = "~Digimon Save Editor~\nOriginal Script by AnalogMan\n\nApplies various edits to a Digimon Story Cyber Sleuth\nComplete Edition for Nintendo Switch save file."
CHEATS = [
    '1)  Add all medals to inventory                      (700 inventory slots)',
    '2)  Add 5 stacks of Popular Guy\'s Guide to inventory  (5 inventory slots)',
    '3)  Add 99x of all stat increasing foods to inventory  (7 inventory slots)',
    '4)  Add 99x of all stat decreasing items to inventory  (6 inventory slots)',
    '5)  Add 99x of all equipable USBs to inventory         (6 inventory slots)',
    '6)  Add 50x of all Digimon Accessories to inventory   (61 inventory slots)',
    '7)  Complete the Field Guide                          (Affects both games)',
    '8)  200% Scan all Digimon                        (Only discovered Digimon)',
    '9)  Add 95x of all items                              (Excludes Key Items)',
    '10) Max Yen',
    '11) Max Party Memory',
    '12) 100 Points short of Max Rank',
]
CHEATMAP = {}
#Map cheat number to cheat string
i = 1
for c in CHEATS:
    CHEATMAP[c] = i
    i += 1

GAMES = [
'1) Cyber Sleuth',
'2) Hacker\'s Memory',
'3) Both'
]
GAMEMAP = {}
i = 1
for g in GAMES:
    GAMEMAP[g] = i
    i += 1


class Page(basePage.BasePage):
    def __init__(self, app, container, plugin):
        basePage.BasePage.__init__(self, app, container, "Switch ~ DigiSE")
        self.plugin = plugin
        
        self.about_label = tk.Label(self, text = ABOUT, background = style.secondary_color, font = style.smalltext, foreground = "#888888")
        self.about_label.place(relwidth = 1, x = style.offset, width = - 2 * style.offset, rely = 0.5, height = 90, y = - 180)

        self.entry_label = tk.Label(self, text = "Save file path -", foreground = "white", background = style.secondary_color)
        self.entry_label.place(x = style.offset, width = LABELWIDTH, rely = 0.5, height = 20, y = - 70)
        self.entry_box = tk.Entry(self, foreground = "white", background = style.primary_color, justify = "center", font = style.mediumtext)
        self.entry_box.place(relwidth = 1, x = 2 * style.offset + LABELWIDTH, width = - (3 * style.offset + LABELWIDTH), rely = 0.5, height = 20, y = - 70)

        self.selected_save_edit_label = tk.Label(self, text = "Cheats -", foreground = "white", background = style.secondary_color)
        self.selected_save_edit_label.place(x = style.offset, width = LABELWIDTH, rely = 0.5, height = 20, y = - 40 )
        self.selected_save_edit = tk.StringVar()
        self.selected_save_edit.set(CHEATS[0])
        self.selected_save_edit_dropdown = tk.OptionMenu(self,self.selected_save_edit,*CHEATS)
        self.selected_save_edit_dropdown.configure(foreground = "white")
        self.selected_save_edit_dropdown.configure(background = style.primary_color)
        self.selected_save_edit_dropdown.configure(highlightthickness = 0)
        self.selected_save_edit_dropdown.configure(borderwidth = 0)
        self.selected_save_edit_dropdown.place(relwidth = 1, x = 2 * style.offset + LABELWIDTH, width = - (3 * style.offset + LABELWIDTH), rely = 0.5, height = 20, y = - 40)

        self.selected_game_label = tk.Label(self, text = "Game -", foreground = "white", background = style.secondary_color)
        self.selected_game_label.place(x = style.offset, width = LABELWIDTH, rely = 0.5, height = 20, y = - 10 )
        self.selected_game = tk.StringVar()
        self.selected_game.set(GAMES[0])
        self.selected_game_dropdown = tk.OptionMenu(self,self.selected_game,*GAMES)
        self.selected_game_dropdown.configure(foreground = "white")
        self.selected_game_dropdown.configure(background = style.primary_color)
        self.selected_game_dropdown.configure(highlightthickness = 0)
        self.selected_game_dropdown.configure(borderwidth = 0)
        self.selected_game_dropdown.place(relwidth = 1, x = 2 * style.offset + LABELWIDTH, width = - (3 * style.offset + LABELWIDTH), rely = 0.5, height = 20, y = - 10)

        self.run_button = button.Button(self, text_string = "run script", background = style.primary_color, callback = self.run)
        self.run_button.place(relwidth = 1, x = style.offset, width = - 2 * style.offset, rely = 0.5, height = 20, y = 20)

        self.console_label = tk.Label(self, text = "CONSOLE:", foreground = "white", background = style.secondary_color)
        self.console_label.place(relwidth = 1, x = - 0.5 * LABELWIDTH, width = LABELWIDTH, rely = 0.5, height = 20, y = 40 + style.offset)

        self.console = scrollingWidgets.ScrolledText(self, background = "black", foreground = "white")
        self.console.place(relwidth = 1, width = - (2 * style.offset), relheight = 0.5, height = - (2 * style.offset + 60), rely = 0.5, y = 60 + style.offset, x = + style.offset)

    def Print(self, string):
        self.console.insert("end", string)
        self.console.yview_pickplace("end")

    def run(self):
        main(self.entry_box.get(), GAMEMAP[self.selected_game.get()], CHEATMAP[self.selected_save_edit.get()], self.Print)
 
class Plugin(basePlugin.BasePlugin):
    def __init__(self, app, container):
        self.app = app
        self.container = container
        basePlugin.BasePlugin.__init__(self, app, "DigimonSaveEditor", container)
        self.page = Page(self.app, self.container, self)

    def get_pages(self):
        return[self.page]

    def exit(self):
        pass

def main(filepath: str, game: int, cheat: int, sout):
    """main function from DigimonSaveEditor.py modified to take args"""
    if game not in [CYBER_SLEUTH, HACKERS_MEMORY, CYBER_SLEUTH + HACKERS_MEMORY]:
        sout('\n\nInvalid game choice\n')
        return 1

    sout('\nBacking up save file...\n')
    try:
        copy2(filepath, filepath+'.bak')
    except Exception as e:
        sout(f'Could not make backup! Ensure file exists and directory is writable. Exception: {e}\n')
        return 1
        
    if game == CYBER_SLEUTH or game == (CYBER_SLEUTH + HACKERS_MEMORY):
        sout('Executing cheat for Cyber Sleuth...\n')
        if cheat == 1:
            ret = addToInventory(filepath, CS_Inv_Addr, medals, MEDAL_ITEM, 1)
        elif cheat == 2:
            item = [214]
            for _ in range(5):
                ret = addToInventory(filepath, CS_Inv_Addr, item, USABLE_ITEM, 99, True)
        elif cheat == 3:
            items = range(202, 209)
            ret = addToInventory(filepath, CS_Inv_Addr, items, USABLE_ITEM, 99)
        elif cheat == 4:
            items = [112, 115, 118, 121, 124, 127]
            ret = addToInventory(filepath, CS_Inv_Addr, items, USABLE_ITEM, 99)
        elif cheat == 5:
            ret = addToInventory(filepath, CS_Inv_Addr, equipment, EQUIP_ITEM, 99)
        elif cheat == 6: 
            ret = addToInventory(filepath, CS_Inv_Addr, accessories, ACCESSORY_ITEM, 50)
        elif cheat == 7:
            offset = 0x9CC
            for _ in range(351):
                offset += 4
                ret = write32(filepath, offset, 3)
                offset += 4
        elif cheat == 8:
            offset = CS_DigiConvert_Addr
            for _ in range(346):
                offset += 2
                ret = write16(filepath, offset, 200)
                offset += 2
        elif cheat == 9:
            ret = allItems(filepath, CS_Inv_Addr)
        elif cheat == 10:
            ret = write32(filepath, CS_Money_Addr, 9999999)
        elif cheat == 11:
            ret = write32(filepath, CS_Party_Mem_Addr, 255)
        elif cheat == 12:
            ret = write32(filepath, CS_Rank_Addr, 19)
            ret = write32(filepath, CS_Points_Addr, 49900)
        else:
            sout('Invalid cheat choice.\n')
            return 1

    if game == HACKERS_MEMORY or game == (CYBER_SLEUTH + HACKERS_MEMORY):
        sout('Executing cheat for Hacker\'s Memory...\n')
        if cheat == 1:
            ret = addToInventory(filepath, HM_Inv_Addr, medals, MEDAL_ITEM, 1)
        elif cheat == 2:
            item = [214]
            for _ in range(5):
                ret = addToInventory(filepath, HM_Inv_Addr, item, USABLE_ITEM, 99, True)
        elif cheat == 3:
            items = list(range(202, 209))
            ret = addToInventory(filepath, HM_Inv_Addr, items, USABLE_ITEM, 99)
        elif cheat == 4:
            items = [112, 115, 118, 121, 124, 127]
            ret = addToInventory(filepath, HM_Inv_Addr, items, USABLE_ITEM, 99)
        elif cheat == 5:
            ret = addToInventory(filepath, HM_Inv_Addr, equipment, EQUIP_ITEM, 99)
        elif cheat == 6: 
            ret = addToInventory(filepath, HM_Inv_Addr, accessories, ACCESSORY_ITEM, 50)
        elif cheat == 7:
            offset = 0x9CC
            for _ in range(351):
                offset += 4
                ret = write32(filepath, offset, 3)
                offset += 4
        elif cheat == 8:
            offset = HM_DigiConvert_Addr
            for _ in range(346):
                offset += 2
                ret = write16(filepath, offset, 200)
                offset += 2
        elif cheat == 9:
            ret = allItems(filepath, HM_Inv_Addr)
        elif cheat == 10:
            ret = write32(filepath, HM_Money_Addr, 9999999)
        elif cheat == 11:
            ret = write32(filepath, HM_Party_Mem_Addr, 255)
        elif cheat == 12:
            ret = write32(filepath, HM_Rank_Addr, 19)
            ret = write32(filepath, HM_Points_Addr, 49900)
        else:
            sout('Invalid cheat choice.\n')
            return 1
    
    if ret == 0:
        sout('Clearing backup...\n')
        try:
            remove(filepath+'.bak')
        except:
            sout('Could not remove backup file. Remove manually.\n')
        sout('Done!\n')
    if ret > 0:
        sout('An error has occured applying cheats. Please check that the file exists, is writable, and is not corrupted.\n'
            'Restoring backed up save...')
        try:
            copy2(filepath+'.bak', filepath)
            sout('Backup restored successfully.\n')
            remove(filepath+'.bak')
        except:
            sout('Could not restore backup file. Please manually rename backup file.\n')

    return ret

def setup(app, container):
    return Plugin(app, container)