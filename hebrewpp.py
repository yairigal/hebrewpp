import re
import sys

IM = 'אם'
HADPES = 'הדפס'
TRUE = 'אמת'
FALSE = 'שקר'

BOOL = f'(?P<bool>{TRUE}|{FALSE})'
PRINT = f'{HADPES} (?P<message>.+)'
INDENT = '\s+'
NEWLINE = '\n'
operators_handlers = {
    '==': lambda op1, op2: op1 == op2,
    "<": lambda op1, op2: float(op1) < float(op2),
    ">": lambda op1, op2: float(op1) > float(op2)
}
OPERATORS = f"(?P<operator>{'|'.join(operators_handlers.keys())})"
BINARY_OPERATOR = f'(?P<operand1>.*) {OPERATORS} (?P<operand2>.*)'

STATEMENT = (f'(?P<statement>'
             f'{BOOL}|'
             f'{BINARY_OPERATOR}'
             f')')
CONDITION = (f'{IM} {STATEMENT}:{NEWLINE}'
             f'{INDENT}(?P<action>.+)')
VARIABLE_DEFINITION = f'(?P<var_name>.*) = (?P<var_value>.*)'
PHRASE = f'(?P<phrase>{PRINT}|{CONDITION}|{VARIABLE_DEFINITION})'

NUMBER = '\d+'

context = {}


def is_number(number_string):
    return re.fullmatch(NUMBER, number_string) is not None


def get_value_of(token):
    if is_number(token):
        return int(token)

    if token in context:
        return context[token]

    raise NameError(f'{token} not found')


def calculate_statement(code):
    match = re.fullmatch(BOOL, code)
    if match:
        return match.group('bool') == TRUE

    match = re.fullmatch(BINARY_OPERATOR, code)
    if match:
        op1 = match.group('operand1')
        op1 = get_value_of(op1)
        op2 = match.group('operand2')
        op2 = get_value_of(op2)
        op = match.group('operator')
        return operators_handlers[op](op1, op2)


def handle_condition(match):
    statement = match.group('statement')
    action = match.group('action')
    if calculate_statement(statement):
        run(action)


def handle_print(match):
    message = match.group('message')
    try:
        message = get_value_of(message)
    except NameError:
        pass

    print(message)


def phrase_generator(code):
    while code != '':
        match = re.match(PHRASE, code)
        if match:
            phrase = match.group('phrase')
            yield phrase
            code = code.replace(phrase, "", 1)
            if code != '' and code[0] == NEWLINE:
                code = code[1:]

        else:
            raise SyntaxError(f"No Phrase found in `{code}`")


def prettify_code(code):
    # Remove empty newlines
    def is_empty(line):
        return re.fullmatch('\s*', line)

    code = NEWLINE.join(line for line in code.split(NEWLINE) if not is_empty(line))

    return code


def handle_variable_definition(match):
    variable_name = match.group('var_name')
    variable_value = match.group('var_value')
    context[variable_name] = variable_value


def run(code):
    code = prettify_code(code)
    for phrase in phrase_generator(code):
        match = re.fullmatch(CONDITION, phrase)
        if match:
            handle_condition(match)

        match = re.fullmatch(PRINT, phrase)
        if match:
            handle_print(match)

        match = re.fullmatch(VARIABLE_DEFINITION, phrase)
        if match:
            handle_variable_definition(match)


if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf8') as f:
        run(f.read())
