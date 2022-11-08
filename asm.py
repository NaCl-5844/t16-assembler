from sys import argv
import re
version = '[v1.2.0]'

### TODO{
## v1.2.0:
# - adjust argv to be modular and add error checks
# - use improved argv to select output format, verbose/debug, and help [bxvh]
## v1.3.0:
# - add debug mode using log(), if bool or another method
## v1.4.0:
# - output format[bx] can use both formats side by side, eg 1100110011001100 CCCC
## v1.5.0:
# - add a way to convert output files between binary and hex 
## v2.0.0 == v.1.5.x has all features finished and debugged
### }

_t16_format = '_t16_format_'
_t16_bwidth = 16
_t16_misc = {
	'k': 0,					# peeK mask
	'p': 1,					# poP mask
	'$': 'NOT IMPLEMENTED',	# Variable indicator - if I go that far
}

def get_asm(file):
	asm = {}
	f = open(file, 'r')
	for k, v in enumerate(f):
		hot_cmd = re.split(' ', v, 1)
		if len(v.split()) >= 2:
			asm[k] = (hot_cmd[0], re.split(' \n| ;', hot_cmd[1])[0])
	f.close()
	return asm #asm[i-line] -> (op, 'oper str')

def get_rc(_asm_):
	rc = {}
	op_set = {v[0] for v in _asm_.values()}
	with open(_t16_format, 'r') as f:
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
		try:
			_argv_lookup[v](entry)
		except:
			pass
		opr_dic = entry[1][1]
		entry_opr = entry[0].rsplit(', ', 1)
		hot_opr = entry_opr[-1]
		blen = len(re.findall(f"{hot_fmt[-1]}", fmt)) ### >> 2 if option = '-x'
		try:
			hot_val = int(re.sub('[a-zA-Z|\n]', '', hot_opr)) # <-- gets calculated regardless of exception
			1/(abs(hot_val)+(hot_val)) #if val is +ve: 1/2*val; else: 1/0
			# -ve values are exceedingly rare as only immediates use them
			opr_dic[hot_fmt[-1]] = f"{hot_val:0{int(blen)}b}" ### replace '...b}"' with variable {format var}
		except ZeroDivisionError:
			if hot_val != 0: # -ve values get bitmasked before being converted to binary
				opr_dic[hot_fmt[-1]] = f"{((1<<blen)-1)-(~hot_val):0{int(blen)}b}"
				# tmp = f"{((1<<blen)-1)-(~hot_val):0{int(blen)}b}" ### replace '...b}"' with variable {format var}
			else: # If 0. ## I don't like how my (duck?) method excludes r0
				opr_dic[hot_fmt[-1]] = f"{hot_val:0{int(blen)}b}" ### replace '...b}"' with variable {format var}
		except:
			try: # string supplied as operand is searched in _t16_misc to find it's binary value
				hot_val = re.sub('[ |\n]', '', hot_opr)
				opr_dic[hot_fmt[-1]] = str(_t16_misc[hot_val])
			except Exception: #learn how to give more + accurate error messages
				print(f"Unknown Error:: Check assembly file for errors.\n\tHINT: Err in parse({entry})")
				exit()
		fmt = fmt.replace(hot_fmt[-1], '', (blen-1)).replace(hot_fmt[-1], opr_dic[hot_fmt[-1]])
		return parse((entry_opr[0], (fmt, opr_dic)))
	else: # entry = ('op,er,an,ds', ('fmt', {}))
		try:
			_argv_lookup[v](entry)
		except:
			pass
		return entry[1][0]


# def assemble(base, _asm_):
# 	# parse(('oper str', ('fmt', {}))) <- empty dict
# 	for l in _asm_.keys():
# 		try: # parse(('oper str', ('fmt', {}))) <- empty dict
# 			tmp = {}
# 			asm_ln = _asm_[l]
# 			_t16_[l] = parse((asm_ln[1], (_rc_[asm_ln[0]], tmp)))
# 			if 'b' & 'x' in base:
# 				_bytecode_.write(f"{_t16_[l]} {_t16_[l]:0X}\n")
# 		except KeyError:
# 			print(f"KeyError:: Line {l}, in <{asm_file}>:\n\tHINT: no instruction '{_asm_[l][0]}' found in T16's isa.")
# 			_bytecode_.close()
# 			exit()
# 		except:
# 			print(f"Unknown Error:: Check <{asm_file}> and '_t16_format_' for errors.")
# 			_bytecode_.close()
# 			exit()
# 	_bytecode_.close()



def main():
	global _argv_, _argv_lookup, v
	_argv_lookup = {
		'h': f"\nT16 assembler{version}\n  -h\tHelp\n  -v\tVerbose output/debug\n  -b\tBinary output, can be used with 'x'\n  -x\tHexadecimal output, can be used with 'b'",
		# 'b': f"{hot_val:0{bits}b}",
		# 'x': f"{hot_val:0{bits >> 2}X}",
		'v': print
	}
	
	if (argv[1][0] == '-') & (len(argv) == 4):
		_argv_ = argv[0][1:]
		if 'h' in argv[1]:
			print(_argv_lookup['h'])
			exit()
		if 'v' in argv[1]:
			v = 'v'
		_asm_ = get_asm(argv[2]) # asm[i-line] -> (op, 'oper str')
	elif len(argv) == 3:
		b = 'b'
		_asm_ = get_asm(argv[1]) # asm[i-line] -> (op, 'oper str')
	else:
		print(f"Unknown Error:: .\n\tHINT:")
		exit()
	
	_bytecode_ = open(argv[-1], 'w')
	_rc_ = get_rc(_asm_) #rc[op] -> 'fmt'
	try:
		_argv_lookup[v](_asm_,"\n",_rc_)
	except:
		0
	_t16_ = {}
	for l in _asm_.keys():
		try: # parse(('oper str', ('fmt', {}))) <- empty dict
			tmp = {}
			asm_ln = _asm_[l]
			_t16_[l] = parse((asm_ln[1], (_rc_[asm_ln[0]], tmp)))
			_bytecode_.write(f"{_t16_[l]}\n")
		except KeyError:
			print(f"KeyError:: Line {l}, in <{asm_file}>:\n\tHINT: no instruction '{_asm_[l][0]}' found in T16's isa.")
			_bytecode_.close()
			exit()
		except:
			print(f"Unknown Error:: Check <{asm_file}> and '_t16_format_' for errors.")
			_bytecode_.close()
			exit()
	_bytecode_.close()
	return print('done')

if __name__ == "__main__":
	main()
	