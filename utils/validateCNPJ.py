import re


def validate_cnpj(cnpj, return_formated=True) -> str | bool:
    """
    Valida CNPJs, retornando apenas a string de números válida.
    
    # CNPJs errados
    >>> validate_cnpj('abcdefghijklmn')
    False
    >>> validate_cnpj('123')
    False
    >>> validate_cnpj('')
    False
    >>> validate_cnpj(None)
    False
    >>> validate_cnpj('12345678901234')
    False
    >>> validate_cnpj('11222333000100')
    False
    
    # CNPJs corretos
    >>> validate_cnpj('11222333000181')
    '11222333000181'
    >>> validate_cnpj('11.222.333/0001-81')
    '11222333000181'
    >>> validate_cnpj('  11 222 333 0001 81  ')
    '11222333000181'
    """
    cnpj = ''.join(re.findall(r'\d', str(cnpj)))
    
    if (not cnpj) or (len(cnpj) < 14):
        return False
    
    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
    inteiros = [int(char) for char in cnpj]
    novo = inteiros[:12]
    
    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x*y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)
    
    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        if return_formated:
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[-2:]}"
        return cnpj
    return False