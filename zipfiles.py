#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = 'ZYSzys'

import os
import sys
import zipfile

reload(sys)
sys.setdefaultencoding('cp936')

class ZipDir(object):
	"""docstring for ZipFile"""
	def __init__(self):
		pass

	def zip_dir(self, dirname, zipfilename):
		filelist = []
		if os.path.isfile(dirname):
			filelist.append(dirname)
		else:
			for root, dirs, files in os.walk(dirname):
				for name in files:
					filelist.append(os.path.join(root, name))

		zf = zipfile.ZipFile(zipfilename, 'w', zipfile.zlib.DEFLATED)
		for tar in filelist:
			arcname = tar[len(dirname):]
			zf.write(tar, arcname)
		zf.close()
		print 'Zip Done!'

if __name__ == '__main__':
	dirname = '201605070523'
	zipfilename = dirname+'zys.zip'
	z = ZipDir()
	z.zip_dir(dirname, zipfilename)