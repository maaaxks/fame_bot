# bot/keyboards/main_menu.py - REPLY КЛАВИАТУРА (под полем ввода)
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="📊 Проанализировать текст")],
        [KeyboardButton(text="ℹ️ Помощь"), KeyboardButton(text="🤖 О боте")],
        [KeyboardButton(text="📈 Статус модели")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,  #Подстраивается под экран
        one_time_keyboard=False,  #Не скрывается после нажатия
        input_field_placeholder="Выберите действие или отправьте текст..."
    )

def predict_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для анализа текста"""
    buttons = [
        [KeyboardButton(text="🔙 Назад в меню")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Отправьте текст для анализа..."
    )