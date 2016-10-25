script.module.catchuptv.brightcove
==================================

Python wrapper for the Brightcove read-only API.

```python
from brightcove.api import Brightcove

TOKEN = 'myreadonlytoken.'
b = Brightcove(TOKEN)
videos = b.find_all_videos()
```

To use within an XBMC addon, add the following line to the `<requires>` tag in your addon.xml:
```xml
<import addon="script.module.brightcove"/>
```

See:

* http://support.brightcove.com/en/docs/getting-started-media-api
* http://docs.brightcove.com/en/media/
