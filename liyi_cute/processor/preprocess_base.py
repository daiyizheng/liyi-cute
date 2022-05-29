#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/15 13:25
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : process.py

from __future__ import annotations

import abc
import logging
from typing import List, Text, Tuple, Optional

from liyi_cute.processor.tokenizers.sent_tokenizer import SentTokenize
from liyi_cute.shared.exceptions import NotImplementedException
from liyi_cute.shared.imports.schemas.schema import Example, Entity, Relation, Event

logger = logging.getLogger(__file__)


class PreProcessBase(abc.ABC):
    def __init__(self, tokenizer,
                 max_length: int=256,
                 special_tokens_count: int=2,
                 is_chinese: bool=False):
        self.is_chinese = is_chinese
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.special_tokens_count = special_tokens_count
        if not is_chinese:
            self.punctuation_special_char = {".", ";", "?"}
        else:
            self.punctuation_special_char = {"。", "！", "；", "？"}


    def is_ge_max_len(self,
                      text: Text
                      ) -> bool:
        """
        :param text:
        :return:
        """
        if len(self.tokenizer.tokenize(text)) > self.max_length - self.special_tokens_count:
            return True
        return False

    def cut_sentences(self,
                      text: Text,
                      entities: List[Entity]
                      )->List[Tuple[int, Text]]:
        ## 一阶截断
        cut_sents_list = [(0, text)]
        if self.is_ge_max_len(text):
            cut_sents_list = self.cut_sentences_v1((0, text))

        ## 二阶截断
        cut_two_sents_list = []
        for sent_tup in cut_sents_list:
            if self.is_ge_max_len(sent_tup[1]):
                cut_two_sents_list += self.cut_sentences_v2(sent_tup, entities)
            else:
                cut_two_sents_list.append(sent_tup)
        return cut_two_sents_list

    def cut_sentences_v1(self,
                         sent_tupe: Tuple[int, Text]
                         )->List[Tuple[int, Text]]:
        """
        tupe第一位是原文的开始位置，第二位是原文截断后的位置
        :param sent_tupe:
        :return:
        """
        init_start = sent_tupe[0]
        sent = sent_tupe[1]
        cut_sents_output = SentTokenize()(text=sent, is_chinese=self.is_chinese)
        cut_sents = cut_sents_output["sentences"]
        offset_mapping = cut_sents_output["offset_mapping"]

        assert "".join(cut_sents) == sent, "error cut text:%s" %sent
        new_sent_tupe = []

        for index in range(len(cut_sents)):
            new_sent_tupe.append(((offset_mapping[index][0]) + init_start, cut_sents[index]))
        return new_sent_tupe

    def cut_sentences_v2(self,
                         sent_tupe:Tuple[int, Text],
                         entities: List[Entity]
                         )->List[Tuple[int, Text]]:
        """

        :param sent_tupe:
        :param entities:
        :return:
        """
        init_start = sent_tupe[0]
        c_text = sent_tupe[1]
        mid = len(c_text) // 2
        entities = sorted(entities, key=lambda x: x.start)
        while True:
            flag = False
            for ent in entities:
                if ent.start <= mid <= ent.end:
                    flag = True
            if (not flag) or mid >= len(c_text):
                break
            mid += 1
        new_sent_tupes = [(init_start, c_text[:mid]), (init_start + mid, c_text[mid:])]
        return new_sent_tupes


    def correct_ner_position(self,
                             cut_tuple: Tuple[int, Text],
                             entities:List[Entity]
                             )->List[Entity]:
        """

        :param cut_tuple:
        :param entities:
        :return:
        """
        new_entities = []
        entities = sorted(entities, key=lambda x: (x.start, x.end))
        cut_text = cut_tuple[1]
        cut_start = cut_tuple[0]
        cut_end = cut_start + len(cut_text)

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

    def correct_rel_position(self,
                             cut_tuple: Tuple[int, Text],
                             relations: List[Relation]
                             ) -> List[Relation]:
        new_relations = []
        relations = sorted(relations, key=lambda x: (x.arg1.start, x.arg2.start))
        cut_text = cut_tuple[1]
        cut_start = cut_tuple[0]
        cut_end = cut_start + len(cut_text)
        for rel in relations:
            arg1 = rel.arg1
            arg2 = rel.arg2
            arg1_start = arg1.start
            arg1_end = arg1.end
            arg2_start = arg2.start
            arg2_end = arg2.end

            if cut_end<arg1_start or cut_end<arg2_start:
                continue

            if cut_start <=arg1_start<=cut_end and cut_start <=arg1_end<=cut_end and \
                    cut_start <=arg2_start<=cut_end and cut_start <=arg2_end<=cut_end:
                new_relations.append(Relation(id=rel.id,
                                              arg1=Entity(id=arg1.id,
                                                          start=arg1_start-cut_start,
                                                          end=arg1_end-cut_start,
                                                          mention=arg1.mention,
                                                          type=arg1.type),
                                              arg2=Entity(id=arg2.id,
                                                          start=arg2_start-cut_start,
                                                          end=arg2_end-cut_start,
                                                          mention=arg2.mention,
                                                          type=arg2.type),
                                              type=rel.type))
            return new_relations


    def correct_ent_position(self,
                             cut_tuple: Tuple[int, Text],
                             events: List[Relation]
                             ) -> List[Relation]:
        raise NotImplementedException

    def correct_tag_position_v1(self, text_id: Optional[int, Text],
                                all_cut_sents: List[Tuple[int, Text]],
                                entities:List[Entity]=[],
                                relations: List[Relation]=[],
                                events: List[Event]=[])->List[Example]:
        """

        :param text_id:
        :param all_cut_sents:
        :param annotaion:
        :return:
        """
        new_examples = []
        entities = sorted(entities, key=lambda x: (x.start, x.end))
        relations = sorted(relations, key=lambda x: (x.arg1.start, x.arg2.start))
        all_cut_sents = sorted(all_cut_sents, key=lambda x: x[0])

        for cut_tup in all_cut_sents:
            new_entities = self.correct_ner_position(cut_tup, entities)
            new_relations = self.correct_rel_position(cut_tup, relations)

            new_examples.append(Example(id=text_id, text=cut_tup[1], entities=new_entities, relations=new_relations))

        return new_examples

    def check_ner_postion_v1(self,
                             examples: List[Example]
                             ) -> List[Example]:
        """

        :param examples:
        :return:
        """
        for example in examples:
            cut_text = example.text
            for ent in example.entities:
                mention = ent.mention
                cut_start = ent.start
                cut_end = ent.end
                if cut_text[cut_start:cut_end] != mention:
                    logger.warning("entity is not aligned")
                    logger.warning("cut_text:%s" % cut_text)
                    logger.warning("cut_start:%s" % cut_start)
                    logger.warning("cut_end:%s" % cut_end)
                    logger.warning("mention:%s" % mention)
                    logger.warning("cut tag:%s" % cut_text[cut_start:cut_end])
                    example.entities.remove(ent)

        return examples

    def cut_text(self, example: Example)->List[Example]:
        """

        :param example:
        :return:
        """
        text_id = example.id
        text = example.text
        entities = example.entities

        ## 截断句子
        cut_sents_list = self.cut_sentences(text, entities)
        ## 截断后纠正标签的起始和结束的位置
        correct_cut_sents_list = self.correct_tag_position_v1(text_id, cut_sents_list, entities)
        ## 校验标签是否对齐
        new_examples = self.check_ner_postion_v1(correct_cut_sents_list)

        return new_examples








