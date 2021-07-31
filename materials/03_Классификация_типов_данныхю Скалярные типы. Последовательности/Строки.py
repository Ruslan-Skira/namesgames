# Строки - последовательности символов unicode (utf-8)

single_quote_str = 'some single quote str'
double_quote_str = "some single quote str"
some_long_long_text = """some long, very long text. some long, very long text. 
                some long, very long text. some long, very long text. """

string_with_tab_and_newline_and_slash_and_double_quote = "tab\t and new \n line and slash \\ and double qoute \" "


ord('a')  # => 97
# Кроме того, есть функция имеющая противоположенное действие -
chr(65)  # => 'A'

# methods
'some str'.upper()  # => 'SOME STR'
'SOME str'.lower()  # => 'some str'
'some str'.capitalize()  # => 'Some str'
'some str'.title()  # => 'Some Str'
'some str'.count('s')  # => 2
'some str'.replace('s', 'm', 1)  # заменяет нахождения первого элемента на второй, n раз (3 аргумент - тут 1)
#  => 'mome str'
