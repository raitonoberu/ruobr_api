# -*- coding: utf-8 -*-
"""
:authors: raitonoberu
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 raitonoberu
"""
from typing import List, Union
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
    school_is_tourniquet: int
    readonly: bool
    school_is_food: int
    group: str
    gps_tracker: bool
    balance: int = None
    tourniquet: int = None
    mau_balance: int = None


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


class Reciver(SubscriptableBaseModel):
    role: int
    user_id: int
    user_img: str
    verbose_name: str


class Message(SubscriptableBaseModel):
    id: int
    type_id: int  # 1 - plain text, 2 - html
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
    recivers_list: List[Reciver] = None


class Comment(SubscriptableBaseModel):
    id: int
    author_id: int
    post_date: datetime
    update_date: datetime
    author_img: str
    author: str
    text: str


class MessageDetail(SubscriptableBaseModel):
    update_date: datetime
    author_img: str
    author: str
    text: str
    comments: List[Comment]
    count_recivers: int
    post_date: datetime
    role_str: str
    role: int
    recivers_list: List[Reciver]
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
    percent: str
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
    control_mark: Union[int, str]  # empty string if no value
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


class Direction(SubscriptableBaseModel):
    cnt: int
    direction_str: str
    indx: int
    percent: str
    percent_int: int


class Petition(SubscriptableBaseModel):
    certificate_monthly_payment: List  # TODO
    created: str
    fund: int
    fund_str: str
    module_id: int
    module_name: str
    msg: str
    parent_pay: List  # TODO
    parent_pay_status: int
    petition_pfdo_id: int
    program_id: int
    program_img: str
    program_name_full: str
    program_name_short: str
    program_school: str
    program_territory: str
    program_territory_img: str
    pt_pfdo_contract_date_end: str
    pt_pfdo_contract_start_day: str
    pt_pfdo_group_end: str
    pt_pfdo_group_start: str
    sdg_id: int
    sdg_name: str
    status: str
    status_str: int


class Certificate(SubscriptableBaseModel):
    id: int
    status_actul: int
    balance: str
    cert_group_name: str
    cert_group_id: int
    balance_start: str
    petition_bad: List[Petition]
    rmc_nominal: float
    cert_territory_img: str
    date_actual: datetime
    do_direction: List[Direction]
    number_cert: str
    cert_territory: str
    petition_good: List[Petition]


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
    vizit: List  # TODO
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


class Link(SubscriptableBaseModel):
    id: int
    about: str
    href: str
    img: str


class Category(SubscriptableBaseModel):
    id: int
    link_list: List[Link]
    categories: str


class UsefulLinks(SubscriptableBaseModel):
    categories_list: List[Category]
    link_without_category_list: List  # TODO
