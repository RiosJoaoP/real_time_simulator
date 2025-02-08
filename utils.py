import math

def _lcm(a, b):
    """Calcula o MMC de dois números."""
    return abs(a * b) // math.gcd(a, b)

def least_common_multiple(numbers):
    """Calcula o MMC de uma lista de números."""
    if not numbers:
        return 0
    resultado_mmc = numbers[0]
    for numero in numbers[1:]:
        resultado_mmc = _lcm(resultado_mmc, numero)
    return resultado_mmc

# Exemplo de uso
numbers = [12, 18, 24]
result = least_common_multiple(numbers)
print(f"O MMC de {numbers} é {result}")