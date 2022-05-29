#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/15 11:12
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : schema.py

from __future__ import annotations

from typing import Optional, Union, List
from collections.abc import Iterable
import dataclasses


@dataclasses.dataclass
class Entity(object):
    mention: str
    type: str
    start: int
    end: int
    id: Optional[str] = None


@dataclasses.dataclass
class Relation(object):
    type: str
    arg1: Entity
    arg2: Entity
    id: Optional[str] = None


@dataclasses.dataclass
class Event(object):
    id: Optional[str] = None


@dataclasses.dataclass
class Example(object):
    text: Union[str, Iterable[str]]
    entities: list[Entity] = dataclasses.field(default_factory=list)
    relations: list[Relation] = dataclasses.field(default_factory=list)
    events: list[Event] = dataclasses.field(default_factory=list)
    id: Optional[str, int] = None
    task_name: Optional[str] = None


## 只是针对conll格式的数据
@dataclasses.dataclass
class NerExample(object):
    text: List[str, Iterable[str]]
    entities: List[str, Iterable[str]] = dataclasses.field(default_factory=list)
    id: Optional[str, int] = None
    task_name: Optional[str] = "ner"
