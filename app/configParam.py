import os
import sys

# define your parameters here first
class configParam(object):
	def __init__(self):
		self.working_directory = '/home/manishhag/Documents/competition/Airbus/app'

		# do not change the FILENAME here in version 2 (can be changed in version 1)
		# since changing wont bring any effect
		# essentially any .dot can be taken since all of them have all the entry points
		self.FILENAME = "callgraph.dot"

		## for the version2 define your own entry point
		self.entry_point = ['BCO_Se_ExecuterCtlBite','LGD_Se_ExecuterServNvm']

