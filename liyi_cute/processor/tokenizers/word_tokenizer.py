#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 9:11
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : word_tokenizer.py
from typing import Text, List

import spacy
from liyi_cute.utils.io import write_text_file, json_to_string

from liyi_cute.utils.text_normalize import string_q2b
from liyi_cute.processor.tokenizers.tokenizer_base import TokenizeBaseFast


class WordTokenizeFast(TokenizeBaseFast):
    def __init__(self, spacy_model, *args, **kwargs):
        super(WordTokenizeFast, self).__init__(*args, **kwargs)
        self.spacy_model = spacy_model
        self.nlp = spacy.load(spacy_model)

    def tokenize(self,
                 text: Text,
                 ) -> List:
        if self.do_lower_case:
            text = text.lower()
        if self.do_text_normalize:
            text = string_q2b(text)
        tokens = self.nlp(text)
        return [t.text for t in tokens]

    def __call__(self,
                 text: Text,
                 return_offset_mapping=False,
                 return_tensor:bool=False,
                 *args, **kwargs):

        if self.do_lower_case:
            text = text.lower()
        if self.do_text_normalize:
            text = string_q2b(text)

        tokens = self.nlp(text)
        input_ids = [self.word2id.get(t.text, self.get_unk_token_id) for t in tokens]
        if kwargs.get("padding", None):
            raise NotImplementedError

        if return_offset_mapping:
            offset_mapping = self.build_offset_mapping(text, tokens)
            return {"input_ids": input_ids, "offset_mapping": offset_mapping}

        return {"input_ids": input_ids}

    @staticmethod
    def build_offset_mapping(text, tokens):
        offset_mapping = []
        init_start = 0
        new_text = ""
        for token in tokens:
            index = 0
            while True:
                if (new_text + " " * index + token.text) in text:
                    new_text += " " * index + token.text
                    break
                if len(new_text + " " * index + token.text) > len(text):
                    raise ValueError
                index += 1
            assert text[init_start + index: len(new_text)] == token.text, \
                "offset_mapping is not aligned, token: %s, position:%d, %d" % (
                    token.text, init_start + index, len(new_text))
            offset_mapping.append((init_start, len(new_text)))
            init_start = len(new_text)

        return offset_mapping

    def save_pretrained(self,
                        output_dir: Text
                        ) -> None:
        outputs = {"unk_token":self.unk_token,
                   "pad_token":self.pad_token,
                   "spacy_model": self.spacy_model,
                   "word2id":self.word2id,
                   "do_lower_case":self.do_lower_case,
                   "do_text_normalize":self.do_text_normalize}
        write_text_file(content=json_to_string(outputs), file_path=output_dir)
