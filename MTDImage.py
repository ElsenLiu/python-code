# coding: utf8

import os
import urllib2
import threading

'''
from MTDImage import MTDImage

mtdimage = MTDImage(in_urls, out_names, out_folder)
mtdimage.start()
'''

class MTDImage(object):
	'''
	Multi Thread Download Image
	构造多线程对图片进行下载，未优化，多线程下载时失败率高

	in_urls: 需要下载的图片url
	out_names: 下载图片后保存的文件名，和in_urls对应
	out_folder: 下载的文件夹位置
	'''
	thread_number = 1

	def __init__(self, in_urls, out_names, out_folder):
		object.__init__(self)
		self.in_urls = in_urls
		self.out_names = out_names
		self.out_folder = out_folder

	def start(self):
		batch_size = len(self.in_urls) / self.thread_number
		for i in range(self.thread_number):
			batch_urls = self.in_urls[i*batch_size:(i+1)*batch_size]
			batch_names = self.out_names[i*batch_size:(i+1)*batch_size]
			thread = ImageDownloaderThread(batch_urls, batch_names, self.out_folder)
			thread.start()

class ImageDownloaderThread(threading.Thread):
	'''
	ImageDownloaderThread
	单个下载线程

	in_urls: 需要下载的图片url
	out_names: 下载图片后保存的文件名，和in_urls对应
	out_folder: 下载的文件夹位置
	'''
	def __init__(self, in_urls, out_names, out_folder):
		threading.Thread.__init__(self)
		self.in_urls = in_urls
		self.out_names = out_names
		self.out_folder = out_folder

	def run(self):
		for i in range(len(self.in_urls)):
			in_url = self.in_urls[i]
			print in_url
			out_name = self.out_names[i]
			try:

				image_data = urllib2.urlopen(urllib2.Request(in_url)).read()

				out_file = open(os.path.join(self.out_folder, out_name), "wb")
				out_file.write(image_data)
				out_file.close()
			except:
				print "download failed"
		

