import os
import re
import sys
import xbmc
import xbmcgui

import addon.common

addon = Addon('plugin.video.free.cable', sys.argv)

def has_upgraded():
    old_version = addon.get_setting('old_version').split('.')
    new_version = addon.get_version().split('.')
    current_oct = 0
    for octant in old_version:
        if int(new_version[current_oct]) > int(octant):
            try: addon.log('New version found')
            except: pass
            return True
        current_oct += 1
    return False


class TextBox:
    # constants
    WINDOW = 10147
    CONTROL_LABEL = 1
    CONTROL_TEXTBOX = 5

    def __init__(self, *args, **kwargs):
        # activate the text viewer window
        xbmc.executebuiltin("ActivateWindow(%d)" % ( self.WINDOW, ))
        # get window
        self.win = xbmcgui.Window(self.WINDOW)
        # give window time to initialize
        xbmc.sleep(1000)
        self.setControls()

    def setControls(self):
        # set heading
        heading = "Upgrade message"
#         heading = "Free Cable v%s" % (addon.get_version())
        self.win.getControl(self.CONTROL_LABEL).setLabel(heading)
        # set text
        root = addon.get_path()
        faq_path = os.path.join(root, 'info.txt')
        f = open(faq_path)
        text = f.read()
        self.win.getControl(self.CONTROL_TEXTBOX).setText(text)
        