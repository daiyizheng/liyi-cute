#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 9:11
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : TokenizerFast.py
from __future__ import annotations, print_function

from typing import Text, List, Dict, Union
import abc

import torch

from liyi_cute.utils.io import string_to_json


class TokenizeBaseFast(abc.ABC):
    def __init__(self, *args, **kwargs):
        self.do_lower_case = kwargs.get("do_lower_case", True)
        self.do_text_normalize = kwargs.get("do_text_normalize", True)
        self.unk_token = kwargs.get("unk_token", "[UNK]")
        self.pad_token = kwargs.get("pad_token", "[PAD]")
        self.word2id = kwargs.get("word2id", {})
        self.id2word = {self.word2id[k]: k for k in self.word2id}

    @staticmethod
    def tokenize(text: Text
                 ) -> List:
        raise NotImplementedError

    def vocab_size(self):
        return len(self.word2id)

    @property
    def get_unk_token(self) -> Text:
        return self.unk_token

    @property
    def get_unk_token_id(self) -> int:
        return self.word2id[self.unk_token]

    @property
    def get_pad_token(self) -> Text:
        return self.pad_token

    @property
    def get_word2id(self) -> Dict:
        return self.word2id

    @property
    def get_id2word(self) -> Dict:
        return self.id2word

    def convert_ids_to_tokens(self,
                              token_id
                              ) -> Text:
        return self.id2word.get(token_id, self.unk_token)


    def __call__(self,
                 text: Text,
                 *args,
                 **kwargs):
        raise NotImplementedError

    @classmethod
    def from_pretrained(cls,
                        word2id:Union[Dict, Text],
                        *args, **kwargs
                        ) -> TokenizeBaseFast:
        if isinstance(word2id, str):
            config = string_to_json(word2id)
            return cls(**config)

        return cls(word2id=word2id, *args, **kwargs)

    def save_pretrained(self,
                        output_dir: Text
                        ) -> None:
        raise NotImplementedError
