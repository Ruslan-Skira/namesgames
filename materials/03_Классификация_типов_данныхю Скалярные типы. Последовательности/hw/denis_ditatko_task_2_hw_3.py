# Вычисляем часы в солы
days, hours = map(int, input("Введите дни и часы: "). split(","))
sol = (days + hours / 24) * 1.02595675
sol_1 = round(sol, 2)
print('Количество солов: ', sol_1)