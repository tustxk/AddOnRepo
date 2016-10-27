# Script to generate the xml files for repo

import os
import xml.etree.ElementTree

def main():
	tree = xml.etree.ElementTree.parse("/media/sdc/xk/kkk/AddOnRepo/Australian/addons.xml")
	root = tree.getroot()
	for addon in root.findall('addon'):
		repoProviderName = addon.get('provider-name')
		if 'netxeon-country' == repoProviderName:
			break
	print repoProviderName
if __name__ == '__main__':
  main()
