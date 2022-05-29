#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/29 14:27
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : data_convert.py
from __future__ import annotations, print_function

from copy import deepcopy
from typing import Optional, List, Dict, Any, Text, Tuple

from liyi_cute.shared.imports.schemas.schema import Example, Entity
from liyi_cute.processor.process import Process
from liyi_cute.stat.statistics import Statistics
from liyi_cute.utils.common import check_key


class DataConvert(Process):

    @staticmethod
    def convert_mrc(examples: Optional[List[Example], Example],
                    query_map: Dict
                    ) -> List[Any]:
        ner_type_set = Statistics.entity_type(examples)

        check_key(curr_keys=set(query_map.keys()), need_keys=ner_type_set)

        deepcopy_examples = deepcopy(examples)
        new_examples = []
        for example in deepcopy_examples:
            entites = example.entities

            for key in query_map.keys():
                new_entities = []
                for ent in entites:
                    if key == ent.type:
                        new_entities.append(Entity(id=ent.id,
                                                   start=ent.start,
                                                   end=ent.end,
                                                   mention=ent.mention,
                                                   type=ent.type))
                example.entities = new_entities
                query_content = query_map[key]
                setattr(example, "query", query_content)
                setattr(example, "ner_cate", key)
                new_examples.append(deepcopy(example))

        return new_examples

    @staticmethod
    def conll_subword_token(text: List[Text],
                            entities: List[Text],
                            tokenizer
                            ) -> Tuple[List[str], List[str], List[str], List[int]]:
        offset_mapping = []
        tokens = []
        labels = []
        # 转为 sub-token 级别 数据中有一些 输入 不是单词级别，比如日期，需要做转化
        for index, (word, slot_label) in enumerate(zip(text, entities)):
            words_ = tokenizer.tokenize(word)
            if not words_:
                text.remove(word)
                continue

            tokens.extend(words_)
            slot_label_nonstart = slot_label.replace("B-", "I-")
            labels.extend([slot_label] + [slot_label_nonstart] * (len(words_) - 1))
            offset_mapping.append(len(words_))

        return text, tokens, labels, offset_mapping

    @staticmethod
    def span_subword_token(text: Text,
                           entities: List[Entity],
                           tokenizer
                           ) -> Tuple[str, Any, Any, List[Tuple[int, int, str]]]:
        ent2token_spans = []
        inputs = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
        '''
        {'input_ids': [6224, 7481, 2218, 6206, 6432, 10114, 8701, 9719, 8457, 8758], 
        'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        'offset_mapping': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 8), (9, 14), (15, 18), (18, 21), (21, 24)]}
        '''
        token2char_span_mapping = inputs["offset_mapping"]  # 每个切分后的token在原始的text中的起始位置和结束位置
        text2token = tokenizer.tokenize(text, add_special_tokens=False)
        # ['见', '面', '就', '要', '说', 'say', 'hello', 'yes', '##ter', '##day']
        for ent_span in entities:
            ent = text[ent_span.start:ent_span.end]
            ent2token = tokenizer.tokenize(ent, add_special_tokens=False)

            # 然后将按字符个数标注的位置  修订 成 分完词 以token为个体的位置
            token_start_indexs = [i for i, v in enumerate(text2token) if v == ent2token[0]]
            token_end_indexs = [i for i, v in enumerate(text2token) if v == ent2token[-1]]

            # 分词后的位置 转为字符寻址 要和之前标的地址要一致 否则 就出错了
            token_start_index = list(
                filter(lambda x: token2char_span_mapping[x][0] == ent_span.start, token_start_indexs))
            token_end_index = list(filter(lambda x: token2char_span_mapping[x][-1] == ent_span.end, token_end_indexs))

            if len(token_start_index) == 0 or len(token_end_index) == 0:
                continue
                # 无法对应的token_span中
            token_span = (token_start_index[0], token_end_index[0], ent_span.type)
            ent2token_spans.append(token_span)
        return text, text2token, ent2token_spans, token2char_span_mapping

    @staticmethod
    def bio_to_bioes(tags: List
                     ) -> List:
        """
        把bio编码转换成bioes编码
        返回新的tags
        :param tags:
        :return:
        """
        new_tags = []
        for i, tag in enumerate(tags):
            if tag == 'O':
                # 直接保留，不变化
                new_tags.append(tag)
            elif tag.split('-')[0] == 'B':
                # 如果tag是以B开头，那么我们就要做下面的判断
                # 首先，如果当前tag不是最后一个，并且紧跟着的后一个是I
                if (i + 1) < len(tags) and tags[i + 1].split('-')[0] == 'I':
                    # 直接保留
                    new_tags.append(tag)
                else:
                    # 如果是最后一个或者紧跟着的后一个不是I，那么表示单子，需要把B换成S表示单字
                    new_tags.append(tag.replace('B-', 'S-'))
            elif tag.split('-')[0] == 'I':
                # 如果tag是以I开头，那么我们需要进行下面的判断
                # 首先，如果当前tag不是最后一个，并且紧跟着的一个是I
                if (i + 1) < len(tags) and tags[i + 1].split('-')[0] == 'I':
                    # 直接保留
                    new_tags.append(tag)
                else:
                    # 如果是最后一个，或者后一个不是I开头的，那么就表示一个词的结尾，就把I换成E表示一个词结尾
                    new_tags.append(tag.replace('I-', 'E-'))

            else:
                raise Exception('非法编码')
        return new_tags

    @staticmethod
    def bioes_to_bio(tags: List
                     ) -> List:
        """
        BIOES->BIO
        :param tags:
        :return:
        """
        new_tags = []
        for i, tag in enumerate(tags):
            if tag.split('-')[0] == "B":
                new_tags.append(tag)
            elif tag.split('-')[0] == "I":
                new_tags.append(tag)
            elif tag.split('-')[0] == "S":
                new_tags.append(tag.replace('S-', 'B-'))
            elif tag.split('-')[0] == "E":
                new_tags.append(tag.replace('E-', 'I-'))
            elif tag.split('-')[0] == "O":
                new_tags.append(tag)
            else:
                raise Exception('非法编码格式')
        return new_tags
