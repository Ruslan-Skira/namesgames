# set - Это неупорядоченная коллекция уникальных элементов.

# На русском правильно говорить - множество.

# Два способа создать set
some_set1 = {"a", "b", "c", 2}
some_set2 = set()

some_list1 = [1, 3, 4, 6, 8]
some_set3 = set(some_list1)

# Методы set`ов

some_set3.add('new elem')  # Добавляем элемент в множество
some_set3.remove('new elem 1')  # Удаляет элемент. Если его и не было, кидает ошибку
some_set3.discard('new elem')  # Удаляет элемент. Если его не было, ошибка не возникает
some_set3.pop()  # Удаляет произвольный элемент и возвращает его.
some_set3.clear()  # Удаляет все элементы множества
some_set3.update(some_set1)  # Добавляет все элементы множества-аргумента к множеству для которго вызывается метод

# Математические операции V1
some_set3.union(some_set1, some_set2)  # объеденение множеств. Возвращает новый объект.
some_set3.intersection(some_set1, some_set2)  # пересечение множеств. Возвращает новый объект.
some_set3.difference(some_set1, some_set2)  # разность множеств. Возвращает новый объект.

some_set3.isdisjoint(some_set2)  # возвращет True, если общих элементов у множеств нет.
some_set3.issubset(some_set2)  # возвращет True, если все элементы множества для которого вызывается метод,
# содержаться в множестве-аргументе
some_set3.issuperset(some_set2)  # возвращет True, если все элементы множества-аргумента
# содержаться в множестве для котороо вызывается метод

# Математические операции V2
# Аналог .union()
some_new_set = some_set1 | some_set2 | some_set3

# Аналог .intersection()
some_new_set2 = some_set1 & some_set2 & some_set3

# Аналог .difference()
some_new_set3 = some_set1 - some_set2 - some_set3

# Аналог .issubset()
some_bool_value11: bool = some_set3 <= some_set2
some_bool_value12: bool = some_set3 < some_set2

# Аналог .issuperset()
some_bool_value21: bool = some_set3 >= some_set2
some_bool_value22: bool = some_set3 > some_set2

# Аналог .update()
some_new_set3 |= some_set3  # Добавляет к some_new_set3 элементы some_set3


