from telebot import types
import conf


def keyboard_dict_or_translate():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    dictionary = types.KeyboardButton(text="Словарь")
    translate = types.KeyboardButton(text="Переводчик")
    keyboard.add(dictionary, translate)
    return keyboard


def generated_letters():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for k, v in conf.LANGUAGES.items():
        keyboard.add(types.InlineKeyboardButton(text=v, callback_data=k))
    return keyboard


# def generated_alphabet():
#     keyboard = types.InlineKeyboardMarkup(row_width=3)
    # btn1 = types.InlineKeyboardButton(text='a', callback_data='a')
    # btn2 = types.InlineKeyboardButton(text='b', callback_data='b')
    # btn3 = types.InlineKeyboardButton(text='c', callback_data='c')
    # btn4 = types.InlineKeyboardButton(text='d', callback_data='d')
    # btn5 = types.InlineKeyboardButton(text='e', callback_data='e')
    # btn6 = types.InlineKeyboardButton(text='f', callback_data='f')
    # btn7 = types.InlineKeyboardButton(text='g', callback_data='g')
    # btn8 = types.InlineKeyboardButton(text='h', callback_data='h')
    # btn9 = types.InlineKeyboardButton(text='i', callback_data='i')
    # btn10 = types.InlineKeyboardButton(text='j', callback_data='j')
    # btn11 = types.InlineKeyboardButton(text='k', callback_data='k')
    # btn12 = types.InlineKeyboardButton(text='l', callback_data='l')
    # btn13 = types.InlineKeyboardButton(text='m', callback_data='m')
    # btn14 = types.InlineKeyboardButton(text='n', callback_data='n')
    # btn15 = types.InlineKeyboardButton(text='o', callback_data='o')
    # btn16 = types.InlineKeyboardButton(text='p', callback_data='p')
    # btn17 = types.InlineKeyboardButton(text='q', callback_data='q')
    # btn18 = types.InlineKeyboardButton(text='r', callback_data='r')
    # btn19 = types.InlineKeyboardButton(text='s', callback_data='s')
    # btn20 = types.InlineKeyboardButton(text='t', callback_data='t')
    # btn21 = types.InlineKeyboardButton(text='u', callback_data='u')
    # btn22 = types.InlineKeyboardButton(text='v', callback_data='v')
    # btn23 = types.InlineKeyboardButton(text='w', callback_data='w')
    # btn24 = types.InlineKeyboardButton(text='x', callback_data='x')
    # btn25 = types.InlineKeyboardButton(text='y', callback_data='y')
    # btn26 = types.InlineKeyboardButton(text='z', callback_data='z')
    # keyboard.row(btn1, btn2, btn3, btn4, btn5)
    # keyboard.row(btn6, btn7, btn8, btn9, btn10)
    # keyboard.row(btn11, btn12, btn13, btn14, btn15)
    # keyboard.row(btn16, btn17, btn18, btn19, btn20)
    # keyboard.row(btn21, btn22, btn23, btn24, btn25, btn26)
    # keyboard.row(types.InlineKeyboardButton(text="Все слова", callback_data="all_words"))
    # return keyboard


def keyboard_menu_or_save():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    menu = (types.InlineKeyboardButton(text="Главная", callback_data="menu"))
    save = (types.InlineKeyboardButton(text="Сохранить в словарь", callback_data="save"))
    keyboard.row(menu, save)
    return keyboard
