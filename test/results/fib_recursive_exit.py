def fib(n):
  if n <= 1:
    return n
  return fib(n - 1) + fib(n - 2)
resultado = 0
resultado = fib(6)
print(resultado)
