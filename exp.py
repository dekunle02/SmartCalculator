from app import SmartCalculator

#
# sc = SmartCalculator()
#
# sc.run('a = 3')
# from collections import deque
#
#
# def has_priority(new, old):
#     multi = ("/", "*")
#     ari = ("+", "-")
#     if old == '(':
#         return True
#     return new in multi and old in ari
#
#
# def convert_to_postfix(expression):
#     my_deque = deque()
#     my_list = list()
#     operands = expression.split(' ')
#     for i in range(len(operands)):
#         element = operands[i]
#         if element.isdigit():
#             my_list.append(element)
#         elif element.startswith('('):
#             my_deque.append('(')
#             my_list.append(element[-1])
#         elif element.endswith(')'):
#             my_list.append(element[0])
#             my_list.append(my_deque[-1])
#             my_deque.pop()
#             my_deque.pop()
#         elif element in SmartCalculator.operators:
#             if len(my_deque) == 0:
#                 my_deque.append(element)
#             else:
#                 if has_priority(new=element, old=my_deque[-1]):
#                     my_deque.append(element)
#                 else:
#                     my_deque.reverse()
#                     my_list.extend(my_deque)
#                     my_deque.clear()
#                     my_deque.append(element)
#         if i == len(operands) - 1:
#             if len(my_deque) != 0:
#                 my_deque.reverse()
#                 my_list.extend(my_deque)
#     return " ".join(my_list)
#
# def postfix_to_answer(expression):
#     operands = expression.split()
#     my_deque = deque()
#     current_answer = 0
#     for element in operands:
#         if element.isdigit:
#             my_deque.append(element)
#         else:
#             first = my_deque[-1]
#             operation = element
#             my_deque.pop()
#             second = my_deque[-1]
#             current_answer = SmartCalculator.simple_calculate(f'{first} {operation} {second}')
#             my_deque.append(current_answer)
#     return current_answer
# convert_to_postfix('3 + 2 * 4')
# convert_to_postfix('2 * (3 + 4) + 1')
# convert_to_postfix('10 + 2 * 8 - 3')

print(len(list('sam deyemi colonel'.split())))
