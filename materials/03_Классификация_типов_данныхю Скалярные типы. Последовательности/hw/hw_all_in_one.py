# #task1
# text_ = '(etnfづzxfk｡12dt◕`1ad‿6hns‿1zQY◕Cd$y｡FtSq)Ze6?づ#2)$'
# print(text_[::5])

##task2
# earth_days_hours = input('fill up days and hours on earth in format days, hours  ').split()
earth_days_hours: list = '123, 6'.split(',')  # for test
days: int = int(earth_days_hours[0])
hours: int = int(earth_days_hours[1])

# days to hours and sum them
earth_hours: int = days * 24 + hours
earth_days = earth_hours / 24
sol_days = round(earth_days / 1.0259, 3)
print(f'{sol_days=}')

# variant2
days, hours = map(int, input('days, hours on earth please in forman  << days, hours >>').split(','))
# days, hours = 123, 6
print(round((days + hours/24)/1.0259, 3))


##task3
text_test = 'черт черт чертить черт'
text_clear = text_test.lower().replace(' черт ', ' #### ')
if text_clear[-5:] == ' черт':
    text_clear = text_clear[:-5] + ' ####'
if text_clear[:5] == 'черт ':
    text_clear = '#### ' + text_clear[5:]

print(text_clear)


