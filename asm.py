from sys import argv
import re, math, string

script, asm_file, bin_txt = argv #variables extracted from shell
_t16_format_ = '_t16_format_'
_t16_bwidth = 16
_t16_brange = [range(-2**_t16_bwidth, (2**_t16_bwidth)-1)]
_t16_sregs, _t16_fregs, _t16_vregs = (8, 8, 8)

def get_t16():
	with open(_t16_format_) as f:
		t16 = {}
		for ln in f: #Loop generates dictionary. keys:values = t16's op (name:format)
			opf = [ln][0].split(' ', 1)
			if len(opf) == 2:
				t16[opf[0]] = opf[1].replace('\n', '').replace(' ', '')
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
	with open(_t16_format_) as f:
		t16 = {}
		for ln in f: #Loop generates dictionary. keys:values = t16's op (name:format)
			opf = [ln][0].split(' ', 1)
			if len(opf) == 2:
				t16[opf[0]] = opf[1].replace('\n', '').replace(' ', '')
		_t16_ = t16
	asm_cmd = [l[0] for l in _asm_] #Extracts assembly command from list of tuples
	ref = {k:_t16_[k] for k in _t16_ if k in asm_cmd} #generate doctionary of matching keys command:format
	return ref
	
def charsum(val, ls):
	n = 0
	for i in ls:
		if i == val:
			n += 1
	return n
	
def opr_parse(operands, body): #XXXXXX-CCC-BBB-AAA
	#unzip each unique char -> [chars, aka set()
	#decode bit range of each operand -> [max]
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
				bits = charsum(char, fmt)
				print((char, bits))
				tmp.insert(i, '')
				tmp.remove(opr)
			else: #if imm
				i = tmp.index(opr)
				n = charsum('N', fmt)
				mx_imm = (2**n)-1
				print((opr[0],mx_imm))
				tmp.insert(i, '')
				tmp.remove(opr)
			print("\n")
	return

  
_asm_ = get_asm(asm_file)
_t16_ = get_t16()
refcache = gen_refcache()
#debugging:
# print(_asm_)
# print(refcache)
print(assemble(_asm_, refcache))
# print(list(operand_check.keys())[list(operand_check.values()).index(True)]) #return key using value↓
