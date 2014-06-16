#!/usr/bin/python

#A simple script to enable log4j in tomcat.

#Assumptions:
#There should be none.

import sys
import ConfigParser
import shutil
from os.path import expanduser
import os
import glob
import logging

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger(__name__)

def copyFile(source, destination):
	try:
		#shutil.copyFile(source, destination)
		logger.debug ("Copying " + source  + " To " + destination)
		shutil.copy2(source, destination)
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

def homeDirectory(config):
	use_home = config.get("local_setup", "use_home")
	if use_home:
		return expanduser("~")
	else: 
		return config.get('local_setup', 'use_home')

def copyFilesI(pattern, sourceDirectory, destinationDirectory):
	try:
		logger.debug("Copying jars from " + sourceDirectory + " TO " + destinationDirectory)
		for file in os.listdir(sourceDirectory):
			if file.endswith(pattern):
				copyFile(os.path.join(sourceDirectory, file), destinationDirectory)
			else:
				logger.debug("Ignoring " + file)
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

def copyProperties(sourceDirectory, destinationDirectory):
	logger.debug("Copying properties files from " + sourceDirectory + " ->" + destinationDirectory)
	copyFilesI(".properties", sourceDirectory, destinationDirectory)

# The source directory has all the jars that need to be
# copied.

def copyJars(sourceDirectory, destinationDirectory):
	copyFilesI('.jar', sourceDirectory, destinationDirectory)

def deleteFile(aDirectory, aFile):
	try:
	   path = os.path.join(aDirectory, aFile)
	   if os.path.exists(path):
		   	logger.debug("Deleting file " + aFile + " from " + aDirectory)
			os.remove(os.path.join(aDirectory, aFile))
	   else:
	   		logger.info("Path not found. Ignoring delete");
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass
def readConfig() :
	config = ConfigParser.ConfigParser()
	config.readfp(open('./config/setup.config'))
	log4j_location = config.get('log4j', 'log4j_location')
	commons_logging = config.get('log4j', 'commons_location')
	catalina_home = config.get('tomcat', 'catalina_home')
	catalina_lib = config.get('tomcat', 'catalina_lib')
	catalina_conf = config.get('tomcat', 'catalina_conf')
	catalina_props = config.get('tomcat', 'log_props')
	sourceSetup = config.get('local_setup', 'sourceSetup')
	log4j_location = os.path.join(homeDirectory(config), log4j_location)
	commons_logging = os.path.join(homeDirectory(config), commons_logging)
	catalina_lib = os.path.join(homeDirectory(config), catalina_home, catalina_lib)
	catalina_conf = os.path.join(homeDirectory(config), catalina_home, catalina_conf)
	
	logger.debug(log4j_location)
	logger.debug("\n")
	logger.debug(catalina_home)
	logger.debug("\n")
	logger.debug(catalina_lib)
	logger.debug("\n")
	logger.debug(catalina_conf)
	logger.debug("\n")
	#Now copy the log4j files
	#Now copy the juli files
	copyJars(log4j_location, catalina_lib)
	copyJars(sourceSetup, catalina_lib)
	copyJars(commons_logging, catalina_lib)
	copyProperties(sourceSetup, catalina_conf)
	deleteFile(catalina_conf, catalina_props)


def install_log4j():
	logger.debug("Installing log4j properties\n")
	logger.debug("Reading config\n")
	logger.debug("Reading config")
	readConfig()


if __name__ == "__main__":
	#Call the installation script
	install_log4j()