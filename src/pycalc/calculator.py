import math

class Calculator:
    @staticmethod
    def evaluate(expression):
        try:
            expression = expression.replace('μ', '1e-6')
            eval_globals = {
                'sin': math.sin,
                'e': math.e,
                'radians': math.radians,
            }
            result = eval(expression, {'__builtins__': None}, eval_globals)
            return int(result) if isinstance(result, float) and result.is_integer() else result
        except Exception:
            raise ValueError("Invalid expression")