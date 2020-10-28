from ruobr_api import Ruobr

# Авторизация
u1 = Ruobr("username1", "password1")
u1.getUser()
u2 = Ruobr("username2", "password2")
u2.getUser()

# Получаем прогресс обоих учеников
u1_progress = u1.getProgress()
u2_progress = u2.getProgress()


# Получаем словари вида {предмет: место в топе}
u1_subjects = {}
u2_subjects = {}
for i in u1_progress["subjects"]:
    u1_subjects[i["subject"]] = i["place"]
for i in u2_progress["subjects"]:
    u2_subjects[i["subject"]] = i["place"]

# Сравниваем места в топе и добавляем в списки
u1_better = []
u2_better = []
for subject, place in u1_subjects.items():
    if subject in u2_subjects.keys():
        if u2_subjects[subject] > place:
            u1_better.append(subject)
        elif u2_subjects[subject] < place:
            u2_better.append(subject)

print(u1.user["first_name"], "лучше в следующих предметах:", ", ".join(u1_better))
print(u2.user["first_name"], "лучше в следующих предметах:", ", ".join(u2_better))
