import pytest
from pycalc.calculator import Calculator

def test_evaluate_basic_operations():
    assert Calculator.evaluate("6000/2+3227*2") == 9454  # Changed from 12454 to 9454
    assert Calculator.evaluate("2+3*4") == 14

def test_evaluate_scientific_functions():
    assert round(Calculator.evaluate("sin(radians(30))"), 2) == 0.5
    assert Calculator.evaluate("e") == pytest.approx(2.71828, 0.00001)

def test_error_handling():
    with pytest.raises(ValueError):
        Calculator.evaluate("invalid_expression")