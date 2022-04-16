import ruobr_api

user = ruobr_api.Ruobr("username", "password")
try:
    user.get_user()  # Авторизация
except ruobr_api.AuthenticationException:
    print("Проверьте логин и/или пароль!")
    quit()

if user.is_empty:
    print("На аккаунте не обнаружено детей")
    quit()

if user.is_applicant:  # Обработка родительского аккаунта
    children = user.get_children()  # Получить список детей
    if len(children) > 1:  # Не требуется, если на аккаунте только один ребёнок
        for i in range(len(children)):  # Позволить выбрать одного из детей
            first_name = children[i]["first_name"]
            last_name = children[i]["last_name"]
            print(i + 1, "-", first_name, last_name)

        number = input("\nВыберите ребёнка: ")
        user.child = int(number) - 1  # Выбрать нужного ребёнка

print(user.user)
