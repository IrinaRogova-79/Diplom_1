import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_bun():
    bun = Mock()
    bun.get_name.return_value = "black bun"
    bun.get_price.return_value = 100.0
    return bun

@pytest.fixture
def mock_ingredient():
    ingredient = Mock()
    ingredient.get_name.return_value = "sauce"
    ingredient.get_price.return_value = 50.0
    ingredient.get_type.return_value = "SAUCE"
    return ingredient

@pytest.fixture
def burger():
    from praktikum.burger import Burger
    return Burger()

INGREDIENTS_DATA = [
    ("sauce", "hot sauce", 50.0, "SAUCE"),
    ("filling", "cutlet", 150.0, "FILLING"),
    ("sauce", "sour cream", 30.0, "SAUCE"),
    ("filling", "cheese", 80.0, "FILLING"),
]