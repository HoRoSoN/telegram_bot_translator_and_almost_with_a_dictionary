from telebot import TeleBot
from translate import Translator
import sqlite3

import conf
import keyboards

bot = TeleBot(conf.TOKEN)

user_dictionary = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Приветствие"""
    chat_id = message.chat.id
    first_name = message.from_user.first_name

    msg = bot.send_message(chat_id,
                           f'Привет {first_name} доброго дня, чем займёте себя?',
                           reply_markup=keyboards.keyboard_dict_or_translate())  # Словарь или переводчик)

    register_user(message)
    bot.register_next_step_handler(msg, dict_or_translate)


def register_user(message):
    """Регистрация и сохранение юзера в БД"""
    conn = sqlite3.connect(conf.path, check_same_thread=False)
    cursor = conn.cursor()
    try:
        first_name = message.from_user.first_name

        cursor.execute('''INSERT INTO tg_bot_profile(name, external_id)
        VALUES(?, ?)''', (first_name, message.chat.id))
    except:
        pass
    else:
        conn.commit()
    finally:
        conn.close()


@bot.message_handler(content_types=['text'])
def dict_or_translate(message):
    """Словарь или Переводчик"""
    if message.text == "Словарь":
        bot.send_message(message.chat.id, "Извини нету словаря еше не готово!!!")
        bot.send_message(message.chat.id, 'Повторишь выбор ????', reply_markup=keyboards.keyboard_dict_or_translate())
    if message.text == "Переводчик":
        chose_language(message)

#  Словарь который надо доделать
# @bot.callback_query_handler(func=lambda call: call.data in conf.alphabet_list)
# def dictionary(call):
# """Вывод сохраненных слов из БД"""
#     conn = sqlite3.connect(conf.path, check_same_thread=False)
#     cursor = conn.cursor()
#
#     if call.data:
#         print(call.data)
#
#         text_list = []
#
#         cursor.execute("""
#                 SELECT text_ru, text_en FROM tg_bot_message WHERE profile_id = (
#                 SELECT id FROM tg_bot_profile)""")
#         text_all = cursor.fetchall()
#
#         for data in text_all:
#             response = set(data)
#             for text in response:
#                 text_list.append(text)
#                 if text[0] == call.data:
#                     text_ru = text_list[1].lower()
#                     text_en = text_list[0].lower()
#                     print(text_en)
#
#                     msg_for_user = f"""Слово на букву: {call.data[0]}.
# {text_en}. Его перевод: {text_ru}."""
#
#                     bot.send_message(call.message.chat.id, msg_for_user)
#         conn.commit()
#         conn.close()
#     else:
#         bot.send_message(call.message.chat.id, "Словарь пока пустой")


# @bot.callback_query_handler(func=lambda call: call.data in ['all_word'])
# def all_word(call):
#     """Вывод сохраненных слов из БД"""
#     conn = sqlite3.connect(conf.path, check_same_thread=False)
#     cursor = conn.cursor()
#
#     if call.data:
#         print(call.data)
#
#         text_list = []
#
#         cursor.execute("""
#                 SELECT text_ru, text_en FROM tg_bot_message WHERE profile_id = (
#                 SELECT id FROM tg_bot_profile)""")
#         text_all = cursor.fetchall()
#
#         for data in text_all:
#             response = set(data)
#             for text in response:
#                 text_list.append(text)
#             text_ru = text_list[1].lower()
#             text_en = text_list[0].lower()
#             print(text_en)
#
#             msg_for_user = f"""Слово на букву: {call.data[0]}.
# {text_en}. Его перевод: {text_ru}."""
#
#             bot.send_message(call.message.chat.id, msg_for_user)
#         conn.commit()
#         conn.close()
#     else:
#         bot.send_message(call.message.chat.id, "Словарь пока пустой")

@bot.message_handler(content_types=['text'])
def chose_language(message):
    """Вывод кнопки: Выбор языка En or Ru"""
    if message.text == 'Переводчик':
        bot.send_message(message.chat.id, "Выберите язык: ", reply_markup=keyboards.generated_letters())


@bot.callback_query_handler(func=lambda call: call.data in ['en', 'ru'])
def language(call):
    """Выбор языка En or Ru"""
    chat_id = call.message.chat.id
    if call.data == 'en':
        msg = bot.send_message(chat_id, "Введите одно слово")
        bot.register_next_step_handler(msg, translation, to_lang='en', from_lang='ru')
    elif call.data == 'ru':
        msg = bot.send_message(chat_id, "Введите одно слово")
        bot.register_next_step_handler(msg, translation, to_lang='ru', from_lang='en')


def translation(message, to_lang, from_lang):
    """Переводит сообщение"""
    translator = Translator(to_lang, from_lang)
    translate = translator.translate(message.text)
    bot.send_message(message.chat.id, f'Сообщение:  {message.text} - Перевод:  {translate}',
                     reply_markup=keyboards.keyboard_menu_or_save())

    # создаю глобальный словарь{} и сохраняю в него сообщения
    if to_lang == 'en':
        user_dictionary['text_ru'] = [message.text]  # ru
        user_dictionary['text_en'] = [translate]  # en
        user_dictionary['chat_id'] = message.from_user.id
        user_dictionary['to_lang'] = 'en'
    if to_lang == 'ru':
        user_dictionary['text_en'] = [message.text]  # en
        user_dictionary['text_ru'] = [translate]  # ru
        user_dictionary['chat_id'] = message.from_user.id
        user_dictionary['to_lang'] = 'ru'


@bot.callback_query_handler(func=lambda call: call.data in ['menu', 'save'])
def menu_or_save(call):
    """Обратно к выбору переводчика или словаря и сохранение слова"""
    if "menu" in call.data:
        bot.send_message(call.message.chat.id, "Добро пожаловать в начало!",
                         reply_markup=keyboards.keyboard_dict_or_translate())
    elif "save" in call.data:
        bot.send_message(call.message.chat.id,
                         '''Сохранено!!!\nЕсли хотите перевести ещё одно слово нажмите "Главная"''')
        save(user_dictionary)


def save(data):
    conn = sqlite3.connect(conf.path, check_same_thread=False)
    cursor = conn.cursor()

    if user_dictionary['to_lang'] == 'en':
        messages = user_dictionary['text_ru']  # ru
        translate = user_dictionary['text_en']  # en
        chat_id = user_dictionary['chat_id']

        cursor.execute("""SELECT id
                FROM tg_bot_profile
                WHERE external_id = ?
            """, (chat_id,))
        profile_id = cursor.fetchone()[0]

        try:
            cursor.execute("""INSERT INTO tg_bot_message(text_ru, text_en, profile_id)
                    VALUES(?, ?, ?)
                """, (*messages, *translate, profile_id))
        except Exception as exp:
            print(f"{exp.__class__.__name__}: {exp}")
        else:
            conn.commit()
        finally:
            conn.close()

    if user_dictionary['to_lang'] == 'ru':
        messages = user_dictionary['text_en']  # en
        translate = user_dictionary['text_ru']  # ru
        chat_id = user_dictionary['chat_id']

        cursor.execute("""SELECT id
                FROM tg_bot_profile
                WHERE external_id = ?
            """, (chat_id,))
        profile_id = cursor.fetchone()[0]

        try:
            cursor.execute("""INSERT INTO tg_bot_message(text_en, text_ru, profile_id)
                    VALUES(?, ?, ?)
                """, (*messages, *translate, profile_id))
        except Exception as exp:
            print(f"{exp.__class__.__name__}: {exp}")
        else:
            conn.commit()
        finally:
            conn.close()


bot.polling(none_stop=True, interval=1)
