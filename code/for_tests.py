x = [('Франция', 20), ('Венесуэла', 1), ('Колумбия', 1), ('Австрия', 1), ('Аргентина', 1), ('Норвегия', 1), ('Португалия', 1), ('Мали', 1), ('Польша', 1), ('Сенегал', 1), ('Камерун', 1)]

res = '\n'.join([(q[0] + ' - ' + str(q[1])) for q in x])
print(res)
