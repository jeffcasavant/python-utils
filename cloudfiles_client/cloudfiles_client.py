#!/usr/bin/env python2

import os
import sys
import pyrax
import argparse

#######################################
## Config options

credentialFileName = "/home/geardigitalops/.postgres.pyrax.cfg"

#######################################
## Command-line arguments

parser = argparse.ArgumentParser(
	description="Get specific content from Rackspace cloudfile container.")

parser.add_argument('-x', '--exclude', 
	help='Don\'t return containers with these strings; comma-separated.')

parser.add_argument('-k', '--keywords', 
	help='Only return containers with these strings; comma-separated.')

## Parse arguments
args = parser.parse_args()

## Convert exclude & keyword to lists
excludes = args.exclude.split(',') if args.exclude else []
keywords = args.keywords.split(',') if args.keywords else []

## Set up the Rackspace Connection:
if os.path.isfile(credentialFileName):
	pyrax.set_setting("identity_type", "rackspace")
	pyrax.set_credential_file(credentialFileName)
else:
    print "Invalid Credential file."
    sys.exit(1)

## Instantiate Cloud Files access:
cf = pyrax.cloudfiles

######################################
## Main

## Get a list of container names
containerNames = cf.list_containers()

if args.keywords:
	filteredList = []
	for keyword in keywords:
		containsKeyword = [name for name in containerNames if keyword.lower() in name.lower()]
		filteredList.extend(containsKeyword)
	containerNames = filteredList

if args.exclude:
	filteredList = []
	for exclude in excludes:
		noExclude = [name for name in containerNames if exclude.lower() not in name.lower()]
		filteredList.extend(noExclude)
	containerNames = filteredList

for number, name in enumerate(containerNames):
	print "%d: %s" % (number, name)
print "\nEnter number..."

number = int(raw_input())
container = cf.get_container(containerNames[number])

objectList = container.get_object_names()

for number, name in enumerate(objectList):
	print "%d: %s" % (number, name)

print "\nEnter number (or ALL)..."
response = raw_input()

print "\nEnter a filepath in which to save objects..."
path = raw_input()

if response == "ALL":
	for objName in objectList:
		container.download_object(objName, path)
else:
	container.download_object(objectList[int(response)], path)