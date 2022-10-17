from sys import argv
import re

script, asm_file, bin_txt = argv

_t16_specs_ = {
	'r': list(range(0, 8)),
	'e': list(range(0, 8)),
	'v': list(range(0, 8)),
}




def get_t16():
	with open('_t16_format_v3.4_') as t:
		t16 = {}
		for op in t:
			j = op.split(' ', 1)
			if len(j) == 2:
				t16[j[0]] = j[1].replace('\n', '')
	return(t16)

def crossref_asm(asm, bcode):
	_t16_ = get_t16()
	with open(asm) as a:
		for line in a:
			command = line.split(' ')
			

print(_t16_specs_['r'])






















