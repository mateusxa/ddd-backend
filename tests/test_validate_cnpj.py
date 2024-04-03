from utils.validateCNPJ import validate_cnpj


def test_validate_cnpj():
    # CNPJs errados
    assert validate_cnpj('abcdefghijklmn') == False
    assert validate_cnpj('123') == False
    assert validate_cnpj('') == False
    assert validate_cnpj(None) == False
    assert validate_cnpj('12345678901234') == False
    assert validate_cnpj('11222333000100') == False
    
    # CNPJs corretos
    assert validate_cnpj('11222333000181') == '11.222.333/0001-81'
    assert validate_cnpj('11.222.333/0001-81') == '11.222.333/0001-81'
    assert validate_cnpj('  11 222 333 0001 81  ') == '11.222.333/0001-81'

    # CNPJs corretos
    assert validate_cnpj('11222333000181', return_formated=False) == '11222333000181'
    assert validate_cnpj('11.222.333/0001-81', return_formated=False) == '11222333000181'
    assert validate_cnpj('  11 222 333 0001 81  ', return_formated=False) == '11222333000181'

