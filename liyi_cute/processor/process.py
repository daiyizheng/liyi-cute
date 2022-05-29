#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/27 16:18
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : preprocess.py
from __future__ import annotations, print_function

import abc
from typing import List, Tuple, Text

from liyi_cute.shared.imports.schemas.schema import Entity, Example, Relation, Event


class Process(abc.ABC):
    @staticmethod
    def entity_alignment(entities: List[Entity],
                         offset_mapping: Tuple[int, int]
                         ) -> List[Entity]:

        entities = sorted(entities, key=lambda x: (x.start, x.end))
        cut_start = offset_mapping[0]
        cut_end = offset_mapping[1]

        new_entities = []
        for an in entities:
            e_start = an.start
            e_end = an.end

            if cut_end < e_start:
                continue
            # [) 开区间，最后一位是取不到的，所以*_end是有=的
            if cut_start <= e_start <= cut_end and cut_start <= e_end <= cut_end:
                new_entities.append(Entity(id=an.id,
                                           start=e_start - cut_start,
                                           end=e_end - cut_start,
                                           mention=an.mention,
                                           type=an.type))
        return new_entities

    @staticmethod
    def realtion_alignment(relations: List[Relation],
                           offset_mapping: Tuple[int, int]
                           ) -> List[Relation]:
        raise NotImplementedError

    @staticmethod
    def event_alignment(relations: List[Event],
                        offset_mapping: Tuple[int, int]
                        ) -> List[Event]:
        raise NotImplementedError

    @staticmethod
    def check_ner_postion(text:Text,
                          entities: List[Entity]
                          ) -> List[Entity]:
        new_entities = []
        for ent in entities:
            mention = ent.mention
            cut_start = ent.start
            cut_end = ent.end
            if text[cut_start:cut_end] != mention:
                print("\033[1;35m entity is not aligned \033[0m")
                print("\033[1;35m cut_text:%s  \033[0m" % text)
                print("\033[1;35m cut_start:%s  \033[0m" % cut_start)
                print("\033[1;35m cut_end:%s  \033[0m" % cut_end)
                print("\033[1;35m mention:%s  \033[0m" % mention)
                print("\033[1;35m cut tag:%s  \033[0m" % text[cut_start:cut_end])
                continue

            new_entities.append(Entity(
                id = ent.id,
                start= ent.start,
                end= ent.end,
                mention= ent.mention,
                type=ent.type
            ))

        return new_entities

    @staticmethod
    def check_rel_position(text:Text,
                           relations: List[Relation]):
        raise NotImplementedError

    @staticmethod
    def check_evt_position(text:Text,
                           events:List[Event]):
        raise NotImplementedError

    def check_position(self, id:Text,
                       task_name:Text,
                       text:Text,
                       entities:List[Entity] = [],
                       relations:List[Relation] = [],
                       events:List[Event] = []
                       )->Example:
        new_entities, new_relations, new_events = [], [], []
        if len(entities):
            new_entities = self.check_ner_postion(text, entities)

        if len(relations):
            new_relations = self.check_rel_position(text, relations)

        if len(events):
            new_events = self.check_evt_position(text, events)

        return Example(id=id,
                       text=text,
                       task_name=task_name,
                       entities=new_entities,
                       relations=new_relations,
                       events=new_events)







    def info_alignment(self, id: Text,
                       task_name: Text,
                       sentences: List[Text],
                       offset_mapping: List[Tuple[int, int]],
                       entities: List[Entity] = [],
                       relations: List[Relation] = [],
                       events: List[Event] = []
                       ):
        new_examples = []

        for index in range(len(sentences)):
            new_entities = []
            new_relations = []
            new_events = []
            if len(entities):
                new_entities = self.entity_alignment(entities, offset_mapping[index])

            if len(relations):
                new_relations = self.realtion_alignment(relations, offset_mapping[index])

            if len(events):
                new_events = self.event_alignment(events, offset_mapping[index])

            new_examples.append(Example(id=id + "-" + str(index),
                                        text=sentences[index],
                                        task_name=task_name,
                                        entities=new_entities,
                                        relations=new_relations,
                                        events=new_events))
        return new_examples
