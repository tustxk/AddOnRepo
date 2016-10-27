# Script to generate the xml files for repo

import os
import xml.etree.ElementTree

def get_repo_value(repo_dir, key):
  repo_file = os.path.join(repo_dir, 'addons.xml') 
  try:
    tree = xml.etree.ElementTree.parse(repo_file)
    root = tree.getroot()
    for addon in root.findall('addon'):
      repoProviderName = addon.get('provider-name')
      if 'netxeon' in repoProviderName:
        return addon.get(key)
  except Exception as e:
    print 'Failed to open %s' % repo_file
    print e.message

def main():
	tree = xml.etree.ElementTree.parse("/media/sdc/xk/kkk/AddOnRepo/kkk/addons.xml")
	root = tree.getroot()
	for addon in root.findall('addon'):
		repoProviderName = addon.get('provider-name')
		print repoProviderName
		if 'netxeon-country' == repoProviderName:
			break
	print repoProviderName
if __name__ == '__main__':
  main()
