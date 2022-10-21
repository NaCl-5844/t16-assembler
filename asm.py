from sys import argv
import re, string, math

script, asm_file, bin_txt = argv #variables extracted from shell
_t16_format_ = '_t16_format_'
_t16_bwidth = 16
_t16_brange = [range(-2**_t16_bwidth, (2**_t16_bwidth)-1)]
_t16_sregs, _t16_fregs, _t16_vregs = (8, 8, 8)

def get_asm(file):
	with open(file) as f:
		asm = [(ln.split(' ', 1)[0],re.split(' \n| ;', ln.split(' ', 1)[1])[0].split(', ')) for ln in f if len(ln.split()) > 1]
		return asm

def gen_refcache():
	with open(_t16_format_) as f:
		_t16_ = {ln.split()[0]:ln.split()[1] for ln in f if len(ln.split()) > 1} #t16isa -> dictionary
	asm_cmd = [l[0] for l in _asm_] #Extracts assembly command from list of tuples
	ref = {k:_t16_[k] for k in _t16_ if k in asm_cmd} #generate dictionary of matching keys command:format
	return ref

def opr_parse(asm, rc): 
	# print(asm) #debugging
	# print(rc) #debugging
	#unzip each unique char in position 0
	
	for op, l in asm:
		print()
		fmt = rc[op]
		chars = re.findall('N|C|B|A', fmt)
		print(f"{chars} <- chars")
		opr = {}
		opr[op] = [len(c*chars.count(c)) for c in set(chars)]
		print((op, fmt))
		print(opr)
		print(l) 
		par_list = []
		blen = opr[op]
		print(blen)
		ls = 0
		for i in l: 
			bits = blen[ls]
			# bits = 4
			print(f"test {blen[ls]}")
			try: #if first operand char is an int
				if int(i) >= 0:
					par_list.append((f"{int(i):0{bits}b}"))
				else:
					#(10**(len(i) - 1))-int(i) = 10's complement
					par_list.append((f"{((10**(len(i) - 1))-int(i)):0{bits}b}"))
			except: #else it's a string
				par_list.append((f"{int(i[1:]):0{bits}b}"))
			opr[op] = par_list
			ls += 1
			print(f"list position {bits}")
		print(f"{opr} <- after loop")
		print(par_list)
		
		
	#finally the tuples[1] can be joined to form the binary file.
	#Note: op code and subops must be reattached to operands
	return
	
def assemble(asm, rc):
	# print(asm) #debugging
	# print(rc) #debugging
	#unzip each unique char in position 0
	for op, l in asm:
		print()
		fmt = rc[op]
		chars = re.findall('N|C|B|A', fmt)
		char_set = set(chars)
		opr, tmp_d = {}, {}
		ls = (o for o in l)
		opr[op] = {c: (next(ls), len(c*chars.count(c))) for c in char_set}
		print(f"{(op, l)}\n{(op, fmt)}\t<- debug\n{chars} <- chars")
		print((opr))
		#{int(i[1:]):0{bits}b}
		#{int(k 0):0{len(k.count(k)}b}
		o_index = 0
		
		# for i in opr[op].values(): #i = bit length
		# 	print(f"{i} <- i")
		# 	try:
		# 		if int(i) >= 0:
		# 			print((f"{int(l[o_index]):0{i}b}"))
		# 		else:
		# 			#(10**(len(i) - 1))-int(i) = 10's complement
		# 			print((f"{((10**(len(l[o_index]) - 1))-int(l[o_index])):0{int(i)}b}"))
		# 	except:
		# 		print(f"{int(l[o_index][1:]):0{int(i)}b}")
		# 	o_index += 1












_asm_ = get_asm(asm_file)
refcache = gen_refcache()
#debugging:
# print(_asm_)
# print(refcache)
# print(list(operand_check.keys())[list(operand_check.values()).index(True)]) #return key using value↓

assemble(_asm_, refcache)