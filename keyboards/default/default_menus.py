from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню пользователя

check_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пользователь"),
            KeyboardButton(text="Администратор")
        ]
    ],
    resize_keyboard=True
)

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Личные задачи"),
            KeyboardButton(text="Групповые задачи"),
            KeyboardButton(text="Доска")
        ]
    ],
    resize_keyboard=True
)

# Главное меню админа
admin_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Личные задачи"),
            KeyboardButton(text="Доска"),
            KeyboardButton(text="Кадры")
        ]
    ],
    resize_keyboard=True
)
# Добавить и в главное
add_and_main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить"),
            KeyboardButton(text="↪ В главное меню")
        ]
    ],
    resize_keyboard=True
)


# В главное меню
go_main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)

# Добавить групповую задачу и в главное меню
group_and_main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить групповую задачу"),
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)
