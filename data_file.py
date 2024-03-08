import gspread

# Инициализация глобальных словарей
main_dict = {}
text_dict = {}
stat_cat_dict = {}
stat_markets_dict = {}


def regenerate():
    global main_dict, text_dict, stat_cat_dict, stat_markets_dict

    # Инициализация клиента gspread и открытие таблицы
    gc = gspread.service_account(filename="midyear-cursor-379909-cc15f63beea0.json")
    sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1FhYGE5IODqbtXSfQGBs0BGUaUJYAWBGAC2SRWqYzf6M')
    worksheet = sht2.sheet1

    # Получение всех значений из таблицы
    main_list = worksheet.get_all_values()

    # Очистка словарей перед заполнением
    main_dict.clear()
    text_dict.clear()
    stat_cat_dict.clear()
    stat_markets_dict.clear()

    # Обработка каждого элемента в списке
    for el in main_list[1:]:
        # Добавление элемента в main_dict
        main_dict.setdefault(el[8], []).append(el[0])

        # Формирование текста сообщения
        text = f"Название: {el[0]}\nСкидка: {el[3]}\nСсылка: {el[4]}\nДействует до: {el[5]}\nРегион: {el[6]}\nУсловия акции: {el[7]}\nПромокод ниже⬇️ \n"

        # Добавление текста и промокода в text_dict
        text_dict.setdefault(el[0], []).extend([text, el[2]])

        # Заполнение stat_cat_dict и stat_markets_dict
        for k, v in main_dict.items():
            stat_cat_dict[k] = []
            for x in v:
                stat_markets_dict[x] = []


# Вызов функции для заполнения словарей
regenerate()
