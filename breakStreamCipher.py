import binascii
import re
import sys


def xor(s1,s2,is_hex=True):
	if len(s1) != len(s2):
		return
	if is_hex:
		s1 = binascii.unhexlify(s1)
		s2 = binascii.unhexlify(s2)
	s3 = bytes([s1[i]^s2[i] for i in range(len(s1))])
	if is_hex:
		s3 = binascii.hexlify(s3)
	return s3

def get_warning(text):
	arr = []
	pat = re.compile('<p class="warning">(.*?)</p>')
	for match in re.finditer(pat,text):
		arr.append(match.group(1))
		#print(match.group(1))
	return arr

FREQCT = None
def generate_freqct():
	global FREQCT
	if FREQCT is not None:
		return FREQCT
	freqct = {
		'e':21912,
		't':16587,
		'a':14810,
		'o':14003,
		'i':13318,
		'n':12666,
		's':11450,
		'r':10977,
		'h':10795,
		'd':7874,
		'l':7253,
		'u':5246,
		'c':4943,
		'm':4761,
		'f':4200,
		'y':3853,
		'w':3819,
		'g':3693,
		'p':3316,
		'b':2715,
		'v':2019,
		'k':1257,
		'x':315,
		'q':205,
		'j':188,
		'z':128,
		' ':40000,
		'.':4000,
	}

	for ch in 'abcdefghijklmnopqrstuvwxyz':
		freqct[ch.upper()] = freqct[ch]

	_freqct = {}
	for ch in range(256):
		if chr(ch) not in freqct:
			_freqct[ch] = 1
		else:
			_freqct[ch] = freqct[chr(ch)]

	freqct = _freqct

	s = sum(freqct.values())
	freqct = dict((ch,256.*freqct[ch]/s) for ch in freqct)
	FREQCT = freqct
	return freqct

def score_ascii(st):
	freqct = generate_freqct()
	score = 1.
	for ch in st:
		score = score * freqct[ch]
	return score

if len(sys.argv) != 2:
    print("This script expects a single input specifying a file. This file must meet the following condition: ")
    print("\t 1. Every line contains one entry")
    print("\t 2. Every line is encoded in hex")
    print("\t 3. Every line contains valid ascii symbols encrypted with the same stream cipher key stream")
    print(" If all these conditions are met, this script should produce the plain text for all these strings")

filename = sys.argv[1]
fileHandler = open(filename, "r")

ciphertexts = fileHandler.read()
ciphertexts = ciphertexts.strip().split()

ciphertexts = [binascii.unhexlify(ct) for ct in ciphertexts]
#print(ciphertexts)
key_solve = []
max_len=max(len(ct) for ct in ciphertexts)
#max_len=1
for pos in range(max_len):
    max_score = 0
    ans = None
    for k in range(256):
        plain_chars = [ct[pos]^k for ct in ciphertexts if len(ct) > pos]
        sc = score_ascii(plain_chars)
        if sc > max_score:
            max_score = sc
            ans = k
    key_solve.append(ans)
key_solve = bytes(key_solve)
    
for ct in ciphertexts:
    print(xor(key_solve[:len(ct)],ct,is_hex=False))
print(key_solve)
print(len(key_solve))
#return key_solve
