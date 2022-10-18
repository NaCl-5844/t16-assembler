from sys import argv
import re

script, asm_file, bin_txt = argv #variables extracted from shell

def get_t16():
	with open('_t16_format_') as f:
		t16 = {}
		for ln in f: #Loop generates dictionary. keys:values = t16's op (name:format)
			opf = [ln][0].split(' ', 1)
			if len(opf) == 2:
				t16[opf[0]] = opf[1].replace('\n', '')
	return t16

def get_asm(file):
	asm = []
	with open(file) as f:
		for ln in f: #Loop generates a list of tuples from the input assembly file
			tmp = [ln][0].split(' ;', 1)
			cmd = re.split(', | ', tmp[0]) #Removes whitespaces ans commas
			if len(cmd) > 1:
				cmd[-1] = cmd[-1].replace('\n', '')
				asm.append((cmd[0], cmd[1:]))
	return asm

def gen_refcache():
	asm_cmd = [l[0] for l in _asm_] #Extracts assembly command from list of tuples
	ref = [{(k ,_t16_[k]) for k in _t16_ if k in asm_cmd}] #Puts matching keys t16 dictionary, puts the items in a list
	return ref

_asm_ = get_asm(asm_file)
_t16_ = get_t16()
# _t16_specs_ = {
# 	'r': list(range(0, 8)),
# 	'e': list(range(0, 8)),
# 	'v': list(range(0, 8)),
# }

print(_asm_)
print(gen_refcache())






