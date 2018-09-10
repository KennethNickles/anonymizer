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

def main():
	fileName = sys.argv[1]
	fileExtension = fileName[fileName.find('.'):]
	print(fileExtension)
	salt = defaultSalt
	if len(sys.argv) > 2:
		salt = sys.argv[2]
	caches = {}
	if fileExtension == ".csv":
		with open(fileName, 'r', encoding="utf8") as readfile:
			reader = csv.reader(readfile, delimiter=',', quoting=csv.QUOTE_ALL)
			with open(fileName[:fileName.find('.')] + "_anonymized.csv", "w", encoding="utf8", newline='') as writefile:
				writer = csv.writer(writefile, delimiter=',', quoting=csv.QUOTE_ALL)
				index = 0
				newRows = []
				for row in reader:
					newRow = [row[0], row[1], row[2], row[3], row[4]]
					if index != 0:
						dk_readable = b"unknown"
						if row[2] in caches.keys():
							dk_readable = caches[row[2]]
						else:
							dk = hashlib.pbkdf2_hmac('sha1', str.encode(row[2]) , str.encode(salt), 100)
							dk_readable = binascii.hexlify(dk)
							caches[row[2]] = dk_readable
						newRow[0] = ""
						newRow[1] = ""
						newRow[2] = dk_readable
						print(newRow)
					writer.writerow(newRow)
					index += 1
	elif fileExtension == ".xlsx":
		file = pd.ExcelFile(fileName)
		df = pd.read_excel(file, file.sheet_names[0])
		for column in df.columns:
			if column == "lastname" or column == "firstname":
				df[column] = ""
			if column == "identityname":
				index = 0
				for value in df[column]:
					dk = hashlib.pbkdf2_hmac('sha1', str.encode(value) , str.encode(salt), 100000)
					dk_readable = base64.urlsafe_b64encode(dk)
					print(dk_readable)
					df[column][index] = dk_readable
					index += 1

		df.to_excel(fileName[:fileName.find('.')] + "_anonymized.xlsx", sheet_name=xlsx.sheet_names[0])
	else:
		raise Exception("unrecognized file type" + fileExtension)

if __name__ == '__main__':
	main()