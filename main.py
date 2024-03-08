# Импорт необходимых библиотек и модулей
from vk_api import VkApi
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import data_file

# Константы для работы с VK API
GROUP_ID = '220351935'
GROUP_TOKEN = 'vk1.a.-lSk5BLyFF_XPscwyDEdZo0tEGcLvdvWWmcD0bQR4ih4_KecqFeCO3TtBVi09rYb8XzzL-Lw1IWPLytpwp1HFj5mWuYx5lfIyqvM1eUgOl3WDPwiCE-D1FEnJPhuIYEUJB7-R4XH2qdVgkPkpIC7XwL_EeEJa2q_Q5EoX5nM_9QfL0kjK4jd3IKZREBRHGypmyUzjhfq27chIMTK20yAmg'
API_VERSION = '5.120'

# Инициализация сессии VK и LongPoll
vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)


# Функция для генерации клавиатуры ответа
def reply_gen(flag=""):
    reply_keyboard = VkKeyboard(one_time=False, inline=False)
    reply_keyboard.add_openlink_button(label='Таблица со всеми промокодами!',
                                       link="https://docs.google.com/spreadsheets/d/1FhYGE5IODqbtXSfQGBs0BGUaUJYAWBGAC2SRWqYzf6M",
                                       payload={"type": "open_link",
                                                "link": "https://docs.google.com/spreadsheets/d/1FhYGE5IODqbtXSfQGBs0BGUaUJYAWBGAC2SRWqYzf6M"})
    if flag == "0":
        reply_keyboard.add_line()
        reply_keyboard.add_button(label='Запустить бота!', color=VkKeyboardColor.NEGATIVE, payload={"type": "text"})
    reply_keyboard.add_line()
    reply_keyboard.add_openlink_button(label='Мы в Телеграме!', link="https://t.me/skidkinezagorami",
                                       payload={"type": "open_link", "link": "https://t.me/skidkinezagorami"})
    if flag == "1":
        reply_keyboard.add_line()
        reply_keyboard.add_button(label='Меню!', color=VkKeyboardColor.NEGATIVE, payload={"type": "text"})

    return reply_keyboard


# Функция для создания слайдера
def slider(list_of_data, n, stage="", text="", flag_step="s", flag_data="d", count=5):
    slider_keyb = VkKeyboard(one_time=False, inline=True)
    end_point = min((n + 1) * count, len(list_of_data))

    for i in range(n * count, end_point):
        if stage == "c":
            slider_keyb.add_button(label=list_of_data[i], color=VkKeyboardColor.SECONDARY, payload={"type": 'text'})
            slider_keyb.add_line()
        elif stage == "m":
            slider_keyb.add_callback_button(label=list_of_data[i], color=VkKeyboardColor.SECONDARY,
                                            payload={"type": text, "market": list_of_data[i]})
            slider_keyb.add_line()
    if n > 0:
        slider_keyb.add_callback_button(label="Назад", color=VkKeyboardColor.PRIMARY,
                                        payload={"type": flag_step + str(n - 1), "stage": stage, "text": text})
    if end_point < len(list_of_data):
        slider_keyb.add_callback_button(label="Вперёд", color=VkKeyboardColor.PRIMARY,
                                        payload={"type": flag_step + str(n + 1), "stage": stage, "text": text})

    return slider_keyb


# Инициализация переменной
n = None

print("Ready")

# Список приветственных сообщений
HI = ["start", "Start", "начать", "Начало", "Начать", "начало", "Бот", "бот", "Старт", "старт", "скидки", "Скидки"]

# Инструкция для пользователя
text_inst = """
1. Для начала работы нажмите : "Запустить бота!".
2. Выберите нужную Вам  категорию, если не нашли на первой странице, нажмите : "Вперёд".
Затем введите номер нужной услуги и отправьте сообщением боту. 
3. Также вы всегда можете найти актуальный перечень всех акций и предложений нажав кнопку : "Таблица со всеми промокодами!".
4. Чтобы всегда оставаться на связи, подпишитесь на нас в телеграмм канале, нажав кнопку : "Мы в Телеграме!".
"""

# Основной цикл бота
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.obj.message['text'] != '':
            if event.from_user:
                if event.obj.message['text'] == 'Запустить бота!' or event.obj.message['text'] == "Меню!":
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        keyboard=slider(list(data_file.main_dict.keys()), 0, "c").get_keyboard(),
                        message='Выбирайте категорию:')

                elif event.obj.message['text'] in data_file.main_dict.keys():
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        keyboard=slider(data_file.main_dict[event.obj.message['text']], 0, "m",
                                        event.obj.message['text']).get_keyboard(),
                        message='Выбирайте магазин:')

                elif event.obj.message['text'] in HI:
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        keyboard=reply_gen("0").get_keyboard(),
                        message=text_inst)

    elif event.type == VkBotEventType.MESSAGE_EVENT:
        if event.object.payload.get('type')[0] == "s":
            if event.object.payload.get('stage') == "c":
                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message='Выбирайте категорию:',
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=slider(list(data_file.main_dict.keys()), int(event.object.payload.get('type')[1:]),
                                    "c").get_keyboard())
            elif event.object.payload.get('stage') == "m":
                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message='Выбирайте магазин:',
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=slider(data_file.main_dict[event.object.payload.get('text')],
                                    int(event.object.payload.get('type')[1:]), "m",
                                    event.object.payload.get('text')).get_keyboard())

        elif event.object.payload.get('market') in data_file.main_dict[event.object.payload.get('type')]:
            data_file.text_dict[event.object.payload.get('market')].append("Нажмите 'Меню!' для вызова главного меню.")
            for x in data_file.text_dict[event.object.payload.get('market')]:
                last_id = vk.messages.send(
                    user_id=event.obj['user_id'],
                    random_id=get_random_id(),
                    peer_id=event.obj['user_id'],
                    message=x,
                    keyboard=reply_gen("1").get_keyboard())
