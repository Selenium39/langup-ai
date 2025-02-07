#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import functools
import json
import sys
import threading
import time
from pprint import pprint
from typing import Optional, Any

from pydantic import BaseModel


def singleton(cls):
    _instance = {}

    @functools.wraps(cls)
    def inner(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return inner


class DFA:
    def __init__(self, keyword_list: list):
        self.kw_list = keyword_list
        self.state_event_dict = self._generate_state_event_dict(keyword_list)

    def match(self, content: str):
        match_list = []
        state_list = []
        temp_match_list = []

        for char_pos, char in enumerate(content):
            if char in self.state_event_dict:
                state_list.append(self.state_event_dict)
                temp_match_list.append({
                    "start": char_pos,
                    "match": ""
                })

            for index, state in enumerate(state_list):
                is_find = False
                state_char = None

                # 如果是 * 则匹配所有内容
                if "*" in state:
                    state_list[index] = state["*"]
                    state_char = state["*"]
                    is_find = True

                if char in state:
                    state_list[index] = state[char]
                    state_char = state[char]
                    is_find = True

                if is_find:
                    temp_match_list[index]["match"] += char

                    if state_char["is_end"]:
                        match_list.append(copy.deepcopy(temp_match_list[index]))

                        if len(state_char.keys()) == 1:
                            state_list.pop(index)
                            temp_match_list.pop(index)
                else:
                    state_list.pop(index)
                    temp_match_list.pop(index)

        return match_list

    @staticmethod
    def _generate_state_event_dict(keyword_list: list) -> dict:
        state_event_dict = {}

        for keyword in keyword_list:
            if not keyword:
                continue
            current_dict = state_event_dict
            length = len(keyword)

            for index, char in enumerate(keyword):
                if char not in current_dict:
                    next_dict = {"is_end": False}
                    current_dict[char] = next_dict
                else:
                    next_dict = current_dict[char]
                current_dict = next_dict
                if index == length - 1:
                    current_dict["is_end"] = True

        return state_event_dict


class Record(BaseModel):
    """存档、日志"""
    listener_kwargs: Optional[Any] = None
    react_kwargs: Optional[dict] = None
    time_cost: Optional[str] = None
    created_time: Optional[str] = None