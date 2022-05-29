#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/27 0:58
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : statistics.py
from __future__ import annotations, print_function

from typing import Optional, List, Set, Dict
from collections import defaultdict

from liyi_cute.shared.imports.schemas.schema import Example


class Statistics(object):
    def __init__(self):
        pass

    @staticmethod
    def entity_type(examples: Optional[Example, List[Example]]
                    ) -> Set:
        if isinstance(examples, Example):
            examples = [examples]

        entity_type = set()
        for ex in examples:
            for ent in ex.entities:
                entity_type.add(ent.type)

        return entity_type

    @staticmethod
    def relation_type(examples: Optional[Example, List[Example]]
                      ) -> Set:
        if isinstance(examples, Example):
            examples = [examples]
        relation_type = set()
        for ex in examples:
            for rel in ex.relations:
                relation_type.add(rel.type)

        return relation_type

    @staticmethod
    def event_type(examples: Optional[Example, List[Example]]
                      ) -> Set:
        raise NotImplementedError

    @staticmethod
    def entity_type_count(examples: Optional[Example, List[Example]]
                          )->Dict:
        if isinstance(examples, Example):
            examples = [examples]
        type_count = defaultdict(int)
        for ex in examples:
            for ent in ex.entities:
                type_count[ent.type] += 1

        return type_count

    @staticmethod
    def relation_type_count(examples: Optional[Example, List[Example]]
                          ) -> Dict:
        if isinstance(examples, Example):
            examples = [examples]
        type_count = defaultdict(int)
        for ex in examples:
            for ent in ex.relations:
                type_count[ent.type] += 1

        return type_count

    @staticmethod
    def text_max_length(examples: Optional[Example, List[Example]])->int:
        if isinstance(examples, Example):
            examples = [examples]
        max_length = 0
        for ex in examples:
            max_length = len(ex.text) if len(ex.text) else max_length
        return max_length

    def __call__(self,
                 examples: Optional[Example, List[Example]],
                 *args,
                 **kwargs):
        return {"entity_type": self.entity_type(examples=examples),
                "relation_type":self.relation_type(examples=examples),
                "max_length":self.text_max_length(examples=examples)}
