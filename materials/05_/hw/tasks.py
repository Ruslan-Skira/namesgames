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

#variant3
{k:line.count(k) for k in line}

