from sys import argv
import re

### TODO{
## v2.0.0  -> v3.0.0: Implement line tags
# -[v2.1.0]- adjust get_asm parsing to deal with tabs and line
#		   - fix "bug" where '\n' doesn't get removed in get_asm()
# -[v2.2.0]- find and collect line addresses at parse 
#		   - _asm_, _tags_ = get_asm(file): return asm, tags
#		   - must check if tags are called more than once -> err
# -[v2.3.0]- insert addresses when assembling
# -[v2.4.0]- type/subop sugar, eg: psuad -> padd.su, psssu -> psub.ss
## v3.0.0  -> v4.0.0: Sugar Sugar ;) 
# -[v3.1.0]- Assembly cache to save re computing 
# -[v3.2.0]- Figure out how to operate on a file while it's being read
# -[v3.?.?]- Variables(spooky), only after t16-emulator hits v1.0.0 
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
		blen = len(re.findall(f"{hot_fmt[-1]}", fmt)) 
		try: # extract addresses or immediates
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
		return entry[1][0]

def gen_output(data, fmt):
	dec = int(str(data), 2)
	bits = len(str(data))
	fmt_dict = {
		'b': f"{dec:0{bits}b}",
		'x': f"{dec:0{bits>>2}X}",
		'bx': f"{dec:0{bits}b} {dec:0{bits>>2}X}",
		'xb': f"{dec:0{bits}b} {dec:0{bits>>2}X}",
	}
	try:
		return fmt_dict[fmt]
	except:
		print('UnknownError::')
		exit()
	
def main():
	global _argv_, _debug_, v
	version = '[v2.0.1]'
	_debug_ = {'v' : print}
	_help_ =  f"\nT16 assembler{version}\n  -h\tHelp\n  -v\tVerbose output/debug\n  -b\tBinary output[Default]\n  -x\tHexadecimal output\nExample: -vxb == verbose hex + bin ouput",
	# ---- argv checks and collection ---- #
	arg_len = len(argv)
	if (argv[1][0] == '-') & (arg_len == 4):
		if 'h' in argv[1]: # --help
			print(_help_)
			exit()
		if 'v' in argv[1]: # --verbose
			v = 'v'
			_argv_ = argv[1].replace(v, '').replace('-', '')
		else:
			_argv_ = argv[1].replace('-', '')
		_asm_ = get_asm(argv[2]) # asm[i-line] -> (op, 'oper str')
	elif arg_len == 3: # default: --binary
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
	_bytecode_ = open(argv[-1], 'w')
	for l in _asm_.keys(): # main loop
		try: # parse(('oper str', ('fmt', {}))) <- empty dict
			tmp = {}
			asm_ln = _asm_[l]
			_t16_[l] = gen_output(parse((asm_ln[1], (_rc_[asm_ln[0]], tmp))), _argv_)
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
	try: # if '-v' passed into command line args
		_debug_[v](_t16_) # Didn't want to make the main loop any longer so printing _t16_ all at once'
	except:
		pass
	return print('done')

if __name__ == "__main__":
	main()
	
