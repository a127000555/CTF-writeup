from sage.all import *
from sage.rings.finite_rings.integer_mod import square_root_mod_prime   # sqrt() uses brute force for small p
print(square_root_mod_prime(mod(5,7)))