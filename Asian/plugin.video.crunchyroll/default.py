"""
    CrunchyRoll
"""
import sys
import xbmcaddon

#plugin constants
__plugin__ = "CrunchyRoll"
__version__ = "2.2.3"
__settings__ = xbmcaddon.Addon(id='plugin.video.crunchyroll')

print "[PLUGIN] '%s: version %s' initialized!" % (__plugin__, __version__)

if __name__ == "__main__":
    from resources.lib import crunchy_main as crunchyroll
    if not sys.argv[2]:
        crunchyroll.Main()
    else:
        crunchyroll.Main()

sys.modules.clear()
