

import vk_api  # Интерфейс для работы с базами Вк
import random
import requests  # HTTP библиотека
import lxml.html  # Библиотека обработки XML и HTML файлов

# Переменные
URL = "https://timetable.tusur.ru/faculties/"
FACULTIES_NAMES = ['fit', 'rtf', 'rkf', 'fet', 'fsu', 'fvs', 'gf', 'fb', 'ef', 'yuf', 'zivf']
GROUPS = ['01', '1', '2', '3', '4', '5', '6', '7', '8', '09', 'з']
DAYS = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'выход']
knopki1 = ['вопросы', 'расписание']
knopki = ['общежитие', 'стипендия', 'кружки', 'перевод с платного на бюджет', 'выход']
DAYS_N = [1, 2, 3, 4, 5, 6]
TRANSFORM = {'а': 'a', 'б': 'b', 'з': 'z', 'м': 'm', 'п': 'p', 'э': 'e', 'у': 'u'}
DAYS_TRUE = {'а': 'у'}
link = ''


# Функция получения ссылки
def get_html_group(url):
    return requests.get(url=url)


# Функция для получения информации о парах с сайта ТУСУРа
# Предмет, тип занятия, преподаватель
def get_wrapper(html_text, td):
    tree = lxml.html.document_fromstring(html_text)
    lessons = []
    # tr = Пара
    # td = День
    for i in range(1, 7):
        lessons.append("Пара №" + str(i))

        discipline = tree.xpath(
            f"//*[@id='wrapper']/div[6]/div[2]/div[3]/div/div[1]/table[2]/tbody/tr[{i}]/td[{td}]/div[1]/span[2]/text()")
        print(discipline)
        if not discipline:
            discipline = tree.xpath(
                f"//*[@id='wrapper']/div[6]/div[2]/div[3]/div/div[1]/table[2]/tbody/tr[{i}]/td[{td}]/div/div/div[1]/span[2]/abbr/text()")
        if not discipline:
            discipline = tree.xpath(
                f"//*[@id='wrapper']/div[6]/div[2]/div[3]/div/div[1]/table[2]/tbody/tr[{i}]/td[{td}]/div/div/div[1]/span[3]/abbr/text()")
        if not discipline:
            discipline = tree.xpath(
                f"//*[@id='wrapper']/div[6]/div[2]/div[3]/div/div[1]/table[2]/tbody/tr[{i}]/td[{td}]/div/div/div[1]/span[3]/text()")
        if not discipline:
            discipline = tree.xpath(
                f"//*[@id='wrapper']/div[6]/div[2]/div[3]/div/div[1]/table[2]/tbody/tr[{i}]/td[{td}]/div/div/div[2]/text()")
        if not discipline:
            discipline = tree.xpath(
                f"//*[@id='wrapper']/div[6]/div[2]/div[3]/div/div[1]/table[2]/tbody/tr[{i}]/td[{td}]/div/div/div[1]/span[3]/abbr/text()")

        kind = tree.xpath(
            f"//*[@id='wrapper']/div[6]/div[2]/div[3]/div/div[1]/table[2]/tbody/tr[{i}]/td[{td}]/div/div/div[1]/span[3]/text()")
        if not kind or kind == discipline:
            kind = tree.xpath(
                f"//*[@id='wrapper']/div[6]/div[2]/div[3]/div/div[1]/table[2]/tbody/tr[{i}]/td[{td}]/div/div/div[1]/span[4]/text()")

        teachers = tree.xpath(
            f"//*[@id='wrapper']/div[6]/div[2]/div[3]/div/div[1]/table[2]/tbody/tr[{i}]/td[{td}]/div/div/div[1]/span[5]/a/text()")
        if not teachers:
            teachers = tree.xpath(
                f"//*[@id='wrapper']/div[6]/div[2]/div[3]/div/div[1]/table[2]/tbody/tr[{i}]/td[{td}]/div/div/div[1]/span[6]/a/text()")

        if not discipline:
            pass
        elif discipline[0] == '\n    ':
            pass
        else:
            lessons.append(discipline)

        if not kind:
            pass
        else:
            lessons.append(kind)

        if not teachers:
            pass
        else:
            lessons.append(teachers)

        lessons.append("\n")
    print(lessons)
    return lessons


