from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic, Dict, Any

import uuid

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

T = TypeVar("T", InlineKeyboardButton, KeyboardButton)
B = TypeVar("B", InlineKeyboardBuilder, ReplyKeyboardBuilder)
M = TypeVar("M", InlineKeyboardMarkup, ReplyKeyboardMarkup)


class KeyboardBase(ABC, Generic[T, B, M]):
    def __init__(
        self,
        buttons: List[T],
        *,
        row_width: int = 3,
        page_size: int = 4,
        current_page: int = 0,
        keyboard_id: Optional[str] = None,
        resize_keyboard: bool = True,
        show_page_numbers: bool = False,
        prev_button_text: str = "◀️",
        next_button_text: str = "▶️",
        page_info_text: str = "{current}/{total}",
    ):
        self.buttons = buttons
        self.row_width = row_width
        self.page_size = page_size
        self.current_page = current_page
        self.resize_keyboard = resize_keyboard

        self.show_page_numbers = show_page_numbers
        self.prev_button_text = prev_button_text
        self.next_button_text = next_button_text
        self.page_info_text = page_info_text

        self.keyboard_id = keyboard_id or self._generate_keyboard_id()

        self.builder: Optional[B] = None
        self.keyboard: Optional[M] = None

        self._recalculate_pages()
        self.rebuild()

    # ------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------

    @property
    def total_pages(self) -> int:
        return self._total_pages

    @property
    def page(self) -> int:
        return self.current_page + 1

    # ------------------------------------------------------------------
    # CORE
    # ------------------------------------------------------------------

    def rebuild(self) -> None:
        """Full keyboard rebuild."""
        self.builder = self._create_builder()

        self._add_buttons(self._current_slice())

        if self.total_pages > 1:
            self._add_navigation(self._page_info())

        self.keyboard = self._build_markup(self.builder)

    def _recalculate_pages(self) -> None:
        self._total_pages = (
            (len(self.buttons) - 1) // self.page_size + 1 if self.buttons else 1
        )

    def _current_slice(self) -> List[T]:
        start = self.current_page * self.page_size
        end = start + self.page_size
        return self.buttons[start:end]

    def _add_buttons(self, buttons: List[T]) -> None:
        for i in range(0, len(buttons), self.row_width):
            self.builder.add(*buttons[i : i + self.row_width])

    # ------------------------------------------------------------------
    # PAGINATION
    # ------------------------------------------------------------------

    def next_page(self) -> bool:
        return self.go_to_page(self.current_page + 1)

    def previous_page(self) -> bool:
        return self.go_to_page(self.current_page - 1)

    def go_to_page(self, page: int) -> bool:
        if 0 <= page < self.total_pages:
            self.current_page = page
            self.rebuild()
            return True
        return False

    def _page_info(self) -> Dict[str, Any]:
        return {
            "current": self.page,
            "total": self.total_pages,
            "has_prev": self.current_page > 0,
            "has_next": self.current_page < self.total_pages - 1,
        }

    def format_page_info(self) -> str:
        return self.page_info_text.format(**self._page_info())

    # ------------------------------------------------------------------
    # CALLBACK UTILS
    # ------------------------------------------------------------------

    def create_callback_data(
        self,
        action: str,
        page: Optional[int] = None,
        data: Optional[str] = None,
    ) -> str:
        parts = [action, self.keyboard_id]
        if page is not None:
            parts.append(str(page))
        if data:
            parts.append(data)
        return ":".join(parts)

    def parse_callback(self, callback_data: str) -> Dict[str, Any]:
        action, kid, *rest = callback_data.split(":")
        return {
            "action": action,
            "keyboard_id": kid,
            "page": int(rest[0]) if rest and rest[0].isdigit() else None,
            "data": ":".join(rest[1:]) if len(rest) > 1 else None,
        }

    def is_my_callback(self, callback_data: str) -> bool:
        return f":{self.keyboard_id}" in callback_data

    # ------------------------------------------------------------------
    # UTILS
    # ------------------------------------------------------------------

    @staticmethod
    def _generate_keyboard_id() -> str:
        return uuid.uuid4().hex[:8]

    def get_keyboard(self) -> Optional[M]:
        return self.keyboard

    # ------------------------------------------------------------------
    # ABSTRACT
    # ------------------------------------------------------------------

    @abstractmethod
    def _create_builder(self) -> B:
        pass

    @abstractmethod
    def _build_markup(self, builder: B) -> M:
        pass

    @abstractmethod
    def _add_navigation(self, page_info: Dict[str, Any]) -> None:
        pass