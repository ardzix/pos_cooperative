# http://stackoverflow.com/questions/561486/how-to-convert-an-integer-to-the-shortest-url-safe-string-in-python?lq=1
import string

ALPHABET            = string.ascii_uppercase + string.ascii_lowercase + string.digits
ALPHABET_REVERSE    = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE                = len(ALPHABET)
SIGN_CHARACTER      = '$'

def base62_encode(n):
    if n < 0:
        return SIGN_CHARACTER + num_encode(-n)
    
    s = []
    
    while True:
        n, r = divmod(n, BASE)
        s.append(ALPHABET[r])
        
        if n == 0:
            break
    
    return ''.join(reversed(s))

def base62_decode(s):
    if s[0] == SIGN_CHARACTER:
        return -num_decode(s[1:])
    
    n = 0
    
    for c in s:
        n = n * BASE + ALPHABET_REVERSE[c]
    
    return n