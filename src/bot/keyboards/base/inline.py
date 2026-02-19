from typing import List, Optional, Dict, Any
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards.base.base import KeyboardBase
from aiogram.utils.keyboard import InlineKeyboardBuilder

class InlineKeyboardBase(
    KeyboardBase[InlineKeyboardButton, InlineKeyboardBuilder, InlineKeyboardMarkup]
):
    def _create_builder(self):
        return InlineKeyboardBuilder()

    def _build_markup(self, builder):
        return builder.as_markup()

    def _add_navigation(self, page_info):
        row = []

        if page_info["has_prev"]:
            row.append(
                InlineKeyboardButton(
                    text=self.prev_button_text,
                    callback_data=self.create_callback_data(
                        "page", self.current_page - 1
                    ),
                )
            )

        if self.show_page_numbers:
            row.append(
                InlineKeyboardButton(
                    text=self.format_page_info(),
                    callback_data="noop",
                )
            )

        if page_info["has_next"]:
            row.append(
                InlineKeyboardButton(
                    text=self.next_button_text,
                    callback_data=self.create_callback_data(
                        "page", self.current_page + 1
                    ),
                )
            )

        self.builder.row(*row)
