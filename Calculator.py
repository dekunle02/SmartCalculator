# collect the string
# adjust spacing first
# check for proper bracketing
# check for variables and replace where available
# convert to postfix
# solve for answer using stack and simple calculate
# while solving, resolve the ++++ ----

from collections import deque


class Calculator:
    operators = ('-', '+', '/', '*', '^')
    commands = ('/help', '/exit', '/bye')
    error_msg = {1: "Invalid expression", 2: "Unknown command",
                 3: "Unknown variable", 4: 'Invalid identifier',
                 5: 'Invalid assignment', 6: 'Invalid expression'}
    help_msg = 'I am a smart calculator, give me math problems'
    exit_msg = 'Bye!'

    # States are ON, OFF, ERROR

    def __init__(self):
        self.state = 'ON'
        self.variables = {}

    def run(self, user_input):
        if not user_input:
            return
        if user_input[0] == '/' and user_input not in self.commands:
            print(self.error_msg[2])
        if user_input == '/help':
            print(Calculator.help_msg)
        elif user_input == '/exit':
            print(Calculator.exit_msg)
            self.state = 'OFF'
        else:
            if not self.brackets_are_correct(user_input):
                print(self.error_msg[6])
            else:
                problem = self.remove_extra_spaces(user_input)
                problem = self.process_exp_for_variables(problem)
                if problem is None:
                    return
                postfix = self.convert_to_postfix(problem)
                if postfix is None:
                    return
                answer = self.postfix_to_answer(postfix)
                print(answer)

    @staticmethod
    def calculate(expression):
        num1, operation, num2 = expression.split(" ")
        num1 = int(num1)
        num2 = int(num2)
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '/':
            return num1 / num2
        elif operation == '*':
            return num1 * num2

    @staticmethod
    def remove_extra_spaces(string):
        string_list = string.split()
        while ' ' in string_list:
            string_list.remove(' ')
        return ' '.join(string_list)

    @staticmethod
    def brackets_are_correct(expression):
        my_stack = deque()
        for char in expression:
            if char == "(":
                my_stack.append("(")
            elif char == ")":
                if len(my_stack) > 0:
                    my_stack.pop()
                else:
                    return False
        if len(my_stack) == 0:
            return True
        else:
            return False

    def fetch_variable(self, given_string):
        if given_string.isdigit():
            return given_string
        elif given_string in self.variables.keys():
            return self.variables[given_string]
        elif not given_string.isalpha():
            print(Calculator.error_msg[4])
        else:
            print(Calculator.error_msg[3])

    def save_new_variable(self, string):
        string = self.remove_extra_spaces(string)
        # checking to see if assignment has more than 1 equal sign
        if string.count('=') > 1:
            print(Calculator.error_msg[5])
            return
        key, value = string.split('=')
        key = key.strip()
        value = value.strip()

        # checking to see that key contains no numbers
        if not key.isalpha():
            print(Calculator.error_msg[4])
            return
        # check if value is a number
        if value.isdigit():
            self.variables[key] = value
        else:
            # check if value is a previously saved variable
            value = self.fetch_variable(value)
            if value:
                self.variables[key] = self.fetch_variable(value)

    def process_exp_for_variables(self, expression):
        # to assignment branch of calculator
        if '=' in expression:
            self.save_new_variable(expression)
            return
        else:
            strings = expression.split(" ")
            for i in range(len(strings)):
                element = strings[i]
                if element.isalpha() and element not in self.variables.keys():
                    print(self.error_msg[3])
                    return
                elif element.isalpha() and element in self.variables.keys():
                    strings[i] = self.variables[i]
            return ' '.join(strings)

    def determine_operator(self, operator):
        if len(operator) == 1:
            return operator
        if len(operator) == 2:
            if operator == '++' or operator == '--':
                return '+'
            elif operator == '+-' or operator == '-+':
                return '-'
            else:
                return operator
        if len(operator) > 2:
            part_1 = operator[:2]
            part_2 = operator[2:]
            return self.determine_operator(self.determine_operator(part_1) + self.determine_operator(part_2))

    @staticmethod
    def has_priority(new, old):
        multi = ("/", "*")
        ari = ("+", "-")
        if old == '(':
            return True
        return new in multi and old in ari

    def convert_to_postfix(self, expression):
        my_deque = deque()
        my_list = list()
        operands = expression.split(' ')
        for i in range(len(operands)):
            element = operands[i]
            if element.isdigit():
                my_list.append(element)
            elif element.startswith('('):
                my_deque.append('(')
                my_list.append(element[-1])
            elif element.endswith(')'):
                my_list.append(element[0])
                my_list.append(my_deque[-1])
                my_deque.pop()
                my_deque.pop()
            else:
                if element.count('*') > 1 or element.count('/') > 1:
                    print(self.error_msg[6])
                    return
                try:
                    int(element)
                except ValueError:
                    element = self.determine_operator(element)
                if len(my_deque) == 0:
                    my_deque.append(element)
                else:
                    if Calculator.has_priority(new=element, old=my_deque[-1]):
                        my_deque.append(element)
                    else:
                        my_deque.reverse()
                        my_list.extend(my_deque)
                        my_deque.clear()
                        my_deque.append(element)
            if i == len(operands) - 1:
                if len(my_deque) != 0:
                    my_deque.reverse()
                    my_list.extend(my_deque)
        return " ".join(my_list)

    @staticmethod
    def postfix_to_answer(expression):
        if expression is None:
            return
        operands = expression.split()
        my_deque = deque()
        current_answer = 0
        for element in operands:
            if element not in Calculator.operators:
                my_deque.append(element)
            else:
                first = my_deque[-1]
                operation = element
                my_deque.pop()
                second = my_deque[-1]
                my_deque.pop()
                current_answer = Calculator.calculate(f'{second} {operation} {first}')
                my_deque.append(current_answer)
        current_answer = my_deque[-1]
        return current_answer


cal = Calculator()
while cal.state != 'OFF':
    cal.run('8 * 3 + 12 * (4 - 2)')
    cal.run('2 - 2 + 3')
    cal.run('4 * (2 + 3')
    cal.run('-10')
    cal.run('a=4')
    cal.run('b=5')
    cal.run('c=6')
    # cal.run('a*2+b*3+c*(2+3)')
    # cal.run('1 +++ 2 * 3 -- 4')
    # cal.run('3 *** 5')
    # cal.run('4+3)')
    # cal.run('/command')
    cal.run('/exit')
