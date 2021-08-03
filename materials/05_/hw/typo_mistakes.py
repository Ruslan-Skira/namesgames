# inline строчные комменты ошибка в синтаксисе
# https://www.python.org/dev/peps/pep-0008/#inline-comments

# task 3
# проверь входную строку 'Черт черт черт черт начертил чЕртов чертеж вот черт'
#
# результат:  '#### #### #### #### начертил чeртов чертеж вот ####'

# Ellipsis
a = []
b = a; b.append(a); id(b) ; id(a); id(b[0]); id(a[0])
# It means that you created an infinite list nested inside itself, which can not be printed