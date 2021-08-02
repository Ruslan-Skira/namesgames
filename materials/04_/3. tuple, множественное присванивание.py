# tuple - это упорядоченная неизменяемая последовательность элементов.
# На русском правильно говорить - кортеж.

# обычно tuple объявляют так:
some_tuple1 = ('some str', 131, 46.74)

# Но можно это сделать без скобок. Показателем того что это tuple являются ЗАПЯТЫЕ!
some_tuple2 = 'x', 131, 46

z = 1
y = 2

z, y = y, z

# А еще tuple используют для множественного присваивания.
# Пример:
age, name = 23, 'SomeName1'
# Здесь tuple c левой стороны РАСПАКОВЫВАЕТСЯ в tuple с правой.
# При этом, Вы можете как распокавать уже существующий tuple
age1 = 23
name1 = 'SomeName'
age_and_name = age1, name1




new_age2, new_name2 = age_and_name

# При этом если например, вам нужно получить первый элемент кортежа и последний, а другие вам не нужны,
# вы можете сделать так:
some_long_tuple: tuple = ('first elem', 2, 3, 4, 5, 6, 'last elem')
first_elem, *other_elements, last_elem = some_long_tuple
# В данном случае вы получите:
# first_elem: str = 'first elem'
# other_elements: tuple = (2, 3, 4, 5, 6)
# last_elem: str = 'last elem'

# еще пример:
first_elem1, second_elem1, *other_elements1 = some_long_tuple
# В данном случае вы получите:
# first_elem: str = 'first elem'
# second_elem1: int = 2
# last_elem: tuple = (2, 3, 4, 5, 6, 'last elem')

# Этот несложный трюк иногда очень облегчает работу с последовательностями

