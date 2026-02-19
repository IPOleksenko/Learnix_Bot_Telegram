from bot.keyboards.base.base import KeyboardBase
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List, Optional, TypeVar, Generic
from aiogram.utils.keyboard import ReplyKeyboardBuilder

class ReplyKeyboardBase(
    KeyboardBase[KeyboardButton, ReplyKeyboardBuilder, ReplyKeyboardMarkup]
):
    def _create_builder(self):
        return ReplyKeyboardBuilder()

    def _build_markup(self, builder):
        return builder.as_markup(resize_keyboard=self.resize_keyboard)

    def _add_navigation(self, page_info):
        row = []

        if page_info["has_prev"]:
            row.append(
                KeyboardButton(
                    text=f"{self.prev_button_text}"
                )
            )

        if self.show_page_numbers:
            row.append(
                KeyboardButton(
                    text=self.format_page_info()
                )
            )

        if page_info["has_next"]:
            row.append(
                KeyboardButton(
                    text=f"{self.next_button_text}"
                )
            )

        self.builder.row(*row)
