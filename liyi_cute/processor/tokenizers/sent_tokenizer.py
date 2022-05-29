#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/25 10:21
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : sent_tokenize.py
from __future__ import annotations

import re
from typing import Text, List, Dict, Tuple, Union, Any


class SentTokenize(object):
    def __init__(self):
        pass

    def zh_cut_sent(self,
                    para: Text
                    ) -> List[Text]:
        para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
        para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
        para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
        para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
        # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
        para = para.rstrip()  # 段尾如果有多余的\n就去掉它
        # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
        return para.split("\n")

    def en_cut_sent(self,
                    para: Text
                    ) -> List[Text]:
        para = re.sub(r'(\.\s|\!\s|\?\s|;\s)([^”’])', r"\1\n\2", para)
        para = re.sub('(\.{6}\s)([^”’])', r"\1\n\2", para)  # 英文省略号
        para = para.rstrip()  # 段尾如果有多余的\n就去掉它
        return para.split("\n")

    def tokenize(self,
                 text: Text,
                 is_chinese=False
                 ) -> List[Text]:
        if is_chinese:
            return self.zh_cut_sent(text)
        return self.en_cut_sent(text)

    def fine_cut(self,
                 sentence: Text,
                 offset_mapping: Tuple[int, int],
                 entities_position: List[Tuple[int, int]] = None
                 ) -> Tuple[List[str], List[Tuple[int, int]]]:
        init_start = offset_mapping[0]
        init_end = offset_mapping[1]
        mid = len(sentence) // 2

        if entities_position is None:
            sents = [sentence[:mid], sentence[mid:]]
            new_offset_mapping = [(init_start, init_start + mid), (init_start + mid, init_end)]
            return sents, new_offset_mapping

        entities = sorted(entities_position, key=lambda x: (x[0], x[1]))
        while True:
            flag = False
            for ent in entities:
                if ent[0] <= mid <= ent[1]:
                    flag = True
            if (not flag) or mid >= len(sentence):
                break
            mid += 1

        sents = [sentence[:mid], sentence[mid:]]
        new_offset_mapping = [(init_start, init_start + mid), (init_start + mid, init_end)]
        return sents, new_offset_mapping

    def __call__(self,
                 text: Text,
                 is_chinese: bool = False,
                 is_fine_cut: bool = False,
                 *args,
                 **kwargs,
                 ) -> Dict:
        sents = self.tokenize(text, is_chinese)
        offset_mapping = []
        index = 0
        for sent in sents:
            offset_mapping.append((index, index + len(sent)))
            index += len(sent)

        if is_fine_cut:
            max_length = kwargs.get("max_length", None)
            tokenizer = kwargs.get("tokenizer", None)
            special_tokens_count = kwargs.get("special_tokens_count", 0)
            if not max_length:
                raise KeyError("miss max_length parameter")

            sents_ = sents
            offset_mapping_ = offset_mapping
            sents = []
            offset_mapping = []
            for i in range(len(sents_)):
                if not self.is_ge_max_length(text, max_length, tokenizer, special_tokens_count):
                    sents += [sents_[i]]
                    offset_mapping += [offset_mapping_[i]]
                    continue

                new_sents, new_offset_mapping = self.fine_cut(sents_[i],
                                                              offset_mapping=offset_mapping_[i],
                                                              *args,
                                                              **kwargs)
                sents += new_sents
                offset_mapping += new_offset_mapping
        return {"sentences": sents, "offset_mapping": offset_mapping}

    def is_ge_max_length(self,
                         text: Text,
                         max_length: int,
                         tokenizer: Any = None,
                         special_tokens_count: int = 0
                         ) -> bool:
        if max_length and tokenizer:
            return max_length > len(tokenizer(text)) - special_tokens_count
        elif max_length:
            return max_length > len(text)
        else:
            raise KeyError("max_length parameter is missing")
