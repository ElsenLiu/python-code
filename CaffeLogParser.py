
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab as pl

class CaffeLogParser(object):
	max_iter = 0
	train_iter = 0
	test_iter = 0
	test_accuracy_list = list()
	test_loss_list = list()
	train_loss_list = list()

	def __init__(self, logpath, outfolder):
		self.logpath = logpath
		self.outfolder = outfolder

	def parse_log_file(self):
		logfile = open(self.logpath, "r")
		loglines = logfile.readlines()
		for logline in loglines:
			# parse max_iter
			if "max_iter: " in logline:
				self.max_iter = int(logline.split("max_iter: ")[-1])

			# parse train_iter
			elif "display: " in logline:
				self.train_iter = int(logline.split("display: ")[-1])

			# parse max_iter
			elif "test_iter: " in logline:
				self.test_iter = int(logline.split("test_iter: ")[-1])

			# parse test accuracy
			elif "Test net output #0: accuracy = " in logline:
				accuracy = float(logline.split("accuracy = ")[-1])
				self.test_accuracy_list.append(accuracy)

			# parse test loss
			elif "Test net output #1: loss = " in logline:
				loss = float(logline.split("loss = ")[-1].split(" (* 1")[0])
				self.test_loss_list.append(loss)

			# parse train loss
			elif "Train net output #0: loss = " in logline:
				loss = float(logline.split("loss = ")[-1].split(" (* 1")[0])
				self.train_loss_list.append(loss)
		logfile.close()

	def print_parse_result(self):
		print "max iteration: ", self.max_iter
		print "train iteration: ", self.train_iter
		print "test iteration: ", self.test_iter
		print "test accuracy: ", self.test_accuracy_list
		print "test loss: ", self.test_loss_list
		print "train loss: ", self.train_loss_list

	'''
	train test loss plot image
	'''
	def save_ttloss_plot_image(self):
		plt.plot(self.train_iter * np.arange(len(self.train_loss_list)), self.train_loss_list, label='train loss', color='r')
		plt.plot(self.test_iter * np.arange(len(self.test_loss_list)), self.test_loss_list, label='test loss', color='g')

		plt.xlabel('iteration')
		plt.ylabel('train&test loss')
		plt.title('Loss on Train vs. Test')
		plt.legend()
		# plt.show()
		plt.savefig(os.path.join(self.outfolder, 'ttloss.jpg'))
		plt.close()

	'''
	test accuracy plot image
	'''
	def save_accuracy_plot_image(self):
		plt.plot(self.test_iter * np.arange(len(self.test_accuracy_list)), self.test_accuracy_list, color='r')
		
		plt.xlabel('iteration')
		plt.ylabel('test accuracy')
		plt.title('Test accuracy')
		# plt.show()
		plt.savefig(os.path.join(self.outfolder, 'accuracy.jpg'))
		plt.close()


def usage():
	print "\nThis program help you parse caffe log file and create plot images.\n\n" \
	"Parse content: \n  train loss, test loss, test accuracy.\n\n" \
	"Usage: \n  python CaffeLogParser.py -i [logpath] -o [outfolder]\n\n" \
	"To save caffe log to file, you should write train.sh like this: \n\n" \
	"  #!/usr/bin/env sh \n\n" \
	"  LOG=train-`date +%Y-%m-%d-%H-%M-%S`.log\n" \
	"  CAFFE=$CAFFE_ROOT/build/tools/caffe\n" \
	"  SOLVER=$SOLVER_PATH\n\n" \
	"  $CAFFE train --solver=$SOLVER --gpu=0 2>&1 | tee $LOG\n"


import sys, getopt
opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
logpath=""
outfolder=""
for op, value in opts:
    if op == "-i":
        logpath = value
    elif op == "-o":
        outfolder = value
        if not os.path.isdir(outfolder):
        	os.mkdir(outfolder)
    elif op == "-h":
        usage()
        sys.exit()


parser = CaffeLogParser(logpath, outfolder)
parser.parse_log_file()
parser.print_parse_result()
parser.save_ttloss_plot_image()
parser.save_accuracy_plot_image()
