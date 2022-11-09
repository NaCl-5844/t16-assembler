from sys import argv
import re

### TODO{
## v1.4.0:
# - output format[bx] can use both formats side by side, eg 1100110011001100 CCCC
## v1.5.0:
# - add a way to convert output files between binary and hex 
## v2.0.0 == v.1.5.x has all features finished and debugged
### }

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
	with open('_t16_format_', 'r') as f:
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
		try: # if '-v' passed into command line args
			_debug_[v](entry)
		except:
			pass
		opr_dic = entry[1][1]
		entry_opr = entry[0].rsplit(', ', 1)
		hot_opr = entry_opr[-1]
		blen = len(re.findall(f"{hot_fmt[-1]}", fmt)) ### >> 2 if option = '-x'
		try:
			hot_val = int(re.sub('[a-zA-Z|\n]', '', hot_opr)) # <-- gets calculated regardless of exception
			hot_val>>hot_val # -ve shifts generate a ValueError
			opr_dic[hot_fmt[-1]] = f"{hot_val:0{int(blen)}b}" 
		except ValueError: # -ve values get sign extended  ## -ve values are rare as only immediates use them
			opr_dic[hot_fmt[-1]] = f"{((1<<blen)-1)-(~hot_val):0{int(blen)}b}"
		except:
			try: # string supplied as operand is searched in _t16_misc to find it's binary value
				_t16_misc = {
					'k': 0,					# peeK mask
					'p': 1,					# poP mask
					'$': 'NOT IMPLEMENTED',	# Variable indicator - if I go that far
				}
				hot_val = re.sub('[ |\n]', '', hot_opr)
				opr_dic[hot_fmt[-1]] = str(_t16_misc[hot_val])
			except Exception: #learn how to give more + accurate error messages
				print(f"Unknown Error:: Check assembly file for errors.\n\tHINT: Err in parse({entry})")
				exit()
		fmt = fmt.replace(hot_fmt[-1], '', (blen-1)).replace(hot_fmt[-1], opr_dic[hot_fmt[-1]])
		return parse((entry_opr[0], (fmt, opr_dic)))
	else: # entry = ('op,er,an,ds', ('fmt', {}))
		try: # if '-v' passed into command line args
			_debug_[v](entry)
		except:
			pass
		# _bin_ = 'poopyhead' # entry[1][0]
		# print(_bin_)
		# bits = len(_bin_) >> 2
		# _bytecode_ = _argv_lookup[_argv_]
		return entry[1][0]

def binconcat(n, arg):
	return print()
	
def main():
	global _argv_, _debug_, v
	version = '[v1.3.2]'
	_debug_ = {'v' : print}
	_argv_data = {
		# 'ibits': 0,
		# '_bin_': 0,
		# 'b' : _argv_data['_bin_'],
		# 'x' : f"{_argv_data['_bin_'], 2:0{_argv_data['ibits']>>2}X}",
		# 'xb': f"{_argv_data['_bin_'], 2:0{_argv_data['ibits']>>2}X} {_bin_}",
		# 'bx': f"{_bin_} {_argv_data['_bin_'], 2:0{_argv_data['ibits']>>2}X}",
		# 'h' : f"\nT16 assembler{version}\n  -h\tHelp\n  -v\tVerbose output/debug\n  -b\tBinary output[Default]\n  -x\tHexadecimal output\nExample: -vxb == verbose hex + bin ouput",
	}
	# ---- argv checks and collection ---- #
	if (argv[1][0] == '-') & (len(argv) == 4):
		if 'h' in argv[1]: # --help
			print(_argv_misc['h'])
			exit()
		if 'v' in argv[1]: # --verbose
			v = 'v'
			_argv_ = argv[1].replace(v, '').replace('-', '')
		else:
			_argv_ = argv[1].replace('-', '')
		print(_argv_)
		_asm_ = get_asm(argv[2]) # asm[i-line] -> (op, 'oper str')
	elif len(argv) == 3: # default: --binary
		_argv_ = 'b'
		_asm_ = get_asm(argv[1]) # asm[i-line] -> (op, 'oper str')
	else:
		print(f"Unknown Error:: .\n\tHINT:")
		exit()
	
	# ---- parse and write _bytecode_ to file ---- #
	_rc_ = get_rc(_asm_) #rc[op] -> 'fmt'
	try: # if '-v' passed into command line args
		_debug_[v](f"Argv:\n{argv}\nAssembly:\n{_asm_}\nReference Cache:\n{_rc_}")
	except:
		pass
	_t16_ = {}
	_argv_data = {
		
	}
	_bytecode_ = open(argv[-1], 'w')
	for l in _asm_.keys(): # main loop
		try: # parse(('oper str', ('fmt', {}))) <- empty dict
			tmp = {}
			asm_ln = _asm_[l]
			_t16_[l] = parse((asm_ln[1], (_rc_[asm_ln[0]], tmp)))
			print(binconcat(_t16_[l], _argv_))
			_bytecode_.write(f"{_t16_[l]}\n")
		except KeyError:
			print(f"KeyError:: Line {l}, in <{argv[-2]}>:\n\tHINT: no instruction '{_asm_[l][0]}' found in T16's isa.")
			_bytecode_.close()
			exit()
		except:
			print(f"Unknown Error:: Check <{argv[-2]}> and '_t16_format_' for errors.")
			_bytecode_.close()
			exit()
	_bytecode_.close()
	print(_t16_)
	return print('done')

if __name__ == "__main__":
	main()
	