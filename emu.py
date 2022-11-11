from sys import argv

version = '[v0.1.2]'
# [LOG]: working towards extracting binaries into the 32 mem width 

### TODO{
## v0.0.0 to v0.5.0 will only implement: 
## - stages?: single cycle
## - mem?	: ram, iq[instruction queue], import bytecode to rom
## - units?	: scalar, pc
## - trace?	: no bus tracing, possible ram and/or register tracing
# -[v0.1.0]- implement configuration of cpu internal states
# -[v0.2.0]- initialise rom with bytecode file from commandline  
# -[v0.3.0]- initialise pc and iq. Implement simple prefetching
# -[v0.4.0]- simple arithmetic, boolean, shifts and register moves
# -[v0.5.0]- ram access and all but complex arithmetic scalar instructions
# -[v0.6.0]- complex scalar
# -[v0.7.0]- simple floating point instructions
# -[v0.8.0]- simple vector instructions
# -[v0.9.0]- verbose logging and printout
# -[v1.0.0]- ALL ABOVE IMPLEMENTED AND BUG CHECKED
###}


#--------config--------#
# NOTE:
# - first 2KB of memory addressing will be assigned to ROM
# - scalar registers[sr] are 16-bit + 2-bit flags, can be read/write independamtly(doesn't change the code much)

_t16_conf = { 
	'flags':{'sr':2, 'fp':3, 'vx':3, 'pc':1, 'cr':1, 'l1i':1}, # 
	'srf'  :{'bit':16, 'sr':16, 'pc':2, 'cr':16, 'mo':8}, # (byte capacity) // Scalar Register Files
	'xrf'  :{'bit':32, 'line':16, 'vx':32, 'fp':32}, # (byte capacity) // eXtended Register Files
	'mem'  :{'bit':32, 'line':16, 'ram':256, 'iq':16, 'rom':0,}, # (byte capacity) // standard MEMory
	'cam'  :{'bit':32, 'line':16, 'l1d':(128, 4), 'l1i':(128, 8)}, # (byte capacity, associativity) // CAche Memory
	'bus'  :{'bit':32,},
	'unit' :{},
}

# bus = { # <data bus>[bus] = {data:"", source:"", destination:""}
# 	sc_mb:{}, 
# 	vx_mb:{},	
# 	fp_mb:{},
# 	mb_l1d:{},
# 	mb_ram:{},
# 	l1d_ram:{},
# 	l1i_ram:{},
# }

# unit = { # <func unit>[unit] = {op:>function name>}
# 	scu:{},
# 	vxu:{},
# 	fpu:{},
# }


#--------init memory structures--------#

def init_scalar_mem(entry): # Initialise: SCalar Memory
	sr = list(entry.keys())[1:]
	hexbits = entry['bit'] >> 2
	for e in sr: # entry[e] == capacity
		entry[e] = {x:f"{0:0{hexbits}X}" for x in range(0, entry[e] >> 1)}
	return entry
	
def init_extended_mem(entry): # Initialise: Memory and eXtended Registers
	mxr = list(entry.keys())[2:]
	cline = entry['line']
	hexbits = entry['bit'] >> 2
	for e in mxr: # entry[e] == capacity
		sets = int(entry[e]/cline) # $ = capacity / (1 way * cache line size) // 1 way == direct mapped. 1*x=x
		entry[e] = {f"${cl}":{x:f"{0:0{hexbits}X}" for x in range(0, cline >> 2)} for cl in range(0, sets)}
	return entry

def init_register_flags(entry):
	pass

def init_cache_mem(entry): # Initialise: CAche Memory
	csh = list(entry.keys())[2:]
	cline = entry['line']
	hexbits = entry['bit'] >> 2
	for e in csh: # entry[e] == capacity
		ways = entry[e][1] # % = ways. used by caching algorithm(s)
		sets = int(entry[e][0]/(ways*cline)) # $ = capacity / (ways * cache line size)
		entry[e] = {f"%{w}":{f"${cl}":{x:f"{0:0{hexbits}X}" for x in range(0, cline >> 2)} for cl in range(0, sets)} for w in range(0, ways)}
	return entry



srf = init_scalar_mem(_t16_conf['srf'])
# xrf = init_extended_mem(_t16_conf['xrf'])
mem = init_extended_mem(_t16_conf['mem'])
# cam = init_cache_mem(_t16_conf['cam'])

print("\nscm:\n", srf)
# print("\nmxr:\n", xrf)
print("\nmem:\n", mem)
# print("\ncam:\n", cam)

#--------init rom--------#
# load default rom files - added over time and addressed directly to save argv space.
# load assembly file
# generate reference cache
# line by line, parse to hex -> insert to rom @specific address
# when program(s) are loaded, initiate boot sequence
# jump to program address and execute.






#--------init functional units--------#






#--------state--------#







def join2(entry):
	hot_list, hot_dict = entry
	items = len(hot_list)
	if items > 1: # if i > 1: pair up data in 32-bit words
		hot_dict[len(hot_dict.keys())] = f"{hot_list[1]}{hot_list[0]}"
		return join2((hot_list[2:], hot_dict))
	elif items == 1: # mask zero onto lone leftover data
		bits = len(str(hot_list[0]))<<1 # x<<1 == x*2
		hot_dict[len(hot_dict.keys())] = f"{int(str(hot_list[0]),16):0{bits}X}"
		return hot_dict
	else:
		return hot_dict

def join2sped(entry):
	hot_list, hot_dict = entry
	items = len(hot_list)
	try: # if i > 1: pair up data in 32-bit words
		hot_dict[len(hot_dict.keys())] = f"{hot_list[1]}{hot_list[0]}"
		return join2sped((hot_list[2:], hot_dict))
	except KeyError: # mask zero onto lone leftover data
		bits = len(str(hot_list[0]))<<1 # x<<1 == x*2
		hot_dict[len(hot_dict.keys())] = f"{int(str(hot_list[0]),16):0{bits}X}"
		return hot_dict
	except:
		return hot_dict


# file = ['f',1,2,3,4,5,6,7,8]

with open('out.txt', 'r') as f:
	file = [ln.replace('\n', '') for ln in f]
print(file)
my_dict = join2((file, {}))
key = my_dict.keys()
print(my_dict, key)
