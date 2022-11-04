from sys import argv
import re

script, asm_file, bin_txt = argv #variables extracted from shell

_t16_format_ = '_t16_format_'
_t16_bwidth = 16
_t16_sr, _t16_fr, _t16_vr = (8, 8, 8) #registers
_t16_misc = {
	'k': 0,					# peeK mask
	'p': 1,					# poP mask
	'$': 'NOT IMPLEMENTED',	# Variable indicator - if I go that far
}

def get_asm():
	asm = {}
	with open(asm_file, 'r') as f:
		for k, v in enumerate(f):
			hot_cmd = re.split(' ', v, 1)
			if len(v.split()) >= 2:
				asm[k] = (hot_cmd[0], re.split(' \n| ;', hot_cmd[1])[0])
		return asm #asm[i-line] -> (op, 'oper str')

def get_rc():
	rc = {}
	op_set = {v[0] for v in _asm_.values()}
	with open(_t16_format_, 'r') as f:
		for ln in f:
			hot_ln = ln.split()
			if len(hot_ln) > 1:
				if hot_ln[0] in op_set:
					rc[hot_ln[0]] = hot_ln[1].replace('-', '')
		return rc #rc[op] -> fmt

def parse(entry): # entry = ('op,er,an,ds', ('fmt', {}))
	fmt = entry[1][0]
	hot_fmt = re.findall('M|N|C|B|A', fmt)
	if len(hot_fmt) > 0: # one or more operand to be processed
		opr_dic = entry[1][1]
		entry_opr = entry[0].rsplit(', ', 1)
		hot_opr = entry_opr[-1]
		blen = len(re.findall(f"{hot_fmt[-1]}", fmt))
		try:
			hot_val = int(re.sub('[a-zA-Z|\n]', '', hot_opr)) # <-- gets calculated regardless of exception
			1/(abs(hot_val)+(hot_val)) #if val is +ve, 1/2*val else 1/0
			# -ve values are exceedingly rare as only immediates use them
			opr_dic[hot_fmt[-1]] = f"{hot_val:0{int(blen)}b}"
		except ZeroDivisionError:
			if hot_val != 0: # -ve values get bitmasked before being converted to binary
				opr_dic[hot_fmt[-1]] = f"{((1<<blen)-1)-(~hot_val):0{int(blen)}b}"
				tmp = f"{((1<<blen)-1)-(~hot_val):0{int(blen)}b}"
			else: # If 0. ## I don't like how my (duck?) method excludes r0
				opr_dic[hot_fmt[-1]] = f"{hot_val:0{int(blen)}b}"
		except:
			try: # string supplied as operand is searched in _t16_misc to find it's binary value
				hot_val = re.sub('[ |\n]', '', hot_opr)
				opr_dic[hot_fmt[-1]] = str(_t16_misc[hot_val])
			except Exception: #learn how to give more + accurate error messages
				print(f"Unknown Error: Check assembly file for errors.\n\tHINT: Err in {entry}")
				exit()
		fmt = fmt.replace(hot_fmt[-1], '', (blen-1)).replace(hot_fmt[-1], opr_dic[hot_fmt[-1]])
		return parse((entry_opr[0], (fmt, opr_dic)))
	else: # entry = ('op,er,an,ds', ('fmt', {}))
		return entry[1][0]

def main():
	global _asm_, _rc_
	_asm_ = get_asm() #asm[i-line] -> (op, 'oper str')
	_rc_ = get_rc()	#rc[op] -> 'fmt'
	_t16_ = {}
	_bytecode_ = open(bin_txt, 'w')
	for l in _asm_.keys(): 	
		try:
			tmp = {}
			#parse(('oper str', ('fmt', {}))) <- empty dict
			#output[l] = 't16 bytecode'
			asm_ln = _asm_[l]
			_t16_[l] = parse((asm_ln[1], (_rc_[asm_ln[0]], tmp)))
			_bytecode_.write(f"{_t16_[l]}\n")
		except KeyError:
			print(f"KeyError:: Line {l}, in <{asm_file}>:\n  HINT: no instruction '{_asm_[l][0]}' found in T16's isa.")
			_bytecode_.close()
			exit()
		except:
			# print(f"Unknown Error: Check your assembly and _t16_format_ for errors")
			_bytecode_.close()
			exit()
	_bytecode_.close()
	return print('done')

if __name__ == "__main__":
	main()
