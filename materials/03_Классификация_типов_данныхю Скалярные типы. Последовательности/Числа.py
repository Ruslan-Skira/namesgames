# int
x_10: int = 15  # десятичное число => 15
y_2: int = 0b1111  # двоичное число => 15
z_8: int = 0o17  # восьмеричное число => 15
w_16: int = 0xF  # шестнадцатиричное число => 15

# float
x: float = 5.5  # Стандартная форма записи => 5.0
y: float = 5.  # Без дробной части => 5.0 => 0.0003
z: float = 3e-4  # Экспоненциальная форма => 5.0

# Операции
sum_x_y: float = 0.4 + 0.2  # => 0.6000000000000001 ????
some_dif: float = 6 - 3.4
some_sum1: float = 6 + 3.0
some_div1: float = 10 / 3  # => 3.3333333333333335
some_div2: float = 9 / 3  # => 3.0
some_sum2: int = 43 + 34
some_mult: int = 43 * 2

# Несколько полезных функций при работе с числами
absolute_n = abs(-5)  # Абсолютное значение / Значение по модулю
rounded_n1: int = round(4.23121)  # round => 4
rounded_n2: float = round(4.23121, 2)  # round => 4.23
fl_n: float = float(45)  # => 45.0
int_from_float: int = int(45.90757820)  # => 45



