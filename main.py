#НЕ ЗНАЕШЬ - НЕ ТРОГАЙ
import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import string
from vk_api.utils import get_random_id
vk_session = vk_api.VkApi(token="vk1.a.K6eYXuEK8BY8qUaVGLIksmTeSYjgmkcDhllTUT58MrmIusZF1xFqeEn62C496gpojPfE67FKDFQrWmQfqecOZv68a3FYtCAEj3zGB-lz6kc-V4Lozuv8cMQ0Hznn0k8fZJU5Coh1l1Fdy7NO6uXcacg3sGzo38Idk_OUWfJSjTCKt0IiEf818TlmCrYUXBMp")
vk = vk_session.get_api()
longpool = VkLongPoll(vk_session)

#АНТИСПАМ
calls_time=dict()

#АДМИНИСТРАТОРЫ
admins=["245248572", "270130810"]
adf = open('admins.txt','r')
for g in adf.readlines():
    admins.append(g.rstrip())

adf.close();

#КЛАВИАТУРЫ (UI)
start = VkKeyboard(one_time=True)
start.add_button('Начать', color=VkKeyboardColor.POSITIVE)
# start

title = VkKeyboard(one_time=True)
title.add_button('Ozon', color=VkKeyboardColor.SECONDARY)
title.add_button('WB', color=VkKeyboardColor.SECONDARY)
title.add_line()
title.add_button('Меню', color=VkKeyboardColor.POSITIVE)
# title

menu = VkKeyboard(one_time=True)
menu.add_button('WB и Ozon', color=VkKeyboardColor.POSITIVE)
menu.add_line()
menu.add_button('Админ', color=VkKeyboardColor.PRIMARY)
menu.add_line()
menu.add_button('Хочу тату по своему эскизу', color=VkKeyboardColor.SECONDARY)
# Menu


Ozon = VkKeyboard(one_time=True)
Ozon.add_button('Ozon', color=VkKeyboardColor.SECONDARY)
Ozon.add_button('WB', color=VkKeyboardColor.SECONDARY)
Ozon.add_line()
Ozon.add_button('Меню', color=VkKeyboardColor.PRIMARY)
# WBandOzon

admin = VkKeyboard(one_time=True)
admin.add_button('Оплата и доставка', color=VkKeyboardColor.SECONDARY)
admin.add_line()
admin.add_button('Вы не обманете?', color=VkKeyboardColor.SECONDARY)
admin.add_line()
admin.add_button('Меню', color=VkKeyboardColor.NEGATIVE)
# Admin

self = VkKeyboard(one_time=True)
self.add_button('Оформить заказ', color=VkKeyboardColor.POSITIVE)
self.add_line()
self.add_button('Прайс', color=VkKeyboardColor.SECONDARY)
self.add_button('Меню', color=VkKeyboardColor.SECONDARY)
# SelfTatoo

Zakaz = VkKeyboard(one_time=True)
Zakaz.add_button('Вызвать администратора', color=VkKeyboardColor.POSITIVE)
Zakaz.add_line()
Zakaz.add_button('Меню', color=VkKeyboardColor.SECONDARY)
# Zakaz

AdminVizvan = VkKeyboard(one_time=True)
AdminVizvan.add_button('Классные эскизы', color=VkKeyboardColor.SECONDARY)
AdminVizvan.add_line()
AdminVizvan.add_button('Меню', color=VkKeyboardColor.SECONDARY)
# AdminVizvan

#КАСТОМНЫЕ ФУНКЦИИ
def send_msg_kboard(id, some_text, kboard):
    vk.messages.send(peer_id=id,message=some_text,keyboard=kboard.get_keyboard(),random_id=0)


def send_msg(id, some_text):
    vk.messages.send(peer_id=id,message=some_text,random_id=0)


def send_everyone(some_text):
    convers= vk.messages.getConversations()
    print(convers)
    for g in convers["items"]:
        send_msg(g['conversation']['peer']['id'], some_text)


