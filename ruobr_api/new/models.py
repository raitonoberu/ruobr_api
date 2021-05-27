# -*- coding: utf-8 -*-
"""
:authors: raitonoberu
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 raitonoberu
"""
from typing import List
from ruobr_api.models import SubscriptableBaseModel
from datetime import datetime, time, date


class User(SubscriptableBaseModel):
    id: int
    user_id: int
    status: str
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date
    user_img: str
    school: str
    school_terrirtory_id: int
    school_is_tourniquet: bool
    readonly: bool
    school_is_food: int
    group: str
    gps_tracker: bool


class LessonTask(SubscriptableBaseModel):
    id: int
    title: str
    doc: bool
    requires_solutions: bool
    deadline: date
    test_id: int = None
    type: str


class LessonMark(SubscriptableBaseModel):
    question_name: str
    question_id: int
    number: int
    question_type: str
    mark: int  # str?


class Lesson(SubscriptableBaseModel):
    id: int
    division_subject: int
    division_subject_str: str
    topic: str = None
    task: List[LessonTask] = None
    marks: List[LessonMark] = None
    time_start: time
    date: date
    subject: str
    time_end: time
    staff: str
    staff_id: int


class Message(SubscriptableBaseModel):
    id: int
    type_id: int
    update_date: datetime
    post_date: datetime
    author: str
    author_id: int
    author_img: str
    read: bool
    last_msg_text: str
    clean_text: str
    subject: str
    count_people: int
    recivers_list: List  # TODO


class MessageDetail(SubscriptableBaseModel):
    upload_date: datetime
    author_img: str
    author: str
    text: str
    comments: List  # TODO
    count_recivers: int
    post_date: datetime
    role_str: str
    role: int
    recivers_list: List  # TODO
    author_id: int
    subject: str


class Recipient(SubscriptableBaseModel):
    person_str: str
    staff_id: int
    user_id: int
    user_img: str


class CountedMark(SubscriptableBaseModel):
    cnt: int
    mark: float


class ControlMark(SubscriptableBaseModel):
    mark: float
    sub_type: int
    subject_id: int
    subject_name: str


class ControlmarksPeriod(SubscriptableBaseModel):
    counted_marks: List[CountedMark]
    date_end: date
    date_start: date
    marks: List[ControlMark]
    marks_future: int
    period: int
    rom: str
    title: str


class MarkStatistics(SubscriptableBaseModel):
    percent_int: int
    indx: int
    percent: float
    state_count_mark: int
    state_mark: str


class MarkCount(SubscriptableBaseModel):
    state_count_mark: int
    state_mark: int


class AllMarksItem(SubscriptableBaseModel):
    date: date
    mark_int: int
    status_lesson: str
    indx: int
    mark: str


class AllMarks(SubscriptableBaseModel):
    title: str
    need_five: int
    avg_mark: float
    control_mark: int
    need_four: int
    date_start: date
    period: int
    all_state_marks: List[MarkStatistics]
    count_mark: int
    sub_id: int
    marks: List[AllMarksItem]
    state_mark: List[MarkCount]
    not_in_lesson: int
    date_end: date
    subject: str


class Certificate(SubscriptableBaseModel):
    id: int
    status_actul: int
    balance: str
    cert_group_name: str
    cert_group_id: int
    balance_start: str
    petition_bad: List  # TODO
    rmc_nominal: float
    cert_territory_img: str
    date_actual: datetime
    do_direction: List  # TODO
    number_cert: str
    cert_territory: str
    petition_good: List  # TODO


class Birthday(SubscriptableBaseModel):
    first_name: str
    last_name: str
    middle_name: str
    avatar: str
    birth_date: date
    birthdate_year_future: int


class FoodInfo(SubscriptableBaseModel):
    account: str
    uid: str
    day_limit: str
    vizit: list  # TODO
    balance: str
    default_complex: str


class Classmate(SubscriptableBaseModel):
    first_name: str
    last_name: str
    middle_name: str
    avatar: str
    birth_date: date
    gender: int  # 1 - male, 2 - female


class Teacher(SubscriptableBaseModel):
    person_str: str
    user_id: int
    user_img: str


class Guide(SubscriptableBaseModel):
    id: int
    post_adress: str
    name: str
    tel_rec: str
    url: str
    teacher_list: List[Teacher]
    fullname: str
    territory: str
