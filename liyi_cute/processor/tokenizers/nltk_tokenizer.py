#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/2 12:20
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : nltk_tokenizer.py

from __future__ import annotations
from typing import Text, List, Tuple, Dict

from nltk import wordpunct_tokenize, word_tokenize

from liyi_cute.utils.common import doubleQuotes


class WordTokenizerFast():
    def __init__(self, *args, **kwargs):
        self.do_lower_case = kwargs.pop("do_lower_case", True)
        self.word2id = kwargs.pop("word2id", {})
        self.id2word = { self.word2id[k]: k for k in self.word2id}
        self.unk_token = kwargs.pop("unk_token", "[UNK]")
        self.pad_token = kwargs.pop("pad_token", "[PAD]")

    def _check_unk(self):
        if self.unk_token not in self.word2id:
            raise ValueError("unk_token not in word2id")

    def tokenize(self, text:Text)->List:
        text = doubleQuotes(text)
        if self.do_lower_case:
            text = text.lower()
        return word_tokenize(text)

    def vocab_size(self):
        return len(self.word2id)

    def __call__(self, text:Text)->Dict:
        self._check_unk()
        if self.do_lower_case:
            text = text.lower()
        text = text.strip()
        text = doubleQuotes(text)
        word_list = word_tokenize(text)
        idx = 0
        offset_mapping = []
        start = 0
        while idx < len(word_list):
            while text[start] == " ":
                start += 1
            end = start + len(word_list[idx])
            assert text[start:end] == word_list[idx], "单词切分错误！:%s" %text
            offset_mapping.append((start, end))
            start = end
            idx += 1
        input_ids = [self.word2id.get(w, self.word2id[self.unk_token]) for w in word_list]
        return {"input_ids":input_ids, "offset_mapping":offset_mapping}

    def convert_ids_to_tokens(self, token_id)->Text:

        return self.id2word.get(token_id, self.unk_token)

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        return cls(*args, **kwargs)


class WordPunctTokenizerFast:

    def __init__(self, *args, **kwargs):
        self.do_lower_case = kwargs.pop("do_lower_case", True)
        self.word2id = kwargs.pop("word2id", {})
        self.unk_token = kwargs.pop("unk_token", "[UNK]")
        self.pad_token = kwargs.pop("pad_token", "[PAD]")


    def _check_unk(self):
        if self.unk_token not in self.word2id:
            raise ValueError("unk_token not in word2id")

    def tokenize(self, text:Text)->List:
        if self.do_lower_case:
            text = text.lower()
        return wordpunct_tokenize(text)

    def vocab_size(self):
        return len(self.word2id)

    def __call__(self, text:Text)-> Dict:
        self._check_unk()
        if self.do_lower_case:
            text = text.lower()
        text = text.strip()
        word_list = wordpunct_tokenize(text)
        idx = 0
        offset_mapping = []
        start = 0
        while idx < len(word_list):
            while text[start] == " ":
                start += 1
            end = start + len(word_list[idx])
            assert text[start:end] == word_list[idx], "单词切分错误！"
            offset_mapping.append((start, end))
            start = end
            idx += 1
        input_ids = [self.word2id.get(w, self.word2id[self.unk_token]) for w in word_list]
        return {"input_ids":input_ids, "offset_mapping":offset_mapping}

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        return cls(*args, **kwargs)