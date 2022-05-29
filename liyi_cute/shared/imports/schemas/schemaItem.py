#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/26 14:00
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : schemaItem.py
from marshmallow import Schema, fields, post_load

from .schema import Entity, Relation, Event, Example


class EntitySchema(Schema):
    mention = fields.Str()
    type = fields.Str()
    start = fields.Int()
    end = fields.Int()
    id = fields.Str(default=None)

    @post_load
    def make_entity(self, data, **kwargs):
        return Entity(**data)


class RelationSchema(Schema):
    type = fields.Str()
    arg1 = fields.Nested(EntitySchema())
    arg2 = fields.Nested(EntitySchema())
    id = fields.Str(default=None)

    @post_load
    def make_relation(self, data, **kwargs):
        return Relation(**data)


class EventSchema(Schema):
    id = fields.Str(default=None)

    @post_load
    def make_event(self, data, **kwargs):
        return Event(**data)


class ExampleSchema(Schema):
    text = fields.Str()
    entities = fields.List(fields.Nested(EntitySchema()))
    relations = fields.List(fields.Nested(RelationSchema()))
    events = fields.List(fields.Nested(EventSchema()))
    id = fields.Str(default=None)
    task_name = fields.Str(default=None)

    @post_load
    def make_example(self, data, **kwargs):
        return Example(**data)


class NerExampleSchema(Schema):
    text = fields.List(fields.Str())
    entities = fields.List(fields.Str())
    id = fields.Str(default=None)
    task_name = fields.Str(default="ner")
