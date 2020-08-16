class SmartCalculator:
    operators = ('-', '+', '/', '*')
    commands = ('/help', '/exit', '/bye')
    error_msg = {1: "Invalid expression", 2: "Unknown command",
                 3: "Unknown variable", 4: 'Invalid identifier',
                 5: 'Invalid assignment'}
    help_msg = 'I am a smart calculator, give me math problems'
    exit_msg = 'Bye!'

    def __init__(self):
        self.state = 'ON'
        self.variables = {}

    def fetch_variable(self, given_string):
        if given_string.isdigit():
            return given_string
        elif given_string in self.variables.keys():
            return self.variables[given_string]
        elif not given_string.isalpha():
            print(SmartCalculator.error_msg[4])
        else:
            print(SmartCalculator.error_msg[3])

    def save_new_variable(self, string):
        string = self.remove_extra_spaces(string)
        # checking to see if assignment has more than 1 equal sign
        if string.count('=') > 1:
            print(SmartCalculator.error_msg[5])
            return
        key, value = string.split('=')
        key = key.strip()
        value = value.strip()

        # checking to see that key contains no numbers
        if not key.isalpha():
            print(SmartCalculator.error_msg[4])
            return
        # check if value is a number
        if value.isdigit():
            self.variables[key] = value
        else:
            # check if value is a previously saved variable
            value = self.fetch_variable(value)
            if value:
                self.variables[key] = self.fetch_variable(value)

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
    def remove_extra_spaces(string):
        string_list = string.split()
        while ' ' in string_list:
            string_list.remove(' ')
        return ' '.join(string_list)

    def simple_calculate(self, string):
        arr = string.split(' ')
        if len(arr) == 1:
            return arr[0]
        elif len(arr) == 2:
            return arr[1]
        elif len(arr) > 2:
            num1 = int(arr[0])
            op = arr[1]
            num2 = int(arr[2])
            if len(arr) == 3:
                if op == '+':
                    return str(num1 + num2)
                elif op == '-':
                    return str(num1 - num2)
                elif op == '/':
                    return str(num1 / num2)
                elif op == '*':
                    return str(num1 * num2)
            else:
                sub = ' '.join(arr[:3])
                left = ' '.join(arr[3:])
                return self.simple_calculate(self.simple_calculate(sub) + ' ' + left)

    def smart_calculate(self, problem_string):
        string_arr = self.remove_extra_spaces(problem_string).split(' ')
        format_is_correct = True
        for i in range(len(string_arr)):
            if i % 2 == 0:
                try:
                    int(string_arr[i])
                except TypeError:
                    print(SmartCalculator.error_msg[1])
                    format_is_correct = False
                    break
            else:
                if not self.determine_operator(string_arr[i]) in SmartCalculator.operators:
                    print(SmartCalculator.error_msg[1])
                    format_is_correct = False
                    break
                else:
                    operator = self.determine_operator(string_arr[i])
                    string_arr[i] = operator
        if format_is_correct:
            problem = ' '.join(string_arr)
            answer = int(self.simple_calculate(problem))
            return answer

    def process_variables(self, user_input):
        # to assignment branch of calculator
        if '=' in user_input:
            self.save_new_variable(user_input)
        else:
            strings = self.remove_extra_spaces(user_input).split(" ")
            for i in range(len(strings)):
                # to exclude the operators
                if i % 2 == 0:
                    element = strings[i]
                    if self.fetch_variable(element):
                        strings[i] = self.fetch_variable(element)
                    else:
                        return
            return ' '.join(strings)

    def run(self, user_input):
        if not user_input:
            return
        if user_input[0] == '/' and user_input not in self.commands:
            print(SmartCalculator.error_msg[2])
            return
        if user_input == '/help':
            print(SmartCalculator.help_msg)
        elif user_input == '/exit':
            print(SmartCalculator.exit_msg)
            self.state = 'OFF'
        else:
            problem = self.process_variables(user_input)
            if problem:
                answer = self.smart_calculate(problem)
                print(answer)


if __name__ == '__main__':
    cal = SmartCalculator()
    while cal.state != 'OFF':
        cal.run(input())


# from collections import deque
#
#
# def check_brackets(string):
#     my_stack = deque()
#     for char in string:
#         if char == "(":
#             my_stack.append("(")
#         elif char == ")":
#             if len(my_stack) > 0:
#                 my_stack.pop()
#             else:
#                 return 'ERROR'
#     if len(my_stack) == 0:
#         return "OK"
#     else:
#         return "ERROR"


# collect the string
# adjust spacing
# check for proper bracketing
# check for variables and replace where available
# convert to postfix
# solve for answer using stack and simple calculate