# Основной цикл программы
while True:
    token = "4d3f7b33a06b32e88d36cc1ff1ae3b0d024e21c64b5a718bc3f7fe25253770ae6cd02f4201090756205fe"  # Ключ доступа, скрыт в целях безопасности
    vk = vk_api.VkApi(token=token, api_version=5.74)
    vk._auth_token()
    message = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
    # Ниже идут все необходимые условия для взаимодействия с ботом
    if message["count"] > 0:
        text = message['items'][0]['last_message']['text']
        user_id = message['items'][0]['last_message']['from_id']
        if text.lower() == "start":  # При вводе команды "инфо", появляются две кнопки - вопросы и расписание
            vk.method("messages.send",
                      {
                          "user_id": user_id,
                          "message": "Выберите на кнопках, что вас интересует",
                          "keyboard": open('keyboard_menu.json', 'r', encoding='UTF8').read(),
                          "random_id": random.randint(1, 1000)
                      })
        print(text.lower())
        if text.lower() == "вопросы":  # При выборе кнопки "вопросы" на экран выводится сообщение с предлождением выбрать вопрос
            vk.method("messages.send",
                      {
                          "user_id": user_id,
                          "message": 'Информация взята с сайта ТУСУРа или основана на личном опыте\n\nВыберите интересующую вас тему',
                          "keyboard": open('keyboard_menu_vopr.json', 'r', encoding='UTF8').read(),
                          "random_id": random.randint(1, 1000)
                      })
            print(text.lower())
            while True:  # Цикл отправки ответа пользователю на выбранный вопрос
                message = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
                if message["count"] > 0:
                    text = message['items'][0]['last_message']['text']
                    user_id = message['items'][0]['last_message']['from_id']
                    print(text.lower())
                    if text.lower() != "выход" :  # Для выхода из вопросов нужно написать "выход" или выбрать соответстующую кнопку
                        print(text.lower())

                        if text.lower() == "абитуриент":  # Отправка ответа пользователю при выборе вопроса "перевод с платного на бюджет"
                            vk.method("messages.send",
                                      {
                                          "user_id": user_id,
                                          "message": 'ТУСУР приветствует вас! Мы рады видеть здесь всех! Абитуриентов, родителей абитуриентов, наших студентов и выпускников – всех, кому не безразличен наш университет. \n'
                                                     'Здесь можно задавать любые вопросы о поступлении, учёбе, творчестве, спорте и быте студентов – мы ответим на все!\n'
                                                     'Присоединяйтесь к нашей группе и подписывайтесь на новости!\n'
                                                     'https://vk.com/mytusur\n\n'
                                                     'Более обширную информацию можете узнать тут:\nhttps://vk.com/abiturient_tusur\n',
                                          "random_id": random.randint(1, 1000)
                                      })
                            vk.method("messages.send",
                                      # Отправка сообщения о выходе из вопросов и появление кнопок вопросы и расписание
                                      {
                                          "user_id": user_id,
                                          "message": 'Выберите на кнопках, что вас интересует',
                                          "keyboard": open('keyboard_menu.json', 'r', encoding='UTF8').read(),
                                          "random_id": random.randint(1, 1000)
                                      })
                            break
                        if text.lower() == "общежитие":  # Отправка ответа пользователю при выборе вопроса "общежитие"
                            vk.method("messages.send",
                                      {
                                          "user_id": user_id,
                                          "message": 'У нас всего 4 общежития :\n3 - https://vk.com/studsovet_3\n4 - https://vk.com/4ka_tusur\n6 - https://vk.com/tusur_hostel_6\n'
                                                     '5 - https://vk.com/tusur_hostel5 (на ремонте\U0001F614)\n\n'
                                                     'Выше представленны официальные сообщества каждого из общежитий, в каждом из них предствлена актуальная информация\n\n'
                                                     'Страница на сайте ТУСУРа, где размещенная информация о том как заселиться, о правилах проживания, оплате за общежитие и инфраструктуре\nhttps://tusur.ru/ru/studentam/zhizn-v-obschezhitii',
                                          "random_id": random.randint(1, 1000)
                                      })
                            vk.method("messages.send",
                                      {
                                          "user_id": user_id,
                                          "message": 'Ещё "пару слов" об общежитии можно выбрать на клавиатуре',
                                          "keyboard": open('keyboard_menu_obsh.json', 'r', encoding='UTF8').read(),
                                          "random_id": random.randint(1, 1000)
                                      })
                            while True:  # Цикл отправки ответа пользователю на выбранный вопрос ообщага
                                message = vk.method("messages.getConversations",
                                                    {"offset": 0, "count": 20, "filter": "unanswered"})
                                if message["count"] > 0:
                                    text = message['items'][0]['last_message']['text']
                                    user_id = message['items'][0]['last_message']['from_id']
                                    print(text.lower())
                                    if text.lower() != "start":  # Для выхода из вопросов нужно написать "выход" или выбрать соответстующую кнопку
                                        print(text.lower())
                                        if text.lower() == "в какое пойти и какое лучше?":
                                            vk.method("messages.send",
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Всё зависит от того есть или нет мест в конкретном общежитие, тут всё индивидуально и нужно узнавать у заселитей\n\n'
                                                                     'В данный момент самое комфортное общежитие для "простых смертных" это 4 общежитие, так как:\n'
                                                                     '1) Она секционная\n'
                                                                     '2) В ней сделан ремонт\n'
                                                                     '3) В комнате проживает по два человека\n',
                                                          "random_id": random.randint(1, 1000)
                                                      })
                                        if text.lower() == "правила":
                                                vk.method("messages.send",
                                                          {
                                                              "user_id": user_id,
                                                              "message": 'Для всех тех кто никогда не жил в общежитие и не знает что да как\n'
                                                                         'В общежитие существуют правила, которые необходимо выполять и которые запрещают некторые действия.\n'
                                                                         'Полный свод правил, запретов и обязностей вы можете прочитать в "Правилах внутреннего распорядка"\n'
                                                                         'https://abiturient.tusur.ru/storage/9902/pravila_prozchivaniya.pdf\n\n'
                                                                         'На личном опыте наиболее часто нарушаемые правила за которые можно получить атата и лучше следить за собой\n'
                                                                         '1) Соблюдать технику пожарной безопасности (сигареты фу, алкоголь фу)\n'
                                                                         '2) Исполнять дежурство\n3) Не шуметь после 11.00 (желательно \U0001F61C) \n'
                                                                         'Вежливое общение приветствуется \U0001F643',
                                                              "random_id": random.randint(1, 1000)
                                                          })
                                        if text.lower() == "организации":
                                                vk.method("messages.send",
                                                          {
                                                              "user_id": user_id,
                                                              "message": '1) Студсовет - отвечают за жизнь и урегулирование конфликтов в общежитие.\n2) СООПР - следят за порядком в общежитие.\n'
                                                                         '3) Санитарная комиссия (Сам ком) - проверяют комнаты чтобы были в чистоте и порядке\n',
                                                              "random_id": random.randint(1, 1000)
                                                          })
                                        if text.lower() == "лайфхак":
                                                vk.method("messages.send",
                                                          {
                                                              "user_id": user_id,
                                                              "message": 'Cамый главый лайфхак - это не косячить \U0001F643',
                                                              "random_id": random.randint(1, 1000)
                                                          })

                                    else:
                                        vk.method("messages.send",

                                                  {
                                                      "user_id": user_id,
                                                      "message": 'Вышли из вопросов',
                                                      "keyboard": open('keyboard_menu.json', 'r',
                                                                       encoding='UTF8').read(),
                                                      "random_id": random.randint(1, 1000)
                                                  })
                                    break
                            vk.method("messages.send",
                                      # Отправка сообщения о выходе из вопросов и появление кнопок вопросы и расписание
                                      {
                                          "user_id": user_id,
                                          "message": 'Вышли из вопросов',
                                          "keyboard": open('keyboard_menu.json', 'r', encoding='UTF8').read(),
                                          "random_id": random.randint(1, 1000)
                                      })
                            break
                        if text.lower() == "перевод с платного на бюджет":  # Отправка ответа пользователю при выборе вопроса "перевод с платного на бюджет"
                            vk.method("messages.send",
                                      {
                                          "user_id": user_id,
                                          "message":'Перевод с платного на бюджет возможен, но нужно учитывать несколько факторов:\n1) Успеваемость в учебе (отсутствие долгов)'
                                                     '\n2) Активность в жизни вуза \n'
                                                     '3) Рейтинг (об этом ниже)\n'
                                                     '4) Наличие свободных мест на вашем направлении\n\n'
                                                     'Для перевода необходимо закончить две сессии без троек, чем выше оценки полученные за экзамены тем вы выше в рейтинге.Рейтинг состоит из таких же как вы платников мечтающих о бюджете\n\n'
                                                     'То есть как минимум год вам придеться отучиться на платном и потом если появится бюджетное место (кого-то отчислят), и вы по рейтингу первый на это место (у вас все пятёрки за все прошлые экзамены, идеальный вариант)'
                                                     'вас могут перевести на бюджет.\n\n'
                                                     'Для этого нужно прийти в свой деканат и заполнить соответствующие заявление'
                                                     'Положение и правила о переводе с платного на бюджет можно прочесть в официальном документе на сайте ТУСУРа\nhttps://regulations.tusur.ru/documents/614',
                                          "random_id": random.randint(1, 1000)
                                      })
                            vk.method("messages.send",
                                      # Отправка сообщения о выходе из вопросов и появление кнопок вопросы и расписание
                                      {
                                          "user_id": user_id,
                                          "message": 'Вышли из вопросов',
                                          "keyboard": open('keyboard_menu.json', 'r', encoding='UTF8').read(),
                                          "random_id": random.randint(1, 1000)
                                      })
                            break
                        if text.lower() == "стипендия":  # Отправка ответа пользователю при выборе вопроса "стипендия"
                            vk.method("messages.send",
                                      {
                                          "user_id": user_id,
                                          "message": 'Стипендия выплачивается только обучающимся на бесплатном обучении\n\n'
                                                     'Твоя стипендия будет зависить от успеваемости в учёбе и активности в жизни вуза\n\n'
                                                     'Всем студентам 1 курса выплачивается стипендия в размере 3 419р\n'
                                                     'Но если ты набрал за егэ больше 240 баллов то будешь получать 8 619р\n\n'
                                                     '1) Если закончил сессию хотя бы с одной 3, то скажи стипендии пока (её не будет)\n'
                                                     '2) Если закончил сессию только на 4 то твоя стипендия будет равна 2 500р\n'
                                                     '3) Если закончил сессию на 4 и 5 то получишь заслуженные 2 843р\n'
                                                     '4) Если закончил сессию на 5 то твоя стипендия будет 3 981р\n\n'
                                                     'В приказе об установлении размеров стипендии можно ознакомиться более детальнее с информацией\nhttps://regulations.tusur.ru/documents/664\n\n'
                                                     'О других возможностях увеличить свою стипендию вы можете прочитать тут\n'
                                                     'https://tusur.ru/ru/studentam/stipendii-i-materialnaya-pomosch',
                                          "random_id": random.randint(1, 1000)
                                      })
                            vk.method("messages.send",
                                      {
                                          "user_id": user_id,
                                          "message": 'Можете выбрать ещё один из вопросов или выйти',
                                          "keyboard": open('keyboard_menu_step.json', 'r', encoding='UTF8').read(),
                                          "random_id": random.randint(1, 1000)
                                      })

                            while True:  # Цикл отправки ответа пользователю на выбранный вопрос ообщага
                                message = vk.method("messages.getConversations",
                                                    {"offset": 0, "count": 20, "filter": "unanswered"})
                                if message["count"] > 0:
                                    text = message['items'][0]['last_message']['text']
                                    user_id = message['items'][0]['last_message']['from_id']
                                    print(text.lower())
                                    if text.lower() != "выход":  # Для выхода из вопросов нужно написать "выход" или выбрать соответстующую кнопку
                                        print(text.lower())
                                        if text.lower() == "мат-помощь":
                                            vk.method("messages.send",
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Материальную помощь могут получать только бесплатники\n'
                                                                     'Также обязательным условием является участие в профсоюзе\n'
                                                                     'https://vk.com/ppos_tusur\n\n'
                                                                     'Мат.помощь бывает различная и очень упращает жизнь простому студенту.\n\n'
                                                                     'В мат.помощь входит множество причин по которым вы можете подойти, с полным списком вы можете ознакомиться здесь\n'
                                                                     'https://tusur.ru/ru/studentam/stipendii-i-materialnaya-pomosch\n\n'
                                                                     'Можно выделить по опыту, мат. помощь помогает, но к сожалению до 2 курса, после чего по многим пунктам вы уже не сможете оформить её.\n'
                                                                     'Актуальной информацией по поводу мат. помощи обладает деканат или староста (если ей передали информацию с деканата)\n'
                                                                     'Более точную информацию можно спросить в деканате или же у старосты поскольку чаще всего они осведомлины касаемо данных вопросов.\n',
                                                          "random_id": random.randint(1, 1000)
                                                      })
                                            vk.method("messages.send",
                                                      # Отправка сообщения о выходе из вопросов и появление кнопок вопросы и расписание
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Вышли из вопросов мат.помощь',
                                                          "keyboard": open('keyboard_menu.json', 'r',
                                                                           encoding='UTF8').read(),
                                                          "random_id": random.randint(1, 1000)
                                                      })
                                        if text.lower() == "повышенная":
                                            vk.method("messages.send",
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Можно получить за:\n1) Активное участие в жизни вуза\n2) Особые достижение, о номинициях можно прочесть здесь\nhttps://tusur.ru/ru/studentam/stipendii-i-materialnaya-pomosch\n'
                                                          '3) За счет грантов и премий\n\n'
                                                          'C правилами назначения и выплаты повышенной стипендии можно ознакомиться в оф. документе\nhttps://regulations.tusur.ru/documents/33',
                                                          "random_id": random.randint(1, 1000)
                                                      })
                                            vk.method("messages.send",
                                                      # Отправка сообщения о выходе из вопросов и появление кнопок вопросы и расписание
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Вышли из вопросов повышенная',
                                                          "keyboard": open('keyboard_menu.json', 'r',
                                                                           encoding='UTF8').read(),
                                                          "random_id": random.randint(1, 1000)
                                                      })

                                    else:
                                        vk.method("messages.send",
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Вышли из вопросов ',
                                                          "keyboard": open('keyboard_menu.json', 'r',
                                                                           encoding='UTF8').read(),
                                                          "random_id": random.randint(1, 1000)
                                                      })
                                    break
                            break
                        if text.lower() == "организации-вуза":  # Отправка ответа пользователю при выборе вопроса "кружки"
                            vk.method("messages.send",
                                      {
                                          "user_id": user_id,
                                          "message": 'Различные Информация о них на сайте ТУСУРа https://tusur.ru/ru/studentam/studotryady \n'
                                                     'https://tusur.ru/ru/studentam/kluby-po-interesam-i-volonterstvo \n',
                                          "random_id": random.randint(1, 1000)
                                      })
                            vk.method("messages.send",
                                      {
                                          "user_id": user_id,
                                          "message": 'Выберите вопрос',
                                          "keyboard": open('keyboard_menu_org.json', 'r', encoding='UTF8').read(),
                                          "random_id": random.randint(1, 1000)
                                      })

                            while True:  # Цикл отправки ответа пользователю на выбранный вопрос ообщага
                                message = vk.method("messages.getConversations",
                                                    {"offset": 0, "count": 20, "filter": "unanswered"})
                                if message["count"] > 0:
                                    text = message['items'][0]['last_message']['text']
                                    user_id = message['items'][0]['last_message']['from_id']
                                    print(text.lower())
                                    if text.lower() != "выход":  # Для выхода из вопросов нужно написать "выход" или выбрать соответстующую кнопку
                                        print(text.lower())
                                        if text.lower() == "ик":
                                            vk.method("messages.send",
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Занимаються курированием 1 курс помогают освоиться с студенческой жизнью.\n'
                                                                     'Если есть вопросы всегда помогут (Но не донимайте их сильно они же тоже люди)\n'
                                                                     'https://vk.com/ik_ppos_tusur',
                                                          "random_id": random.randint(1, 1000)
                                                      })
                                            vk.method("messages.send",
                                                      # Отправка сообщения о выходе из вопросов и появление кнопок вопросы и расписание
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Вышли из вопросов ИК',
                                                          "keyboard": open('keyboard_menu.json', 'r',
                                                                           encoding='UTF8').read(),
                                                          "random_id": random.randint(1, 1000)
                                                      })
                                        if text.lower() == "сок":
                                            vk.method("messages.send",
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Спортивно-оздоровительная комиссия создана в целях оказания помощи администрации вуза в организации отдыха и оздоровления студентов\n'
                                                                     'если что вот https://vk.com/sok_tusur "',
                                                          "random_id": random.randint(1, 1000)
                                                      })
                                            vk.method("messages.send",
                                                      # Отправка сообщения о выходе из вопросов и появление кнопок вопросы и расписание
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Вышли из вопросов СОК',
                                                          "keyboard": open('keyboard_menu.json', 'r',
                                                                           encoding='UTF8').read(),
                                                          "random_id": random.randint(1, 1000)
                                                      })
                                        if text.lower() == "студ-отряды":
                                            vk.method("messages.send",
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Занимаються в основном активным туризмом,волонтеры\nhttps://vk.com/shtabsotusur',
                                                          "random_id": random.randint(1, 1000)
                                                      })
                                            vk.method("messages.send",
                                                      # Отправка сообщения о выходе из вопросов и появление кнопок вопросы и расписание
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Вышли из вопросов студ отряды',
                                                          "keyboard": open('keyboard_menu.json', 'r',
                                                                           encoding='UTF8').read(),
                                                          "random_id": random.randint(1, 1000)
                                                      })
                                        if text.lower() == "наш формат":
                                            vk.method("messages.send",
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Занимаються в основном волонтерством. Цель их волонтёрской службы ТУСУРа - состоит в вовлечении студентов, аспирантов, преподавателей и сотрудников \n'
                                                                     'ТУСУРа в активизацию и развитие волонтёрского движения в ТУСУРе, а также в участие во Всемирном добровольческом движении. https://vk.com/shtabsotusur \n"',
                                                          "random_id": random.randint(1, 1000)
                                                      })
                                            vk.method("messages.send",
                                                      # Отправка сообщения о выходе из вопросов и появление кнопок вопросы и расписание
                                                      {
                                                          "user_id": user_id,
                                                          "message": 'Вышли из вопросов повышенная',
                                                          "keyboard": open('keyboard_menu.json', 'r',
                                                                           encoding='UTF8').read(),
                                                          "random_id": random.randint(1, 1000)
                                                      })
                                    else:
                                        vk.method("messages.send",
                                                  {
                                                      "user_id": user_id,
                                                      "message": 'Вышли из вопросов ',
                                                      "keyboard": open('keyboard_menu.json', 'r',
                                                                       encoding='UTF8').read(),
                                                      "random_id": random.randint(1, 1000)
                                                  })
                                    break
                            break
                    else:
                        vk.method("messages.send",
                                  # Отправка сообщения о выходе из вопросов и появление кнопок вопросы и расписани
                                  {
                                      "user_id": user_id,
                                      "message": 'Вышли из вопросов',
                                      "keyboard": open('keyboard_menu.json', 'r', encoding='UTF8').read(),
                                      "random_id": random.randint(1, 1000)
                                  })
                    break


        if text.lower() == "расписание":  # При выборе кнопки "расписание" на экран выводится сообщение с просьбой ввести номер группы
            vk.method("messages.send",
                      {
                          "user_id": user_id,
                          "message": 'выбрал "Рассписание \n Введите номер группы, например "438-1"',
                          "random_id": random.randint(1, 1000)
                      })
            while True:  # Цикл отправки информации парах
                message = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
                if message["count"] > 0:
                    text = message['items'][0]['last_message']['text']
                    user_id = message['items'][0]['last_message']['from_id']
                    if text.lower() != "выход":  # Для выхода из расписания нужно написать "выход" или выбрать соответстующую кнопку
                        if text.lower() in DAYS:
                            if not link:  # Проверка корректности введённых данных
                                vk.method("messages.send",
                                          {
                                              "user_id": user_id,
                                              "message": "Проверьте правильность вводимых данных",
                                              "random_id": random.randint(1, 1000)
                                          })
                                break
                            # Получение информации о парах
                            index = DAYS.index(text.lower())
                            html_text = get_html_group(link)
                            print(html_text)
                            if html_text.status_code == 200:
                                List = get_wrapper(html_text.text, DAYS_N[index])
                                print(List)
                                messages = ''

                                for inner_list in List:
                                    for i in range(len(inner_list)):
                                        item = inner_list[i]
                                        if not item:
                                            pass
                                        else:
                                            messages += item
                                    messages += '\n'

                                temp = text.lower()
                                # Отправка пользователю сообщения с раписанием на выбранный день
                                for i, j in DAYS_TRUE.items():
                                    temp = temp.replace(i, j)
                                vk.method("messages.send",
                                          {
                                              "user_id": user_id,
                                              "message": "Расписание на " + temp + "\n" + messages,
                                              "random_id": random.randint(1, 1000)
                                          })
                                vk.method("messages.send",
                                          # Отправка сообщения пользователю с просьбой выбрать день недели и вывод кнопок с днями нелели, кнопки выход
                                          {
                                              "user_id": user_id,
                                              "message": '\nВведите день недели или номер группы..',
                                              "keyboard": open('keyboard_day.json', 'r', encoding='UTF8').read(),
                                              "random_id": random.randint(1, 1000)
                                          })

                            else:  # Проверка на крректность ввода группы
                                vk.method("messages.send",
                                          {
                                              "user_id": user_id,
                                              "message": "Проверьте правильность ввода группы",
                                              "random_id": random.randint(1, 1000)
                                          })

                        elif text[0].lower() in GROUPS or (text[0].lower() + text[1].lower()) in GROUPS:
                            if text[0].lower() == '0' and text[1].lower() == '9':
                                index = GROUPS.index(text[0].lower() + text[1].lower())
                            elif text[0].lower() == '0' and text[1].lower() == '1':
                                index = GROUPS.index(text[0].lower() + text[1].lower())
                            else:
                                index = GROUPS.index(text[0].lower())
                                temp = text.lower()
                            for i, j in TRANSFORM.items():
                                temp = temp.replace(i, j)
                            link = URL + FACULTIES_NAMES[index] + '/groups/' + temp
                            vk.method("messages.send",
                                      # Отправка сообщения пользователю с просьбой выбрать день недели и вывод кнопок с днями нелели, кнопки выход
                                      {
                                          "user_id": user_id,
                                          "message": "Выберите день, для группы " + text.lower() + "\n",
                                          "keyboard": open('keyboard_day.json', 'r', encoding='UTF8').read(),
                                          "random_id": random.randint(1, 1000)
                                      })
                    else:
                        vk.method("messages.send",  # Отправка сообщения пользователю
                                  {
                                      "user_id": user_id,
                                      "message": 'Вышли из рассписание',
                                      "keyboard": open('keyboard_menu.json', 'r', encoding='UTF8').read(),
                                      "random_id": random.randint(1, 1000)
                                  })
                        break
