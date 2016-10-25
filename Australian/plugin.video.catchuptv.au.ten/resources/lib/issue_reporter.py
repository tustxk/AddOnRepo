#
#   Network Ten CatchUp TV Video Addon
#
#   Copyright (c) 2014 Adam Malcontenti-Wilson
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.
#

import base64
import config
import os
import re
import sys
import urllib2
import rollbar

try:
  import simplejson as json
except ImportError:
  try:
    import deps.simplejson as json
  except ImportError:
    import json

LOG_FILTERS = (
  ('//.+?:.+?@', '//[FILTERED_USER]:[FILTERED_PASSWORD]@'),
  ('<user>.+?</user>', '<user>[FILTERED_USER]</user>'),
  ('<pass>.+?</pass>', '<pass>[FILTERED_PASSWORD]</pass>'),
)

ROLLBAR_API_TOKEN = 'd3402b7c1e3a4a758dc1f25d5eedf72a'

class IssueReporter:
  def __init__(self, utils):
    self.utils = utils
    env = 'development' if os.path.isdir(os.path.join(self.utils.addon_dir, '.git')) else 'production'
    rollbar.init(ROLLBAR_API_TOKEN, env, handler='blocking', code_version='v%s' % self.utils.version, root=self.utils.addon_dir)

  def make_request(self, url):
    return urllib2.Request(url, headers={
      "Authorization": "Basic %s" % config.GITHUB_API_AUTH,
      "Content-Type": "application/json",
      "User-Agent": '%s/%s' % (self.utils.id, self.utils.version)
    })

  def get_xbmc_log(self):
    from xbmcswift2 import xbmc
    log_path = xbmc.translatePath('special://logpath')
    log_file_path = os.path.join(log_path, 'kodi.log')
    if not os.path.exists(log_file_path):
        log_file_path = os.path.join(log_path, 'xbmc.log')

    self.utils.log.debug("Reading log file from \"%s\"" % log_file_path)
    with open(log_file_path, 'r') as f:
      log_content = f.read()
    for pattern, repl in LOG_FILTERS:
      log_content = re.sub(pattern, repl, log_content)
    return log_content

  def get_xbmc_version(self):
    try:
      from xbmcswift2 import xbmc
      return xbmc.getInfoLabel( "System.BuildVersion" )
    except:
      return 'Unknown'

  def upload_log(self):
    try:
      log_content = self.get_xbmc_log()
    except Exception as e:
      self.utils.log.error("Failed to read log: %s" % e)
      return None

    self.utils.log.debug("Uploading xbmc.log")
    try:
      response = urllib2.urlopen(self.make_request(config.GIST_API_URL), json.dumps({
        "files": {
          "xbmc.log": {
            "content": log_content
          }
        }
      }))
    except urllib2.HTTPError as e:
      print e
      self.utils.log.error("Failed to save log: HTTPError %s" % e.code)
      return False
    except urllib2.URLError as e:
      print e
      self.utils.log.error("Failed to save log: URLError %s" % e.reason)
      return False
    try:
      return json.load(response)["html_url"]
    except:
      self.utils.log.error("Failed to parse API response: %s" % response.read())

  def report_issue(self, issue_data):
    log_url = self.upload_log()
    rollbar.report_exc_info(
    payload_data={
      "request": {
        "url": sys.argv[0],
        "user_ip": "$remote_ip",
      },
      "addon": {
        "name": self.utils.name,
        "id": self.utils.id,
        "version": self.utils.version
      },
      "client": {
        "log_url": log_url,
        "xbmc_version": self.get_xbmc_version(),
        "python_version": sys.version,
        "python_path": sys.path,
        "os": {
          "platform": sys.platform,
          "uname": os.uname()
        }
      },
      "platform": sys.platform
    })
