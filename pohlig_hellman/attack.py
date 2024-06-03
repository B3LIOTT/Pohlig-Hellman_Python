from math import sqrt
from time import perf_counter
from functools import reduce
from sympy.ntheory.modular import crt 
from pollard import factorize_with_pollard
from utils import *
import sys


def read_params_from_file(filename: str):
  a, b, p = 0, 0, 0
  try:
    with open(filename, 'r') as f:
      lines = f.readlines()
      for line in lines:
        if line.startswith("a"):
          a = int(line.split("=")[1])
        elif line.startswith("b"):
          b = int(line.split("=")[1])
        elif line.startswith("p"):
          p = int(line.split("=")[1])
        
      if a == 0 or b == 0 or p == 0:
        print("Invalid file format")
        sys.exit(1)

      return a, b, p
  except FileNotFoundError:
    print(f"File {filename} not found")
    sys.exit(1)
  except Exception as e:
    print(f"Error while parsing file {filename}: {e}")
    sys.exit(1)


def inverse_of(x: int, n: int):
  try:
    return pow(x,-1,n)
  except ValueError:
    raise NotInversibleException(f"[!] {x} has no inverse mod {n}")


def chinese_remainder(congruences, moduli):
  return crt(moduli, congruences)[0]


def pohlig_hellman(a, b, p):
  moduli, congruences = [], []

  print("_________Starting attack_________")
  print("Prime factorization...")
  try:
    factorization = factorize(p-1)
  except TooBadFactorization:
    print(f"Prime factorization of {p-1} isn't a small primes factorization (you can add more primes in the SMALL_PRIMES list)")
    test_pollard = input("Do you want to test Pollard's p-1 algorithm (it has many chances to fail/take too long time)? (y/n): ")
    if test_pollard == 'y':
      factorization = factorize_with_pollard(p-1)
    else:
      sys.exit(1)

  length = len(factorization)
  count = 0
  for q, r in factorization:
    print(f"{(100*count)//length}%")
    moduli.append(q ** r)

    x = [0]*r
    beta = [b] + [0]*(r-1)

    for i in range(r):
      lhs = pow(beta[i], (p - 1) // q ** (i + 1), p)
      for k in range(q):
        rhs = pow(a, k * (p - 1) // q, p)
        if lhs == rhs: x[i] = k; break

      if i + 1 < r:
        try:
          inv = inverse_of(pow(a, x[i] * q ** i, p), p)
        except NotInversibleException:
          print(f"[!] {pow(a, x[i] * q ** i, p)} has no inverse mod {p}")
          sys.exit(1)

        beta[i + 1] = (beta[i] * inv) % p

    congruent_to_x = reduce(lambda ac, p, q=q: ac + p[0] * q ** p[1], zip(x, range(r)), 0)
    congruences.append(congruent_to_x)
    count += 1

  return chinese_remainder(congruences, moduli)



if __name__ == '__main__':
  print('____Pohlig-Hellman attack____')
  print('Options:\n\t1 - read argv values')
  print('\t2 - read file')

  a, b, p = 0, 0, 0

  choice =int(input('Your choice: '))
  if choice == 1:
    if len(sys.argv) != 4:
      print('Usage: attack.py <b> <a> <p>')
      print('For the equation:  = a^x mod p')
      sys.exit(0)

    b = int(sys.argv[1])
    a = int(sys.argv[2])
    p = int(sys.argv[3])

  elif choice == 2:
    filename = input("Enter filename: ")
    a, b, p = read_params_from_file(filename)

  else:
    print('Invalid Choice')
  
  res = pohlig_hellman(a, b, p)
  print("\nAttack done:")
  print(f"x = {res}")
  print('_'*20)
  print(f"\nChecking the result: ")
  print('Expected: ', b)
  print("\nGot: ", pow(a, res, p))
