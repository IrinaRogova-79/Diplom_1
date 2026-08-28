import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
from tests.conftest import INGREDIENTS_DATA


class TestBurger:
    """Тесты для класса Burger."""

    def test_set_buns_sets_bun_correctly(self, burger, mock_bun):
        """Тест: метод set_buns должен установить булочку."""
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient_adds_to_list(self, burger, mock_ingredient):
        """Тест: метод add_ingredient должен добавить ингредиент в список."""
        burger.add_ingredient(mock_ingredient)
        assert mock_ingredient in burger.ingredients

    @pytest.mark.parametrize("ingredient_data", INGREDIENTS_DATA)
    def test_add_ingredient_with_different_types(self, burger, ingredient_data):
        """Тест: добавление разных ингредиентов с помощью параметризации."""
        name, ingredient_name, price, type_ = ingredient_data
        mock_ing = Mock()
        mock_ing.get_name.return_value = ingredient_name
        mock_ing.get_price.return_value = price
        mock_ing.get_type.return_value = type_

        burger.add_ingredient(mock_ing)
        assert mock_ing in burger.ingredients

    @pytest.mark.parametrize("index, expected_length", [
        (0, 2),
        (1, 2),
        (2, 2),
    ])
    def test_remove_ingredient_changes_length_correctly(self, burger, mock_ingredient, index, expected_length):
        """Тест: метод remove_ingredient должен уменьшать длину списка."""
        ingredients = [mock_ingredient, Mock(), Mock()]
        burger.ingredients = ingredients.copy()

        burger.remove_ingredient(index)

        assert len(burger.ingredients) == expected_length

    @pytest.mark.parametrize("index", [1, 2])
    def test_remove_ingredient_keeps_other_elements(self, burger, mock_ingredient, index):
        """Тест: при удалении второго или третьего элемента, оригинальный мок остаётся."""
        ingredients = [mock_ingredient, Mock(), Mock()]
        burger.ingredients = ingredients.copy()

        burger.remove_ingredient(index)

        assert mock_ingredient in burger.ingredients

    def test_remove_ingredient_removes_first_element(self, burger, mock_ingredient):
        """Тест: при удалении первого элемента, оригинальный мок удаляется."""
        ingredients = [mock_ingredient, Mock(), Mock()]
        burger.ingredients = ingredients.copy()

        burger.remove_ingredient(0)

        assert mock_ingredient not in burger.ingredients

    @pytest.mark.parametrize("index, new_index, expected_first, expected_second, expected_third", [
        (0, 2, "ing2", "ing3", "ing1"),
        (2, 0, "ing3", "ing1", "ing2"),
        (1, 1, "ing1", "ing2", "ing3"),
        (0, 1, "ing2", "ing1", "ing3"),
        (1, 2, "ing1", "ing3", "ing2"),
    ])
    def test_move_ingredient_changes_order_correctly(self, burger, index, new_index,
                                                      expected_first, expected_second, expected_third):
        """Тест: метод move_ingredient должен правильно перемещать ингредиенты."""
        ing1 = Mock()
        ing1.get_name.return_value = "ing1"
        ing2 = Mock()
        ing2.get_name.return_value = "ing2"
        ing3 = Mock()
        ing3.get_name.return_value = "ing3"

        burger.ingredients = [ing1, ing2, ing3]

        burger.move_ingredient(index, new_index)

        result_names = [ing.get_name() for ing in burger.ingredients]
        assert result_names == [expected_first, expected_second, expected_third]

    @pytest.mark.parametrize("bun_price, ingredient1_price, ingredient2_price, expected_price", [
        (100.0, 50.0, 150.0, 400.0),
        (80.0, 30.0, 40.0, 230.0),
        (120.0, 0.0, 0.0, 240.0),
    ])
    def test_get_price_calculates_correctly(self, burger, mock_bun, bun_price,
                                            ingredient1_price, ingredient2_price, expected_price):
        """Тест: метод get_price должен правильно рассчитывать стоимость."""
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)

        ing1 = Mock()
        ing1.get_price.return_value = ingredient1_price
        ing2 = Mock()
        ing2.get_price.return_value = ingredient2_price

        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)

        assert burger.get_price() == expected_price

    @pytest.mark.parametrize("bun_name, ingredient_name, ingredient_type, ingredient_price, expected_receipt", [
        (
            "black bun", "hot sauce", "SAUCE", 50.0,
            "(==== black bun ====)\n= sauce hot sauce =\n(==== black bun ====)\n\nPrice: 250.0"
        ),
        (
            "white bun", "cutlet", "FILLING", 150.0,
            "(==== white bun ====)\n= filling cutlet =\n(==== white bun ====)\n\nPrice: 350.0"
        ),
    ])
    def test_get_receipt_with_single_ingredient(self, burger, bun_name, ingredient_name,
                                                ingredient_type, ingredient_price, expected_receipt):
        """Тест: метод get_receipt должен формировать правильный чек с одним ингредиентом."""
        mock_bun = Mock()
        mock_bun.get_name.return_value = bun_name
        mock_bun.get_price.return_value = 100.0
        burger.set_buns(mock_bun)

        mock_ing = Mock()
        mock_ing.get_name.return_value = ingredient_name
        mock_ing.get_price.return_value = ingredient_price
        mock_ing.get_type.return_value = ingredient_type

        burger.add_ingredient(mock_ing)

        assert burger.get_receipt() == expected_receipt

    @pytest.mark.parametrize("ingredients_data", [
        [("hot sauce", "SAUCE", 50.0), ("cutlet", "FILLING", 150.0)],
        [("sour cream", "SAUCE", 30.0), ("cheese", "FILLING", 80.0)],
        [("bacon", "FILLING", 120.0), ("spicy", "SAUCE", 40.0)],
    ])
    def test_get_receipt_with_multiple_ingredients(self, burger, mock_bun, ingredients_data):
        """Тест: метод get_receipt с несколькими ингредиентами."""
        burger.set_buns(mock_bun)
        bun_name = mock_bun.get_name()
        bun_price = mock_bun.get_price()

        total_price = 0
        receipt_lines = [f"(==== {bun_name} ====)"]

        for ing_name, ing_type, ing_price in ingredients_data:
            mock_ing = Mock()
            mock_ing.get_name.return_value = ing_name
            mock_ing.get_price.return_value = ing_price
            mock_ing.get_type.return_value = ing_type
            burger.add_ingredient(mock_ing)
            total_price += ing_price
            receipt_lines.append(f"= {ing_type.lower()} {ing_name} =")

        receipt_lines.append(f"(==== {bun_name} ====)\n")
        receipt_lines.append(f"Price: {bun_price * 2 + total_price}")

        expected_receipt = "\n".join(receipt_lines)
        assert burger.get_receipt() == expected_receipt

    @pytest.mark.parametrize("bun_price", [100.0, 150.0, 200.0])
    def test_get_price_with_multiple_ingredients(self, burger, mock_bun, bun_price):
        """Тест: расчет цены с несколькими ингредиентами."""
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)

        ingredient_prices = [30.0, 40.0, 50.0]
        expected_price = bun_price * 2

        for price in ingredient_prices:
            mock_ing = Mock()
            mock_ing.get_price.return_value = price
            burger.add_ingredient(mock_ing)
            expected_price += price

        assert burger.get_price() == expected_price

    def test_get_price_without_bun_raises_error(self, burger, mock_ingredient):
        """Тест: метод get_price должен выбрасывать ошибку, если булочка не установлена."""
        burger.add_ingredient(mock_ingredient)
        with pytest.raises(AttributeError):
            burger.get_price()

    def test_get_receipt_without_bun_raises_error(self, burger, mock_ingredient):
        """Тест: метод get_receipt должен выбрасывать ошибку, если булочка не установлена."""
        burger.add_ingredient(mock_ingredient)
        with pytest.raises(AttributeError):
            burger.get_receipt()

    @pytest.mark.parametrize("bun_name, expected_first_line", [
        ("black bun", "(==== black bun ====)"),
        ("white bun", "(==== white bun ====)"),
        ("sesame bun", "(==== sesame bun ====)"),
    ])
    def test_get_receipt_first_line_correct(self, burger, bun_name, expected_first_line):
        """Тест: проверка первой строки чека с разными названиями булочек."""
        mock_bun = Mock()
        mock_bun.get_name.return_value = bun_name
        mock_bun.get_price.return_value = 100.0
        burger.set_buns(mock_bun)

        receipt = burger.get_receipt()
        first_line = receipt.split("\n")[0]
        assert first_line == expected_first_line