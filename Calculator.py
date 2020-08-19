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
            return
        if user_input == '/help':
            print(Calculator.help_msg)
        elif user_input == '/exit':
            print(Calculator.exit_msg)
            self.state = 'OFF'
        # Process input for calculation
        else:
            # Check if brackets are properly placed
            if not self.brackets_are_correct(user_input):
                print(self.error_msg[6])
            else:
                # Convert user input string into a list
                expression = self.process_input_to_list(user_input)
                # check if = in the expression, so we can save variables
                if '=' in expression:
                    self.save_new_variable(expression)
                    return
                else:
                    expression = self.process_exp_for_variables(expression)
                if expression is None:
                    return
                postfix = self.convert_to_postfix(expression)
                if postfix is None:
                    return
                answer = self.postfix_to_answer(postfix)
                print(answer)

    @staticmethod
    def calculate(expression):
        num1, operation, num2 = expression.split(" ")
        num1 = int(float(num1))
        num2 = int(float(num2))
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '/':
            return num1 / num2
        elif operation == '*':
            return num1 * num2

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

    @staticmethod
    def get_stack_elements(stack):
        answer = ''
        while len(stack) != 0:
            answer += stack[0]
            stack.popleft()
        return answer

    def process_input_to_list(self, expression):
        operators = ('-', '+', '/', '*', '^', '=')
        brackets = ('(', ')')
        my_deque = deque()
        answer_list = []
        for char in [char for char in expression]:
            if char in brackets:
                if len(my_deque) != 0:
                    answer_list.append(self.get_stack_elements(my_deque))
                answer_list.append(char)
            else:
                if len(my_deque) != 0:
                    if (char not in operators and my_deque[-1] in operators) or (
                            char in operators and my_deque[-1] not in operators):
                        answer_list.append(self.get_stack_elements(my_deque))
                if char != ' ':
                    my_deque.append(char)
        if len(my_deque) != 0:
            answer_list.append(self.get_stack_elements(my_deque))
        return answer_list

    def fetch_variable(self, given_string):
        if given_string.isdigit():
            return given_string
        elif given_string in self.variables.keys():
            return self.variables[given_string]
        elif not given_string.isalpha():
            print(Calculator.error_msg[4])
        else:
            print(Calculator.error_msg[3])

    def save_new_variable(self, expression):
        # checking to see if assignment has more than 1 equal sign
        if expression.count('=') > 1:
            print(Calculator.error_msg[5])
            return
        key, value = expression[0], expression[2]
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
        for i in range(len(expression)):
            element = expression[i]
            if element.isalpha() and element not in self.variables.keys():
                print(self.error_msg[3])
                return
            elif element.isalpha() and element in self.variables.keys():
                expression[i] = self.variables[expression[i]]
        return expression

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
        result = []
        stack = deque()
        for element in expression:
            if element.isdigit():
                result.append(element)
            elif element == '(':
                stack.append(element)
            else:
                if element.count('*') > 1 or element.count('/') > 1:
                    print(self.error_msg[6])
                    return
                try:
                    int(element)
                except ValueError:
                    element = self.determine_operator(element)
                if len(stack) == 0 or stack[-1] == '(':
                    stack.append(element)
                elif element == ')':
                    while stack[-1] != '(':
                        result.append(stack[-1])
                        stack.pop()
                    stack.pop()
                else:
                    if self.has_priority(element, stack[-1]):
                        stack.append(element)
                    else:
                        while len(stack) != 0 and (stack[-1] != '(' or self.has_priority(stack[-1], element)):
                            result.append(stack[-1])
                            stack.pop()
                        stack.append(element)
        while len(stack) != 0:
            result.append(stack[-1])
            stack.pop()
        return result

    @staticmethod
    def postfix_to_answer(expression):
        if expression is None:
            return
        if len(expression) == 2:
            return int(expression[1] + expression[0])
        my_deque = deque()
        for element in expression:
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


if __name__ == '__main__':
    cal = Calculator()
    while cal.state != 'OFF':
        cal.run(input())

# cal = Calculator()
# while cal.state != 'OFF':
#     cal.run('8 * 3 + 12 * (4 - 2)')
#     cal.run('2 - 2 + 3')
#     cal.run('4 * (2 + 3')
#     cal.run('-10')
#     cal.run('a=4')
#     cal.run('b=5')
#     cal.run('c=6')
#     cal.run('a * 2 + b * 3 + c * (2 + 3)')
#     cal.run('1 +++ 2 * 3 -- 4')
#     cal.run('3 *** 5')
#     cal.run('4+3)')
#     cal.run('3 + 8 * ((4 + 3) * 2 + 1) - 6 / (2 + 1)')
#     cal.run('/command')
#     cal.run('/exit')
