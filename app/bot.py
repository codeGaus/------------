
import telebot
import sqlite3
import redis
import crud
import re
from datetime import datetime

from tokens import API_TOKEN


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
redis_client.flushdb()

bot = telebot.TeleBot(API_TOKEN)

database_name = "salon_database.db"
database_path = f"databases/{database_name}"

# Словарь для хранения состояний пользователей
users_state = {}


def check_date_format(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def check_time_format(time_string):
    pattern = re.compile(r'^([01]?[0-9]|2[0-3])-[0-5][0-9]$')
    return bool(pattern.match(time_string))


# Регистрация
def registration(message, type):
    if type == 'name':
        chat_id = message.chat.id
        tg_id = message.from_user.id
        name = message.text

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Customer (customer_id, name, tg_id) VALUES (?, ?, ?)", (tg_id, name, tg_id))
        conn.commit()
        conn.close()

        text = "Спасибо, теперь введите ваш email:"

    elif type == 'email':
        chat_id = message.chat.id
        tg_id = message.from_user.id
        email = message.text

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE Customer SET email = ? WHERE tg_id = ?", (email, tg_id))
        conn.commit()
        conn.close()

        text = "Отлично, введите ваш номер телефона в формате +79991112233:"

    elif type == 'phone':
        chat_id = message.chat.id
        tg_id = message.from_user.id
        phone_number = message.text

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE Customer SET phone_number = ? WHERE tg_id = ?", (phone_number, tg_id))
        conn.commit()
        conn.close()

        text = "Введите вашу дату рождения в формате ГГГГ-ММ-ДД (например, 1990-01-01):"
    elif type == 'birthday':
        chat_id = message.chat.id
        tg_id = message.from_user.id
        birthdate = message.text

        if not check_date_format(birthdate):
            text = "Вы ввели неверную дату! Введите вашу дату рождения в формате ГГГГ-ММ-ДД (например, 1990-01-01):"
        else:
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE Customer SET birthdate = ? WHERE tg_id = ?", (birthdate, tg_id))
            conn.commit()
            conn.close()
            conn.close()

            text = "Регистрация завершена. Спасибо! \nМожете посмотреть список наших услуг /services и акций /promotions"

    return text


# Запись на прием
def appointment(message, type, service_id=None):
    buttons = []

    if type == 'appointment_service':
        chat_id = message.chat.id
        tg_id = message.from_user.id

        service = message.text
        print(service)

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Service WHERE service_name = '{service}'")
        service_id = cursor.fetchone()[0]
        conn.close()

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Appointment (customer_id, service_id) VALUES (?, ?)", (tg_id, service_id))
        conn.commit()
        conn.close()

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Employee")
        data = cursor.fetchall()
        conn.close()

        buttons = []
        for d in data:
            buttons.append(d[1])

        text = "Выберите мастера по данной услуге: "

    elif type == 'appointment_employee':
        chat_id = message.chat.id
        tg_id = message.from_user.id
        empoloyee = message.text

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Employee WHERE name = '{empoloyee}'")
        empoloyee_id = cursor.fetchone()[0]
        conn.close()

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE Appointment
            SET employee_id = ?
            WHERE
                1 = 1
                and customer_id = {int(tg_id)}
                and appointment_id = (
                    SELECT MAX(appointment_id)
                    FROM Appointment
                    WHERE customer_id = {int(tg_id)}
                )
            """,
            (empoloyee_id,))
        print(empoloyee_id, tg_id)
        conn.commit()
        conn.close()

        text = "Введите дату для записи в формате ГГГГ-ММ-ДД (например, 1990-01-01):"

    elif type == 'appointment_date':
        chat_id = message.chat.id
        tg_id = message.from_user.id
        appointment_date = message.text

        if not check_date_format(appointment_date):
            text = "Вы ввели неверную дату! Введите дату для записи в формате ГГГГ-ММ-ДД (например, 1990-01-01):"
        else:

            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                UPDATE Appointment
                SET appointment_date = ?
                WHERE
                    1 = 1
                    and customer_id = {int(tg_id)}
                    and appointment_id = (
                        SELECT MAX(appointment_id)
                        FROM Appointment
                        WHERE customer_id = {int(tg_id)}
                    )
                """,
                (appointment_date,))
            conn.commit()
            conn.close()

            text = "Введите время для записи в формате ЧАСЫ-МИНУТЫ (например, 22-30):"

    elif type == 'appointment_time':
        chat_id = message.chat.id
        tg_id = message.from_user.id
        appointment_time = message.text

        if not check_time_format(appointment_time):
            text = 'Вы ввели неверное время! Введите время для записи в формате ЧАСЫ-МИНУТЫ (например, 22-30):'
        else:
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                UPDATE Appointment
                SET appointment_time = ?
                WHERE
                    1 = 1
                    and customer_id = {int(tg_id)}
                    and appointment_id = (
                        SELECT MAX(appointment_id)
                        FROM Appointment
                        WHERE customer_id = {int(tg_id)}
                    )
                """,
                (appointment_time,))
            conn.commit()
            conn.close()

            text = "Вы записаны на услугу!"

    return text, buttons


# ----------------------------------------------------------------------

# Команда для просмотра услуг
@bot.message_handler(commands=['services'])
def handle_services(message):
    # Используйте Redis для кэширования данных о услугах
    services = redis_client.get('services')
    if not services:
        # Загрузка данных из базы данных, если кэш пуст
        services = crud.read_service()
        text = 'Наши услуги'
        for serv in services:
            text += f'\n\n✅ {serv[-3]} \nОписание услуги: {serv[-2]} \nСтоимость: {serv[-1]} рублей'
        services = text
        print(services)
        redis_client.set('services', services)
    bot.reply_to(message, services)


# Команда для просмотра акций
@bot.message_handler(commands=['promotions'])
def handle_promotion(message):
    # Используйте Redis для кэширования данных о услугах
    promotions = redis_client.get('promotions')
    if not promotions:
        # Загрузка данных из базы данных, если кэш пуст
        promotions = crud.read_promotion()
        text = 'Промоакции'
        for prom in promotions:
            text += f'\n\n👑 {prom[1]} \nОписание: {prom[-1]} \nДаты: {prom[2].replace('-', '.')} - {prom[3].replace('-', '.')}'
        promotions = text
        print(promotions)
        redis_client.set('promotions', promotions)
    bot.reply_to(message, promotions)


# Команда для просмотра скидок
@bot.message_handler(commands=['discounts'])
def handle_discount(message):
    # Используйте Redis для кэширования данных о услугах
    discounts = redis_client.get('discounts')
    if not discounts:
        # Загрузка данных из базы данных, если кэш пуст

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT service_name, discount_percentage, price  FROM Discount LEFT JOIN Service ON Discount.service_id = Service.service_id")
        data = cursor.fetchall()
        conn.close()

        text = 'Скидки'
        for dis in data:
            service_name = dis[0]
            price = dis[2]
            discount = dis[1]
            text += f'\n\n🔥 {service_name} \nCтоимость: {price} руб. \nСкидка: {discount}%'
        discounts = text
        print(discounts)
        redis_client.set('discounts', discounts)
    bot.reply_to(message, discounts)


# Команда для просмотра своих записей
@bot.message_handler(commands=['my_appointments'])
def handle_my_appointments(message):
    tg_id = message.from_user.id
    chat_id = message.chat.id

    # Загрузка данных из базы данных
    appointments = crud.read_appointment_by_customer_id(tg_id)
    print(appointments)
    if appointments:
        text = 'Ваши записи:'
        for app in appointments:
            employee = crud.read_employee(app[2])
            print(employee)
            employee_name = '-'
            employee_phone = '-'
            if employee:
                employee_name = employee[1]
                employee_phone = employee[3]

            service = crud.read_service(app[3])
            service_name = service[2]
            service_price = service[-1]

            date = app[4]
            time = app[5]
            text += f'\n\n💎{service_name}💎 \n\nМастер: {employee_name} (моб. {employee_phone})'
            text += f'\nСтоимость: {service_price} руб. \n\nДата: {date.replace('-', '.')} \nВремя: {time}'

        text += '\n\n❗️Для отмены записи свяжитесь с Вашим мастером по номеру его телефона'
    else:
        text = 'У вас пока нет записей. Нажмите /appointment, чтобы записаться на услугу'
    print(text)
    bot.send_message(chat_id, text)


# Команда для просмотра информации о себе
@bot.message_handler(commands=['about_me'])
def handle_about_me(message):
    tg_id = message.from_user.id
    chat_id = message.chat.id
    customer = crud.read_customer_by_tg(tg_id)
    if customer:
        text = 'Информация о Вас'
        text += f'\n\nИмя: {customer[1]} \nАдрес электронной почты: {customer[2]} \nНомер телефона: {customer[3]} \nДень рождения: {customer[4]} '
    else:
        text = 'Вы не зарегистрированы'
    bot.send_message(chat_id, text)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    tg_id = message.from_user.id
    chat_id = message.chat.id
    customer = crud.read_customer_by_tg(tg_id)
    print(customer)
    if not customer:
        users_state[chat_id] = 'name'
        bot.send_message(message.chat.id, 
                         "Добро пожаловать! Пожалуйста, введите ваши фамилию и имя в формате Фамилия Имя:",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=telebot.types.ReplyKeyboardRemove())


# Обработчик команды /delete_me
@bot.message_handler(commands=['delete_me'])
def delete_me(message):
    tg_id = message.from_user.id
    chat_id = message.chat.id
    customer = crud.read_customer_by_tg(tg_id)

    if customer:
        crud.delete_customer(customer[0])
        crud.delete_appointment_by_customer(tg_id)
    bot.send_message(chat_id, "Данные о Вас удалены. Нажмите /start, чтобы начать регистрацию")


# Обработчик записи на прием
@bot.message_handler(commands=['appointment'])
def handle_appointment(message):
    tg_id = message.from_user.id
    chat_id = message.chat.id
    customer = crud.read_customer_by_tg(tg_id)
    print(customer)
    if customer:
        print('STATE SERVICE')

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * from Service")
        data = cursor.fetchall()
        conn.close()
        print(data)

        buttons = []
        for d in data:
            buttons.append(d[2])

        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        users_state[chat_id] = 'appointment_service'
        bot.send_message(chat_id, "Выберите услугу:", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Вам нужно зарегистрироваться! Нажмите /start")


# Обработчик ввода данных
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    state = users_state.get(chat_id)

    # if state in ['name', 'email', 'phone', 'birthday']:
    if state == 'name':
        text = registration(message, state)
        users_state[chat_id] = 'email'
        bot.send_message(chat_id, text)
    elif state == 'email':
        text = registration(message, state)
        users_state[chat_id] = 'phone'
        bot.send_message(chat_id, text)
    elif state == 'phone':
        text = registration(message, state)
        users_state[chat_id] = 'birthday'
        bot.send_message(chat_id, text)
    elif state == 'birthday':
        text = registration(message, state)
        if "неверную" in text:
            users_state[chat_id] = 'birthday'
            bot.send_message(chat_id, text)
        else:
            users_state[chat_id] = 'CLEAR'
            bot.send_message(chat_id, text)
    elif state == 'appointment_service':
        print('APPOINTMENT SERVICE STATE')
        text, buttons = appointment(message, state)

        if buttons:
            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

        users_state[chat_id] = 'appointment_employee'
        bot.send_message(chat_id, text, reply_markup=keyboard)
    elif state == 'appointment_employee':
        print('APPOINTMENT EMPLOYEE STATE')
        text, buttons = appointment(message, state)

        users_state[chat_id] = 'appointment_date'
        bot.send_message(chat_id, text, reply_markup=telebot.types.ReplyKeyboardRemove())
    elif state == 'appointment_date':
        print('APPOINTMENT DATE STATE')
        text, buttons = appointment(message, state)
        if "неверную дату" in text:
            users_state[chat_id] = 'appointment_date'
            bot.send_message(chat_id, text, reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            users_state[chat_id] = 'appointment_time'
            bot.send_message(chat_id, text, reply_markup=telebot.types.ReplyKeyboardRemove())
    elif state == 'appointment_time':
        print('APPOINTMENT TIME STATE')
        text, buttons = appointment(message, state)
        if "неверное время" in text:
            users_state[chat_id] = 'appointment_time'
            bot.send_message(chat_id, text, reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            users_state[chat_id] = 'CLEAR'
            bot.send_message(chat_id, text, reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id, 'Ошибка, нажмите /start')


# Запуск бота
bot.polling()
