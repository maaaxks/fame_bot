# bot/keyboards/inline.py - INLINE КНОПКИ 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_inline_keyboard() -> InlineKeyboardMarkup:
    """Inline-клавиатура для главного меню"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(
            text="📊 Анализ текста",
            callback_data="predict"
        ),
        InlineKeyboardButton(
            text="ℹ️ Помощь",
            callback_data="help"
        ),
        InlineKeyboardButton(
            text="🤖 О боте",
            callback_data="about"
        ),
        InlineKeyboardButton(
            text="📈 Статус",
            callback_data="stats"
        )
    )
    
    builder.adjust(2)  # 2 кнопки в ряду
    return builder.as_markup()

def get_analysis_keyboard() -> InlineKeyboardMarkup:
    """Inline-клавиатура после анализа"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(
            text="📊 Новый анализ",
            callback_data="predict"
        ),
        InlineKeyboardButton(
            text="🏠 В меню",
            callback_data="menu"
        )
    )
    
    builder.adjust(2)
    return builder.as_markup()