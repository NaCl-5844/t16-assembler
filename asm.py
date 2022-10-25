from sys import argv
import re, math

script, asm_file, bin_txt = argv #variables extracted from shell

_t16_format_ = '_t16_format_'
_t16_bwidth = 16
_t16_brange = [range(-2**_t16_bwidth, (2**_t16_bwidth)-1)]
_t16_sregs, _t16_fregs, _t16_vregs = (8, 8, 8)
_t16_misc = {
	'k': 0,					# peeK mask
	'p': 1,					# poP mask
	'$': 'NOT IMPLEMENTED',	# Variable indicator - of I wanna go that far
}

#linked dict stricture:
#dict_a[dict_b[dict_a[x][0]]] -> ((dict_c adr), [data_1, data_2,...])



def get_asm():
	with open(asm_file, 'r') as f:
		asm = {k: (v.split(' ', 1)[0], re.split(' \n| ;', v.split(' ', 1)[1])[0]) for k, v in enumerate(f) if len(v.split()) >= 3}
		return asm #final .split(', ') removed to preserve order

def get_refcache():
	with open(_t16_format_) as f:
		rc = {ln.split()[0]: ln.split()[1] for ln in f if len(ln.split()) > 1}
	#generate dictionary {command: (format, oprand bits)}
	refcache = {v[0]: rc[v[0]].replace('-', '') for v in _asm_.values()}
	return refcache #rc[op] -> {qsfmt, [operand list]}

def parse(entry): # entry = ('op,er,an,ds', ('fmt', {}))
	if len(re.findall('M|N|C|B|A', entry[1][0])) > 0:

		# one or more operand to be processed
		print(entry)
		opr_dic = entry[1][1]
		fmt = entry[1][0]
		print(entry[0])
		entry_opr = entry[0].rsplit(', ', 1)
		print('--rsplit--')
		print(entry_opr)
		hot_opr = entry_opr[-1]
		blen = len(re.findall(f"{fmt[-1]}", fmt))
		print('hot opr 0: ', hot_opr)
		print('blen:', blen)
		try:
			hot_val = int(re.sub('[a-zA-Z|\n]', '', hot_opr))
			1/(abs(hot_val)+(hot_val))
			print(hot_val, 'hot_operand is >0')
			opr_dic[fmt[-1]] = f"{hot_val:0{int(blen)}b}"
		except ZeroDivisionError:
			hot_val = int(re.sub('[a-zA-Z|\n]', '', hot_opr))
			print(hot_val, 'hot_operand is <1')
			if hot_val != 0:
				opr_dic[fmt[-1]] = bin(((1<<blen)-1)-(~hot_val))[2:]
			else:
				opr_dic[fmt[-1]] = f"{hot_val:0{int(blen)}b}"
		except:
			try:
				hot_val = re.sub('[ |\n]', '', hot_opr)
				print('hot_val,',hot_val,'is string?')
				opr_dic[fmt[-1]] = _t16_misc[hot_val]
			except: #learn how to give accurate error messages
				print(f"please check assembly file for errors.\n\tHINT: Err in {entry}")
				return exit()
			
		print(opr_dic[fmt[-1]])
		fmt = fmt.replace(fmt[-1], '')
		print('--ret--')
		return parse((entry_opr[0], (fmt, opr_dic)))
	else: # entry = ('op,er,an,ds', ('fmt', {}))
		entry[1][1]['X'] = entry[1][0]
		return entry[1][1]
	



def main():
	global _asm_, _rc_
	_asm_ = get_asm()		#asm[i-line] -> (op, 'oper str')
	_rc_ = get_refcache()	#rc[op] -> (fmt, [operand list])
	_t16_ = {}
	### DO NOT MODIFY _ASM_ OR _RC_. THEY ARE GLOBAL. ###
	print([_rc_[_asm_[a][0]] for a in _asm_])
	for l in _asm_.keys(): 	
		tmp = {}
		#parse(('oper str', ('fmt', {}))) <- empty dict
		_t16_[l] = ((_rc_[_asm_[l][0]], parse((_asm_[l][1], (_rc_[_asm_[l][0]], tmp)))))
	print(_t16_)
	return print('done')
	
main()