from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сократить ссылку")],
        [KeyboardButton(text="Статистика")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие"
)

def link_inline_keyboard(link_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Статистика", callback_data=f"stats:{link_id}")],
            [InlineKeyboardButton(text="✏️ Переименовать", callback_data=f"rename:{link_id}")],
            [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete:{link_id}")]
        ]
    )
