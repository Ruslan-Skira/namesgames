# Существуют 3 варианта форматирования строк на python.


# 1) вариант с использованием оператора '%'.
# Метод является устаревышим. Не стоит уделять ему много вашего внимания.

result1_0 = 'Hello, %s!' % 'World'
# на место знака %s (%+спецификатор) в левом операнде подтсавляется правый операнд.
result1_1 = '%d %s, %d %s' % (6, 'bananas', 10, 'lemons')
# Примеры спецификторов:
# d - десятичное число
# s - строка

# 2) с помощью метода .format(). Является наиболее распространенным.
# Удобен но не так как f-строки

# Общий случай
name: str = 'Joel'
age: int = 23
result1 = 'My name is {}. I am {} years old'.format(name, age)

# Можно указывать индексы (т.е порядковый номер) аргумента который следует подставить.
name: str = 'Yehor'
age: int = 27
result2_0 = 'I am {0} years old. My name is {1}. Today is the {1}th'.format(name, age)

# Можно использовать имя аргумента который нужно поставить
current_day_of_week = 'Sunday'
result2_1 = 'Today is {today}'.format(today=current_day_of_week)

# Для Python version >= 3.6 доступен более простой вариант.
# 3)
name: str = 'Joel'
age: int = 23
result3_0 = f'My name is {name}. I am {age} years old'

# В python 3.8 доступна фича для 'дебага' с помощью f-строк, которая сокращает код.
# вместо:
result3_1 = f'name={name}; age={age}'
# можно писать так:
result3_2 = f'{name=}; {age=}'

# сырые строки.
print('/Users/ruslanskira/Downloads\teleteit')
print(r'/Users/ruslanskira/Downloads\teleteit')