def call_admins(id, some_text, kboard):
    if (id in calls_time):
        if ((datetime.datetime.now()-calls_time[id]).total_seconds()>500):
            send_msg_kboard(id, some_text,kboard)
            calls_time[id] = datetime.datetime.now()
            for g in admins:
                send_msg(g,"У пользователя возник вопрос:\r\nhttps://vk.com/gim214337181?sel=" + str(id))  # возможно тут надо что-то придумать
        else:
            send_msg_kboard(id, "Вы вызывали администратора недавно. Подождите еще "+str(int(500-((datetime.datetime.now()-calls_time[id]).total_seconds())))+" секунд. Если администраторы не отвечают, попробуйте позднее.", kboard)
    else:
        send_msg_kboard(id, some_text, kboard)
        calls_time[id] = datetime.datetime.now()
        for g in admins:
            send_msg(g, "У пользователя возник вопрос:\r\nhttps://vk.com/gim214337181?sel=" + str(id))  # возможно тут надо что-то придумать


#ОСНОВНОЙ ЦИКЛ ЛОГИКИ
for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            isadmin = (str(id) in admins);
            print(msg);
            print(isadmin);

            if (("adminsetup " in msg) and isadmin):
                try:
                    admins.append(msg[11:])
                    adf = open('admins.txt', 'w')
                    for h in admins:
                        adf.write(h+"\n")
                    adf.close();
                    send_msg_kboard(id, "Успешно", menu)
                except:
                    adf.close();
                    send_msg_kboard(id, "Ошибка", menu)

            if msg == "начать":
                send_msg_kboard(id, 'TATTS - бренд временных татуировок и накладных ноготочков. \r\n\r\n Мы есть на Ozon и Wildberries, тыкай меню, чтобы увидеть ссылки. \r\n\r\n Тут отвечает наш админ, а ещё подключен бот, для ответа на популярные вопросы. \r\n\r\n Запутаешься, пиши "Меню" ', title)

            if msg == "меню":
                send_msg_kboard(id,'Вызывай админстратора, если есть вопрос', menu)

            if msg == "wb и ozon":
                send_msg_kboard(id,'Бесплатная доставка за 1-3 дня по всей России О чём ещё можно мечтать? \r\n\r\n Ozon - \r\n\r\n Wildberries - ', Ozon)

            if msg == "админ":
                call_admins(id,'Что вас интересует? \r\n\r\n Опишите максимально подробно и ждите ответа. Наш администратор ждёт вашего вопроса.', admin)
            if msg == "хочу тату по своему эскизу":
                send_msg_kboard(id,'Как сделать заказ тату по своему эскизу? \r\n Создать свой эскиз - canva.com \r\n найти эскиз - pinterest.ru \r\n\r\n 1.Выбери эскиз \r\n 2.Подбери необходимый размер \r\n 3.Скинь эскизы в этот диалог \r\n 4.Оформи и оплати заказ\r\n 5.Жди свои татушечки\r\n\r\n Узнать цены - \r\nМинимальный заказ от 750руб.', self)

            if msg == "оформить заказ":
                send_msg_kboard(id,'Скидывай эскизы с размерами. Затем тыкай на кнопку "вызвать администратора" \r\n\r\n Он поможет тебе оформить заказ', Zakaz)

            if (("рассылка " in msg) and isadmin):
                send_everyone(event.text[9:])

            if msg == "прайс":
                send_msg_kboard(id,'У нас шаблонные размеры. Если у вас будет нестандартный размер, то вы всё равно платите за ---- тату \r\n\r\n К примеру, 9x8см всё равно будет стоить 249руб. \r\n\r\n Мальенький(5x5) - 159руб. \r\n Средний(10x10) - 249руб.\r\n Большой(10x15) - 349руб.\r\n Широкий(5x15) - 199руб. \r\n Высокий(15x5) - 199руб. \r\n Очень большой(15x20) - 549уб.', Zakaz)

            if msg == "вызвать администратора":
                call_admins(id, 'Администраторам пришло уведомление. С вами скоро свяжутся.', Zakaz)

