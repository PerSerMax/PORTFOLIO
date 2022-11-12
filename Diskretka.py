import itertools
import re


print(
    '	Лень делать таблицы по дискретке?	\n'
    '	Ты пришел по адресу!			\n'
    '	! - инверсия					\n'
    '	+ - логическое сложение			\n'
    '	* - логическое умножение		\n'
    '	-> - импликация					\n'
    '	xor - симметричная разность		\n'
    )


input_string = input()
input_string = input_string.replace(' ', '')
input_string = input_string.replace('+', ' or ')
input_string = input_string.replace('*', ' and ')
input_string = input_string.replace('&', ' and ')
input_string = input_string.replace('!', 'not ')
input_string = input_string.replace('=', ' == ')
input_string = input_string.replace('->', ' <= ')
input_string = input_string.replace('xor', ' != ')


masx = re.findall(r'\w\d+', input_string)
masx = set(masx)
masx = sorted(list(masx))

list_of_combinations = list(itertools.product((0, 1), repeat=len(masx)))

for one_combination in list_of_combinations:
    expression = input_string
    for i in range(len(masx)):
        expression = expression.replace(masx[i], str(bool(one_combination[i])))
        combination_output = str(one_combination).replace('(', '')
        combination_output = combination_output.replace(',', '')
        combination_output = combination_output.replace(')', '')
    exec(
        'print("' + combination_output + ' |", int(' + expression + '))'
    )
