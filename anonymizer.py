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

defaultSalt = "bluegreenredwhiteblack"

def main():
	fileName = sys.argv[1]
	salt = defaultSalt
	if len(sys.argv) > 2:
		salt = sys.argv[2]
	xlsx = pd.ExcelFile(fileName)
	df = pd.read_excel(xlsx, xlsx.sheet_names[0])
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


if __name__ == '__main__':
	main()