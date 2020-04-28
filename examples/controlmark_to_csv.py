from ruobr_api import Ruobr
import csv

r = Ruobr("username", "password")  # Авторизация
controlmark = r.getControlmark()  # Получение итоговых оценок

titles = ['Дисциплины']
subjects = []
for period in controlmark:
    titles.append(period['rom'])  # Создание шапки таблицы с номерами четвертей
    subjects.extend(list(period['marks'].keys()))  # Получение всех предметов

# Создание словаря вида {предмет: [], ...}
subjects = {i: [] for i in sorted(list(set(subjects)))}

# Заполнение словаря оценками
for period in controlmark:
    for subject in list(subjects.keys()):
        if subject in period['marks']:
            subjects[subject].append(period['marks'][subject])
        else:
            subjects[subject].append("-")

# Сейчас мы имеем словарь вида {предмет: [оценка1, ...], ...}
# Необходимо представить таблицу в виде [[предмет, оценка1...], ...]
data = [titles]  # Первая строка - шапка
for subject, marks in subjects.items():
    items = [subject]
    for i in marks:
        items.append(i)
    data.append(items)

with open("output.csv", "w") as csv_file:  # Экспорт в csv
    writer = csv.writer(csv_file, delimiter=',')
    for line in data:
        writer.writerow(line)
