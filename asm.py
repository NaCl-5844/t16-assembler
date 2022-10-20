from sys import argv
import re, math, string

script, asm_file, bin_txt = argv #variables extracted from shell
_t16_format_ = '_t16_format_'
_t16_bwidth = 16
_t16_brange = [range(-2**_t16_bwidth, (2**_t16_bwidth)-1)]
_t16_sregs, _t16_fregs, _t16_vregs = (8, 8, 8)

def get_asm(file):
	with open(asm_file) as f:
		asm = {ln.split(' ')[0]:(re.split(' \n| ;', ln)[0].replace(f"{ln.split(' ')[0]} ", '')).split(', ') for ln in f if len(ln.split()) > 1}
		return asm

with open(asm_file) as f:
	tmp = {ln.split(' ')[0]:(re.split(' \n| ;', ln)[0].replace(f"{ln.split(' ')[0]} ", '')).split(', ') for ln in f if len(ln.split()) > 1}
	print(tmp)

def gen_refcache():
	with open(_t16_format_) as f:
		_t16_ = {ln.split()[0]:ln.split()[1] for ln in f if len(ln.split()) > 1} #puts t16isa into dict
	asm_cmd = [l[0] for l in _asm_] #Extracts assembly command from list of tuples
	ref = {k:_t16_[k] for k in _t16_ if k in asm_cmd} #generate doctionary of matching keys command:format
	return ref

def opr_parse(asm, rc): 
	#unzip each unique char -> [chars, aka set()]
	in_rc = (list(set(rc[i].replace('-', ''))) for i in rc)
	print(asm)
	print(rc)
	print(in_rc)
	for a in asm:
		# oprs = {a:f"{i[1][1:]:0{rc[i].count(f'{in_rc}')}b}" for i in a if type(i[0]) == str}
		print(type(f'{a[1][0]}'))
	# print(oprs)	
	
	#decode bit range of each operand -> [max]
	# nest_asm = {:{in_rc[i][]}}
	
	#assemble, generating tuples.append((chars[x], f"{opr[1:]:0{blenth of opetand}b}"))
	#finally the tuples[1] can be joined to form the binary file.
	#Note: op code and subops must be reattached to operands
	return
	
def assemble(asm, ref):
	opr_list = ['A', 'B', 'C'] #legacy
	oper = ['r', 'f', 'v'] 
	oper_dict = {
		'N': type(int), 
		'C': oper,
		'B': oper, 
		'A': oper
	}
	print(asm)
	for a in asm:
		fmtls = ref[a[0]].split('-') #search ref for format of command t[0]
		fmt = ''.join(fmtls)
		if '' in a[1]:
			body = a[1].remove('')
		else:
			body = a[1]
		
		print(a)
		print(body)
		print(fmt)
		tmp = a[1]
		for opr in a[1]:
			if opr[0] in string.ascii_lowercase: #if scalar, vec, float
				print(tmp)
				i = tmp.index(opr)
				char = opr_list[i]
				bits = fmt.count(opr_list[i])
				print((char, bits))
				tmp.insert(i, '')
				tmp.remove(opr)
			else: #if imm
				i = tmp.index(opr)
				n = fmt.count('N')
				mx_imm = (2**n)-1
				print((opr[0],mx_imm))
				tmp.insert(i, '')
				tmp.remove(opr)
			print("\n")
	return

  
_asm_ = get_asm(asm_file)
refcache = gen_refcache()
#debugging:
# print(refcache)
# print(assemble(_asm_, refcache))
# print(list(operand_check.keys())[list(operand_check.values()).index(True)]) #return key using value↓
# opr_parse(_asm_, refcache)