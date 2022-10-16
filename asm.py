from sys import argv
import re

script, asm_file, bin_txt = argv

with open(asm_file) as asm:
	asmDict = {}
	for i in asm:
		j = i.split(' ', 1)
		if len(j) == 2:
			asmDict[j[0]] = j[1].replace('\n', '')
print(asmDict)


























