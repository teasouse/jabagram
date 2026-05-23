#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2025 Vasiliy Stelmachenok <ventureo@yandex.ru>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
import logging
from jabagram.database.base import SqliteTable

class DefaultTopicStorage(SqliteTable):
    def __init__(self, path):
        self.__logger = logging.getLogger(__class__.__name__)
        super().__init__(path=path)

    def create(self):
        if self._execute(
            statement=(
                "CREATE TABLE IF NOT EXISTS default_topics"
                "(chat_id INTEGER PRIMARY KEY, thread_id INTEGER NOT NULL)"
            )
        ) is None:
            return False

        return True

    def set(self, chat_id: int, thread_id: int) -> None:
        self._execute(
            chat_id,
            thread_id,
            statement=(
                "INSERT OR REPLACE INTO default_topics(chat_id, thread_id)"
                " VALUES (?, ?)"
            ),
            on_error_message=(
                f"Failed to set default topic {thread_id} for chat {chat_id}"
            )
        )

    def get(self, chat_id: int) -> int | None:
        result = self._execute(
            chat_id,
            statement=(
                "SELECT thread_id FROM default_topics WHERE chat_id = ?"
            ),
            on_error_message=(
                f"Failed to get default topic for chat {chat_id}"
            )
        )

        if not result:
            return None

        for entry in result:
            return entry[0]

        return None

    def remove(self, chat_id: int) -> None:
        self._execute(
            chat_id,
            statement=(
                "DELETE FROM default_topics WHERE chat_id = ?"
            ),
            on_error_message=(
                f"Failed to remove default topic for chat {chat_id}"
            )
        )
