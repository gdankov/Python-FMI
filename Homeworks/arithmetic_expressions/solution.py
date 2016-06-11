from numbers import Number


class Constant:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if(isinstance(other, Constant)):
            return Constant(self.value + other.value)
        elif isinstance(other, Number):
            return Constant(self.value + other)
        else:
            return NotImplemented

    def __radd__(self, other):
        return Constant.__add__(self, other)

    def __sub__(self, other):
        if(isinstance(other, Constant)):
            return Constant(self.value - other.value)
        elif isinstance(other, Number):
            return Constant(self.value - other)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if(isinstance(other, Constant)):
            return Constant(other.value - self.value)
        elif isinstance(other, Number):
            return Constant(other - self.value)
        else:
            return NotImplemented

    def __mul__(self, other):
        if(isinstance(other, Constant)):
            return Constant(self.value * other.value)
        elif isinstance(other, Number):
            return Constant(self.value * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return Constant.__mul__(self, other)

    def __truediv__(self, other):
        if(isinstance(other, Constant)):
            return Constant(self.value / other.value)
        elif isinstance(other, Number):
            return Constant(self.value / other)
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        if(isinstance(other, Constant)):
            return Constant(other.value / self.value)
        elif isinstance(other, Number):
            return Constant(other / self.value)
        else:
            return NotImplemented

    def __floordiv__(self, other):
        if(isinstance(other, Constant)):
            return Constant(self.value // other.value)
        elif isinstance(other, Number):
            return Constant(self.value // other)
        else:
            return NotImplemented

    def __rfloordiv__(self, other):
        if(isinstance(other, Constant)):
            return Constant(other.value // self.value)
        elif isinstance(other, Number):
            return Constant(other // self.value)
        else:
            return NotImplemented

    def __mod__(self, other):
        if(isinstance(other, Constant)):
            return Constant(self.value % other.value)
        elif isinstance(other, Number):
            return Constant(self.value % other)
        else:
            return NotImplemented

    def __rmod__(self, other):
        if(isinstance(other, Constant)):
            return Constant(other.value % self.value)
        elif isinstance(other, Number):
            return Constant(other % self.value)
        else:
            return NotImplemented

    def __pow__(self, other):
        if(isinstance(other, Constant)):
            return Constant(self.value ** other.value)
        elif isinstance(other, Number):
            return Constant(self.value ** other)
        else:
            return NotImplemented

    def __rpow__(self, other):
        if(isinstance(other, Constant)):
            return Constant(other.value ** self.value)
        elif isinstance(other, Number):
            return Constant(other ** self.value)
        else:
            return NotImplemented

    def __lshift__(self, other):
        if(isinstance(other, Constant)):
            return Constant(self.value << other.value)
        elif isinstance(other, Number):
            return Constant(self.value << other)
        else:
            return NotImplemented

    def __rlshift__(self, other):
        if(isinstance(other, Constant)):
            return Constant(other.value << self.value)
        elif isinstance(other, Number):
            return Constant(other << self.value)
        else:
            return NotImplemented

    def __rshift__(self, other):
        if(isinstance(other, Constant)):
            return Constant(self.value >> other.value)
        elif isinstance(other, Number):
            return Constant(self.value >> other)
        else:
            return NotImplemented

    def __rrshift__(self, other):
        if(isinstance(other, Constant)):
            return Constant(other.value >> self.value)
        elif isinstance(other, Number):
            return Constant(other >> self.value)
        else:
            return NotImplemented

    def __and__(self, other):
        if(isinstance(other, Constant)):
            return Constant(self.value & other.value)
        elif isinstance(other, Number):
            return Constant(self.value & other)
        else:
            return NotImplemented

    def __rand__(self, other):
        if(isinstance(other, Constant)):
            return Constant(other.value & self.value)
        elif isinstance(other, Number):
            return Constant(other & self.value)
        else:
            return NotImplemented

    def __xor__(self, other):
        if(isinstance(other, Constant)):
            return Constant(self.value ^ other.value)
        elif isinstance(other, Number):
            return Constant(self.value ^ other)
        else:
            return NotImplemented

    def __rxor__(self, other):
        if(isinstance(other, Constant)):
            return Constant(other.value ^ self.value)
        elif isinstance(other, Number):
            return Constant(other ^ self.value)
        else:
            return NotImplemented

    def __or__(self, other):
        if(isinstance(other, Constant)):
            return Constant(self.value | other.value)
        elif isinstance(other, Number):
            return Constant(self.value | other)
        else:
            return NotImplemented

    def __ror__(self, other):
        if(isinstance(other, Constant)):
            return Constant(other.value | self.value)
        elif isinstance(other, Number):
            return Constant(other | self.value)
        else:
            return NotImplemented

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __complex__(self):
        return complex(self.value)


class Variable:
    def __init__(self, name):
        self.name = name

    def evaluate(self, **kwargs):
        for key, value in kwargs.items():
            if(key == self.name):
                return value

    def __add__(self, other):
        plus = Operator('+', lambda lhs, rhs: lhs + rhs)

        if (isinstance(other, Variable) or
                isinstance(other, Number) or
                isinstance(other, Constant)):
            return Expression((self, plus, other))
        else:
            return NotImplemented

    def __radd__(self, other):
        plus = Operator('+', lambda lhs, rhs: lhs + rhs)

        if (isinstance(other, Variable) or
                isinstance(other, Number) or
                isinstance(other, Constant)):
            return Expression((other, plus, self))
        else:
            return NotImplemented

    def __sub__(self, other):
        minus = Operator('-', lambda lhs, rhs: lhs - rhs)

        if (isinstance(other, Variable) or
                isinstance(other, Number) or
                isinstance(other, Constant)):
            return Expression((self, minus, other))
        else:
            return NotImplemented

    def __rsub__(self, other):
        minus = Operator('-', lambda lhs, rhs: lhs - rhs)
        if (isinstance(other, Variable) or
                isinstance(other, Number) or
                isinstance(other, Constant)):
            return Expression((other, minus, self))
        else:
            return NotImplemented

    def __mul__(self, other):
        multiply = Operator('*', lambda lhs, rhs: lhs * rhs)
        if (isinstance(other, Variable) or
                isinstance(other, Number) or
                isinstance(other, Constant)):
            return Expression((self, multiply, other))
        else:
            return NotImplemented

    def __rmul__(self, other):
        multiply = Operator('*', lambda lhs, rhs: lhs * rhs)
        if (isinstance(other, Variable) or
                isinstance(other, Number) or
                isinstance(other, Constant)):
            return Expression((other, multiply, self))
        else:
            return NotImplemented

    def __truediv__(self, other):
        truediv = Operator('/', lambda lhs, rhs: lhs / rhs)
        if (isinstance(other, Variable) or
                isinstance(other, Number) or
                isinstance(other, Constant)):
            return Expression((self, truediv, other))
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        truediv = Operator('/', lambda lhs, rhs: lhs / rhs)
        if (isinstance(other, Variable) or
                isinstance(other, Number) or
                isinstance(other, Constant)):
            return Expression((other, truediv, self))
        else:
            return NotImplemented

    def __floordiv__(self, other):
        floordiv = Operator('//', lambda lhs, rhs: lhs // rhs)
        if (isinstance(other, Variable) or
                isinstance(other, Number) or
                isinstance(other, Constant)):
            return Expression((self, floordiv, other))
        else:
            return NotImplemented

    def __rfloordiv__(self, other):
        floordiv = Operator('//', lambda lhs, rhs: lhs // rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((other, floordiv, self))
        else:
            return NotImplemented

    def __mod__(self, other):
        mod = Operator('%', lambda lhs, rhs: lhs % rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((self, mod, other))
        else:
            return NotImplemented

    def __rmod__(self, other):
        mod = Operator('%', lambda lhs, rhs: lhs % rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((other, mod, self))
        else:
            return NotImplemented

    def __pow__(self, other):
        pow_operation = Operator('**', lambda lhs, rhs: lhs ** rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((self, pow_operation, other))
        else:
            return NotImplemented

    def __rpow__(self, other):
        pow_operation = Operator('**', lambda lhs, rhs: lhs ** rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((other, pow_operation, self))
        else:
            return NotImplemented

    def __lshift__(self, other):
        lshift = Operator('<<', lambda lhs, rhs: lhs << rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((self, lshift, other))
        else:
            return NotImplemented

    def __rlshift__(self, other):
        lshift = Operator('<<', lambda lhs, rhs: lhs << rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((other, lshift, self))
        else:
            return NotImplemented

    def __rshift__(self, other):
        rshift = Operator('>>', lambda lhs, rhs: lhs >> rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((self, rshift, other))
        else:
            return NotImplemented

    def __rrshift__(self, other):
        rshift = Operator('>>', lambda lhs, rhs: lhs >> rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((other, rshift, self))
        else:
            return NotImplemented

    def __and__(self, other):
        and_operator = Operator('&', lambda lhs, rhs: lhs & rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((self, and_operator, other))
        else:
            return NotImplemented

    def __rand__(self, other):
        and_operator = Operator('&', lambda lhs, rhs: lhs & rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((other, and_operator, self))
        else:
            return NotImplemented

    def __xor__(self, other):
        xor = Operator('^', lambda lhs, rhs: lhs ^ rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((self, xor, other))
        else:
            return NotImplemented

    def __rxor__(self, other):
        xor = Operator('^', lambda lhs, rhs: lhs ^ rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((other, xor, self))
        else:
            return NotImplemented

    def __or__(self, other):
        or_operator = Operator('|', lambda lhs, rhs: lhs | rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((self, or_operator, other))
        else:
            return NotImplemented

    def __ror__(self, other):
        or_operator = Operator('|', lambda lhs, rhs: lhs | rhs)
        if isinstance(other, Variable) or isinstance(other, Number):
            return Expression((other, or_operator, self))
        else:
            return NotImplemented

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()


class Operator:
    def __init__(self, symbol, function):
        self.symbol = symbol
        self. function = function

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.__str__()


class Expression:
    def __init__(self, expression):
        self.expression = expression

        self.variable_names = []
        self.init_variables(self.expression)

    def init_variables(self, argument):
        first_argument = argument[0]
        second_argument = argument[2]

        if isinstance(first_argument, tuple):
            self.init_variables(first_argument)
        elif isinstance(first_argument, Variable):
            self.variable_names.append(first_argument.name)

        if isinstance(second_argument, tuple):
            self.init_variables(second_argument)
        elif isinstance(second_argument, Variable):
            self.variable_names.append(second_argument.name)

        return self.variable_names

    def __add__(self, other):
        plus = Operator('+', lambda lhs, rhs: lhs + rhs)
        if isinstance(other, Expression):
            return Expression((self.expression, plus, other.expression))
        else:
            return Expression((self.expression, plus, other))

    def __radd__(self, other):
        plus = Operator('+', lambda lhs, rhs: lhs + rhs)
        if isinstance(other, Expression):
            return Expression((other.expression, plus, self.expression))
        else:
            return Expression((other, plus, self.expression))

    def __sub__(self, other):
        minus = Operator('-', lambda lhs, rhs: lhs - rhs)
        if isinstance(other, Expression):
            return Expression((self.expression, minus, other.expression))
        else:
            return Expression((self.expression, minus, other))

    def __rsub__(self, other):
        minus = Operator('-', lambda lhs, rhs: lhs - rhs)
        if isinstance(other, Expression):
            return Expression((other.expression, minus, self.expression))
        else:
            return Expression((other, minus, self.expression))

    def __mul__(self, other):
        times = Operator('*', lambda lhs, rhs: lhs * rhs)
        if isinstance(other, Expression):
            return Expression((self.expression, times, other.expression))
        else:
            return Expression((self.expression, times, other))

    def __rmul__(self, other):
        times = Operator('*', lambda lhs, rhs: lhs * rhs)
        if isinstance(other, Expression):
            return Expression((other.expression, times, self.expression))
        else:
            return Expression((other, times, self.expression))

    def __truediv__(self, other):
        truediv = Operator('/', lambda lhs, rhs: lhs / rhs)
        if isinstance(other, Expression):
            return Expression((self.expression, truediv, other.expression))
        else:
            return Expression((self.expression, truediv, other))

    def __rtruediv__(self, other):
        truediv = Operator('/', lambda lhs, rhs: lhs / rhs)
        if isinstance(other, Expression):
            return Expression((other.expression, truediv, self.expression))
        else:
            return Expression((other, truediv, self.expression))

    def __floordiv__(self, other):
        floordiv = Operator('//', lambda lhs, rhs: lhs // rhs)
        if isinstance(other, Expression):
            return Expression((self.expression, floordiv, other.expression))
        else:
            return Expression((self.expression, floordiv, other))

    def __rfloordiv__(self, other):
        floordiv = Operator('//', lambda lhs, rhs: lhs // rhs)
        if isinstance(other, Expression):
            return Expression((other.expression, floordiv, self.expression))
        else:
            return Expression((other, floordiv, self.expression))

    def __mod__(self, other):
        mod = Operator('%', lambda lhs, rhs: lhs % rhs)
        if isinstance(other, Expression):
            return Expression((self.expression, mod, other.expression))
        else:
            return Expression((self.expression, mod, other))

    def __rmod__(self, other):
        mod = Operator('%', lambda lhs, rhs: lhs % rhs)
        if isinstance(other, Expression):
            return Expression((other.expression, mod, self.expression))
        else:
            return Expression((other, mod, self.expression))

    def __pow__(self, other):
        pow_operation = Operator('**', lambda lhs, rhs: lhs ** rhs)
        if isinstance(other, Expression):
            return Expression((self.expression,
                              pow_operation, other.expression))
        else:
            return Expression((self.expression, pow_operation, other))

    def __rpow__(self, other):
        pow_operation = Operator('**', lambda lhs, rhs: lhs ** rhs)
        if isinstance(other, Expression):
            return Expression((other.expression,
                              pow_operation, self.expression))
        else:
            return Expression((other, pow_operation, self.expression))

    def __lshift__(self, other):
        lshift = Operator('<<', lambda lhs, rhs: lhs << rhs)
        if isinstance(other, Expression):
            return Expression((self.expression, lshift, other.expression))
        else:
            return Expression((self.expression, lshift, other))

    def __rlshift__(self, other):
        lshift = Operator('<<', lambda lhs, rhs: lhs << rhs)
        if isinstance(other, Expression):
            return Expression((other.expression, lshift, self.expression))
        else:
            return Expression((other, lshift, self.expression))

    def __rshift__(self, other):
        rshift = Operator('>>', lambda lhs, rhs: lhs >> rhs)
        if isinstance(other, Expression):
            return Expression((self.expression, rshift, other.expression))
        else:
            return Expression((self.expression, rshift, other))

    def __rrshift__(self, other):
        rshift = Operator('>>', lambda lhs, rhs: lhs >> rhs)
        if isinstance(other, Expression):
            return Expression((other.expression, rshift, self.expression))
        else:
            return Expression((other, rshift, self.expression))

    def __and__(self, other):
        and_operator = Operator('&', lambda lhs, rhs: lhs & rhs)
        if isinstance(other, Expression):
            return Expression((self.expression, and_operator,
                              other.expression))
        else:
            return Expression((self.expression, and_operator, other))

    def __rand__(self, other):
        and_operator = Operator('&', lambda lhs, rhs: lhs & rhs)
        if isinstance(other, Expression):
            return Expression((other.expression, and_operator,
                              self.expression))
        else:
            return Expression((other, and_operator, self.expression))

    def __xor__(self, other):
        xor = Operator('^', lambda lhs, rhs: lhs ^ rhs)
        if isinstance(other, Expression):
            return Expression((self.expression, xor, other.expression))
        else:
            return Expression((self.expression, xor, other))

    def __rxor__(self, other):
        xor = Operator('^', lambda lhs, rhs: lhs ^ rhs)
        if isinstance(other, Expression):
            return Expression((other.expression, xor, self.expression))
        else:
            return Expression((other, xor, self.expression))

    def __or__(self, other):
        or_operator = Operator('|', lambda lhs, rhs: lhs | rhs)
        if isinstance(other, Expression):
            return Expression((self.expression, or_operator, other.expression))
        else:
            return Expression((self.expression, or_operator, other))

    def __ror__(self, other):
        or_operator = Operator('|', lambda lhs, rhs: lhs | rhs)
        if isinstance(other, Expression):
            return Expression((other.expression, or_operator, self.expression))
        else:
            return Expression((other, or_operator, self.expression))

    def evaluate_help(self, argument, variables_mappings):
        if isinstance(argument, tuple):
            operator = argument[1]
            first_argument = argument[0]
            second_argument = argument[2]

            result = operator.function(
                self.evaluate_help(first_argument, variables_mappings),
                self.evaluate_help(second_argument, variables_mappings))
            return result
        elif isinstance(argument, Variable):
            return variables_mappings[argument.name]
        elif isinstance(argument, Constant):
            return argument.value
        else:
            return argument

    def evaluate(self, **kwargs):
        operator = self.expression[1]
        first_argument = self.expression[0]
        second_argument = self.expression[2]

        result = operator.function(
            self.evaluate_help(first_argument, kwargs),
            self.evaluate_help(second_argument, kwargs))
        return result

    def __str__(self):
        return self.str_help(self.expression)

    def str_help(self, argument):
        if(isinstance(argument, tuple)):
            operator = argument[1]
            first_argument = argument[0]
            second_argument = argument[2]

            to_str = ("(" +
                      self.str_help(first_argument) + " " +
                      str(operator) + " " +
                      self.str_help(second_argument) +
                      ")")
            return to_str
        else:
            return str(argument)

    def __repr__(self):
        return self.__str__()


def create_operator(symbol, function):
    return Operator(symbol, function)


def create_constant(value):
    return Constant(value)


def create_variable(name):
    return Variable(name)


def create_expression(expression_structure):
    return Expression(expression_structure)
