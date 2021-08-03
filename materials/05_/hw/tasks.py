''' Write a Python program to count the number of characters (character frequency) in a string. Go to the editor
Sample String : google.com'
Expected Result : {'g': 2, 'o': 3, 'l': 1, 'e': 1, '.': 1, 'c': 1, 'm': 1} '''

# variant1
dict_my = {}
for n in line:
    keys = dict_my.keys()
    if n in keys:
        dict_my[n] += 1
    else:
        dict_my[n] = 1
# variant2
line = 'google.com'
answer = {}
for v in line:
    answer[v] = line.count(v)

# variant3
{k: line.count(k) for k in line}

"""Задача 2. 10 баллов

тема Срезы и условие if.

написать программку которая будет состоять из первых двух и последних символов предоставленной строки.

Если длинна строки меньше двух символов напечатать строку типа.

'Ваша строка слишком короткая - СТРОКА ' . Через метод форматирования строк  с %."""

"""Задача
1.
10
баллов

Написать
программу, которая
подсчитывает
количество
символов
в
строке

и
формирует
dict
в
котором
key = буква, value = количество
их
в
слове:

Входная
строка: 'Hillel school'

Результат: {'H': 1, 'i': 1, 'l': 3, 'e': 1, ' ': 1, 's': 1, 'c': 1, 'h': 1, 'o': 2}"""

"""Задача 3. 15 баллов
Тема list и его методы. Строки и срезы.
Программа принимает список продуктов и принтит самое длинное слово и его длинну.
Ипользовать ''.format() для вывода строки и аргументов.
Входные данные: ['bread', 'milk', 'kolbasa']
Результат: 'Самое длинное название продукта kolbasa длинна 7 символов'"""


def find_longest_word(words_list):
    word_len = []
    for n in words_list:
        word_len.append((len(n), n))
    word_len.sort()
    return word_len[-1][0], word_len[-1][1]


result = find_longest_word(["PHP", "Exercises", "Backend"])
print("\nLongest word: ", result[1])
print("Length of the longest word: ", result[0])

"""Задача 4. 5 баллов
Пользователь водит свое имя. Возвращается тектс БОЛЬШОм и маленьком регистре. Использовать ''.format().
Для вставки аргументов в текст"""
user_input = input("What's your favourite language? ")
print("My favourite language is ", user_input.upper())
print("My favourite language is ", user_input.lower())

"""
Задача 5. 15 баллов.
Тема приведение типов. Работа со списком. Расчленение строки и ее соединение.
Пользователь вводит через запятую последовательность слов например цвета или продукты. 
Программа возвращает уникальные слова отсортированные по алфавиту. 
Входные данные: red, white, black, red, green, black
Результат: black, green, red, white, red

"""
items = input("Input comma separated sequence of words")
words = [word for word in items.split(",")]
print(",".join(sorted(list(set(words)))))

items = input("Input comma separated sequence of words")
words = [word for word in items.split(",")]
print(",".join(sorted(list(set(words)))))

"""
Задача 6. 5 баллов
Тема Кортеж и работа сним
Удалить элемент из кортежа.
"""

"""
Написать программу которая данный список кортежей переведет в список списков"""


def test(lst_tuples):
    result = [list(el) for el in lst_tuples]
    return result


lst_tuples = [(1, 2), (2, 3), (3, 4)]
print("Original list of tuples:")
print(lst_tuples)
print("Convert the said list of tuples to a list of lists:")
print(test(lst_tuples))
lst_tuples = [(1, 2), (2, 3, 5), (3, 4), (2, 3, 4, 2)]
print("\nOriginal list of tuples:")
print(lst_tuples)
print("Convert the said list of tuples to a list of lists:")
print(test(lst_tuples))

""""функция range
вывести в обратном порядке от 99 до -99 с шагом 3.

есть последовательность от 99 до -99. Ее шаг 3
напечатать все элементы последовательности которые делятся на 3 без остатка. 
напечатать в формате 'это ЧИСЛО делится без остатка на 3' использовать метода f' строки' """

for i in range(99, -99, -3):
    if i % 3:
        print(f'это {i}  делиться без остатка ')

"""
даны два списка элементов если хоть один елемент совпадает отпринтить True 
"""


def common_data(list1, list2):
    result = False
    for x in list1:
        for y in list2:
            if x == y:
                result = True
                return result


print(common_data([1, 2, 3, 4, 5], [5, 6, 7, 8, 9]))
print(common_data([1, 2, 3, 4, 5], [6, 7, 8, 9]))
