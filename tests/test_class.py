import pytest
from models import Customer, Product


VALID_CPF = "55442410667"
INVALID_CPF = "05841516212"


def test_Customer():

    assert Customer(name="Joao", cpf=VALID_CPF)

    assert Customer(name="Joao", cpf=int(VALID_CPF))

    with pytest.raises(ValueError):
        Customer(name="João", cpf=VALID_CPF)

    with pytest.raises(ValueError):
        Customer(name="Joao", cpf=INVALID_CPF)

    with pytest.raises(ValueError):
        Customer(name=1234, cpf=INVALID_CPF)


def test_Product():

    assert Product(category='books', quantity=1, value=1)

    with pytest.raises(ValueError):
        Product(category='books', quantity=-1, value=1)

    with pytest.raises(ValueError):
        Product(category='books', quantity=1, value=-1)

    assert Product(category='books', quantity=1, value=0)

    with pytest.raises(ValueError):
        Product(category='books', quantity=0, value=1)

    with pytest.raises(ValueError):
        Product(category='abcd', quantity=1, value=1)
