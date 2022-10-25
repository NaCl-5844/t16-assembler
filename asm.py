from sys import argv
import re

script, asm_file, bin_txt = argv #variables extracted from shell

_t16_format_ = '_t16_format_'
_t16_bwidth = 16
_t16_sregs, _t16_fregs, _t16_vregs = (8, 8, 8)
_t16_misc = {
	'k': 0,					# peeK mask
	'p': 1,					# poP mask
	'$': 'NOT IMPLEMENTED',	# Variable indicator - if I go that far
}

def get_asm():
	with open(asm_file, 'r') as f:
		asm = {k: (v.split(' ', 1)[0], re.split(' \n| ;', v.split(' ', 1)[1])[0]) for k, v in enumerate(f) if len(v.split()) >= 3}
		return asm #final .split(', ') removed to preserve order

def get_refcache():
	with open(_t16_format_) as f:
		rc = {ln.split()[0]: ln.split()[1] for ln in f if len(ln.split()) > 1}
	#generate dictionary {command: format}
	refcache = {v[0]: rc[v[0]].replace('-', '') for v in _asm_.values()}
	return refcache #refcache[op] -> fmt

def parse(entry): # entry = ('op,er,an,ds', ('fmt', {}))
	if len(re.findall('M|N|C|B|A', entry[1][0])) > 0:
	# one or more operand to be processed
		opr_dic = entry[1][1]
		fmt = entry[1][0]
		entry_opr = entry[0].rsplit(', ', 1)
		hot_opr = entry_opr[-1]
		blen = len(re.findall(f"{fmt[-1]}", fmt))
		try:
			hot_val = int(re.sub('[a-zA-Z|\n]', '', hot_opr)) # <-- gets calculated regardless of exception
			1/(abs(hot_val)+(hot_val)) #if val is +ve, 1/2*val else 1/0
			# -ve values are exceedingly rare as only immediates use them
			opr_dic[fmt[-1]] = f"{hot_val:0{int(blen)}b}"
		except ZeroDivisionError:
			if hot_val != 0: # -ve values get bitmasked before being converted to binary
				opr_dic[fmt[-1]] = f"{((1<<blen)-1)-(~hot_val):0{int(blen)}b}"
			else: # If 0. I don't like how my (duck?) method exclude r0
				opr_dic[fmt[-1]] = f"{hot_val:0{int(blen)}b}"
		except:
			try:
				hot_val = re.sub('[ |\n]', '', hot_opr)
				opr_dic[hot_val] = str(_t16_misc[hot_val])
				return parse((entry_opr[0], (fmt, opr_dic)))
			except: #learn how to give more + accurate error messages
				print(f"please check assembly file for errors.\n\tHINT: Err in {entry}")
				return exit()
		fmt = fmt.replace(fmt[-1], '')
		return parse((entry_opr[0], (fmt, opr_dic)))
	else: # entry = ('op,er,an,ds', ('fmt', {}))
		entry[1][1]['X|S|F'] = entry[1][0]
		return entry[1][1]

def main():
	global _asm_, _rc_
	_asm_ = get_asm()		#asm[i-line] -> (op, 'oper str')
	_rc_ = get_refcache()	#rc[op] -> 'fmt'
	_t16_ = {}
	_bytecode_ = open(bin_txt, 'w')
	for l in _asm_.keys(): 	
		tmp = {}
		#parse(('oper str', ('fmt', {}))) <- empty dict
		#output[l] = 't16 bytecode'
		_t16_[l] = ((_rc_[_asm_[l][0]], parse((_asm_[l][1], (_rc_[_asm_[l][0]], tmp)))))
		_t16_[l] = ''.join(list(reversed(_t16_[l][1].values())))
		_bytecode_.write(f"{_t16_[l]}\n")
	_bytecode_.close()
	print(f"\nReference cache:\n{_rc_}\nT16 bytecode:\n{_t16_}")
	return print('done')
	
main()