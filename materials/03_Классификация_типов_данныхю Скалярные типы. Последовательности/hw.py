# print('(etnfづzxfk｡12dt◕`1ad‿6hns‿1zQY◕Cd$y｡FtSq)Ze6?づ#2)$'[::5])

# нарисуй линиями условие.
## variant1
# earth_days_hours = input('earth days, earth hours').split(",")
# earth_hours = (int(earth_days_hours[0]) * 24 + int(earth_days_hours[1]))
# mars_days = earth_hours/24 / 1.02595675
# print(round(mars_hours, 4))
#
# # variant2
# days, hours = map(int, input('earth days, earth hours').split(","))
# mars_days = (days + hours/24) / 1.02595675
# print(round(mars_days, 4))

# 1 = 1.02595675


# task 3
text = "чертовщина на чертеже черт чертежник написал черт"
# text = input('fil up the text please').lower()
text_clear = text.replace(" черт ", ' ### ')


if text_clear[-5:] == ' черт':
    text_clear = text_clear[:-5] + ' ###'
elif text_clear[index_chert + 4] == 'черт ':
    text_clear = ' ###' + text_clear[4:]

print(text_clear)