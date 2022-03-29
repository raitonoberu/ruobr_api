# -*- coding: utf-8 -*-
"""
:authors: raitonoberu
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 raitonoberu
"""
from typing import Dict, List, Union
from pydantic import BaseModel
from datetime import datetime, time, date


class SubscriptableBaseModel(BaseModel):
    # в целях совместимости с прошлыми версиями
    def __getitem__(self, item):
        return getattr(self, item)


class User(SubscriptableBaseModel):
    id: int
    status: str
    first_name: str
    last_name: str
    middle_name: str
    school: str
    school_is_tourniquet: bool
    readonly: bool
    school_is_food: bool
    group: str
    gps_tracker: bool


class Message(SubscriptableBaseModel):
    id: int
    post_date: Union[datetime, date]
    author: str
    read: bool
    text: str
    clean_text: str
    subject: str


class ControlmarksPeriod(SubscriptableBaseModel):
    marks: Dict[str, str]
    rom: str
    period: int
    title: str


class Task(SubscriptableBaseModel):
    id: int
    title: str
    doc: bool
    requires_solutions: bool
    deadline: date
    test_id: int = None
    type: str


class Lesson(SubscriptableBaseModel):
    id: int
    topic: str = None
    task: Task = None
    time_start: time
    date: date
    subject: str
    time_end: time
    staff: str


class ProgressSubject(SubscriptableBaseModel):
    subject: str
    place_count: int
    place: int
    group_avg: float
    child_avg: float
    parallels_avg: float


class Progress(SubscriptableBaseModel):
    period_name: str
    place_count: str
    subjects: List[ProgressSubject]
    place: int
    group_avg: float
    child_avg: float
    parallels_avg: float


class Mark(SubscriptableBaseModel):
    question_name: str
    question_id: int
    number: int
    question_type: str
    mark: int


class FoodInfo(SubscriptableBaseModel):
    subsidy: int
    account: int
    total_take_off: int
    total_add: int
    balance_on_start_year: int
    balance: int
    default_complex: str


class FoodHistoryDay(SubscriptableBaseModel):
    id: int
    date: date
    state: int
    complex__code: str
    complex__uid: str
    state_str: str
    complex__name: str


class NewsItem(SubscriptableBaseModel):
    id: int
    title: str
    clean_text: str
    author: str
    school_name: str
    school_id: int
    text: str
    date: date
    pub_date: Union[datetime, date]
