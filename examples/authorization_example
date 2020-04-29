from ruobr_api import Ruobr

try:
    user = Ruobr("username", "password")  # Авторизация
except Ruobr.AuthError:
    print("Проверьте логин и/или пароль!")
    quit()

if user.isApplicant:  # Обработка родительского аккаунта
    children = user.getChildren()  # Получить список детей
    if len(children) > 1:  # Не требуется, если на аккаунте только один ребёнок
        for i in range(len(children)): # Позволить выбрать одного из детей
            first_name = children[i]['first_name']
            last_name = children[i]['last_name']
            print(i + 1, "-", first_name, last_name)

        number = input("\nВыберите ребёнка: ")
        user.setChild(int(number) - 1)  # Выбрать нужного ребёнка

print(user.user)
