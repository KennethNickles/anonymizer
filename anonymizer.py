#!/usr/bin/python3

# install python3
# link python3
# download conda 3.6
# install conda 3.6

import sys
import hashlib
import binascii
import base64
import pandas as pd
import numpy as np
import csv

defaultSalt = "bluegreenredwhiteblack"
username = "Username"
firstname = "FirstName"
lastname = "LastName"

def main():
	fileName = sys.argv[1]
	fileExtension = fileName[fileName.find('.'):]
	print(fileExtension)
	salt = defaultSalt
	if len(sys.argv) > 2:
		salt = sys.argv[2]
	if fileExtension == ".csv":
		parseCsv(fileName, salt)
	else:
		raise Exception("unrecognized file type" + fileExtension)

def parseCsv(fileName, salt):
	with open(fileName, 'r', encoding="utf8") as readfile, open(fileName[:fileName.find('.')] + "_anonymized.csv", "w", encoding="utf8", newline='') as writefile:
		reader = csv.DictReader(readfile)
		writer = csv.DictWriter(writefile, fieldnames=reader.fieldnames)
		caches = {}
		newRows = []
		index = 0
		for row in reader:
			newRow = row.copy()
			if index != 0:
				dk_readable = b"unknown"
				if newRow[username] in caches.keys():
					dk_readable = caches[row[username]]
				else:
					dk = hashlib.pbkdf2_hmac('sha1', str.encode(row[username]) , str.encode(salt), 100)
					dk_readable = binascii.hexlify(dk)
					caches[row[username]] = dk_readable
				newRow[username] = dk_readable.decode("utf-8") 
				newRow[firstname] = ""
				newRow[lastname] = ""
				print(newRow)
			writer.writerow(newRow)
			index += 1

if __name__ == '__main__':
	main()