import sys

sys.modules['_decimal'] = None
import decimal
from decimal import *
from decimal import Decimal

getcontext().Emin = -10 * 10000
getcontext().Emax = 10 * 10000
getcontext().traps[Overflow] = 0
getcontext().traps[Underflow] = 0
getcontext().traps[DivisionByZero] = 0
getcontext().traps[InvalidOperation] = 0
getcontext().prec = 100

POSSIBLE_OPERATIONS = ["*", "-", "+", "/", "%", "//", "**"]


class Node:
    """
    This class contains attributes of nodes to store data
    """

    def __init__(self):
        self.value = None


class NumNode(Node):
    """
    This class contains attributes of nodes used for storing numbers.
    """

    def __init__(self, value: Decimal or int or float):
        super().__init__()
        self.value: Decimal or int or float = value

    def evaluate(self, operation_node, num_node):
        # type: (OperationNode, NumNode) -> Decimal
        return Decimal(self.value) * Decimal(num_node.value) if operation_node.value == "*" else Decimal(self.value) - Decimal(num_node.value) \
            if operation_node.value == "-" else Decimal(self.value) + Decimal(num_node.value) if operation_node.value == "+" else \
            Decimal(self.value) / Decimal(num_node.value) if operation_node.value == "/" else Decimal(self.value) % Decimal(num_node.value) if \
                operation_node.value == "%" else Decimal(self.value) // Decimal(num_node.value) if operation_node.value == "//" else \
                Decimal(self.value) ** Decimal(num_node.value)


class OperationNode(Node):
    """
    This class contains attributes of nodes used for storing operations.
    """

    def __init__(self, value: str):
        super().__init__()
        assert value in POSSIBLE_OPERATIONS, "Invalid argument 'value'!"
        self.value: str or None = value


def is_operation(a_str: str) -> bool:
    return a_str in POSSIBLE_OPERATIONS


def is_number(a_str: str) -> bool:
    return not Decimal(a_str).is_nan()


def evaluate_expression(expr: str) -> Decimal:
    nodes: list = []  # initial value
    whitespace: str = " "
    values: list = expr.split(whitespace)
    for value in values:
        if is_operation(value):
            nodes.append(OperationNode(value))
        elif is_number(value):
            nodes.append(NumNode(value))

    while len(nodes) > 1:
        first_num: Decimal = Decimal(nodes[0].evaluate(nodes[1], nodes[2]))
        temp_list: list = [NumNode(first_num)]  # initial value
        for i in range(3, len(nodes)):
            temp_list.append(nodes[i])

        nodes = temp_list

    return Decimal(nodes[0].value)


def main():
    """
    This function is used to run the program.
    :return:
    """
    print("Enter 1 to type an expression.")
    print("Enter 2 to quit.")
    option: int = int(input("Please enter a number: "))
    while option < 1 or option > 2:
        option: int = int(input("Sorry, invalid input! Please enter a number: "))

    while option != 2:
        if option == 1:
            allowed_chars: list = [" ", ".", "e", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            for char in POSSIBLE_OPERATIONS:
                allowed_chars.append(char)

            expression: str = input("Please enter an expression: ")
            for char in expression:
                if char not in allowed_chars:
                    expression: str = input("Sorry, invalid expression! Please enter another expression: ")

            result: Decimal = evaluate_expression(expression)
            print(str(expression) + " = " + str(result))

        option: int = int(input("Please enter a number: "))
        while option < 1 or option > 2:
            option: int = int(input("Sorry, invalid input! Please enter a number: "))

    sys.exit()


main()
