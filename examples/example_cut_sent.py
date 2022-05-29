#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/15 13:26
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : example_cut_sent.py

## 脚本使用
import logging
from typing import List, Text

from liyi_cute.processor.preprocess_base import PreProcessBase
from liyi_cute.shared.imports.schemas.schema import Entity, Example

from liyi_cute.shared.loading import parser
from transformers import BertConfig, BertTokenizerFast
logger = logging.getLogger(__file__)

examples = parser(task_name="ner", dirname="../datasets/pmid/", error="ignore")

lang = "en"
max_length = 256
special_tokens_count = 2
punctuation_special_char={".", ";"}
tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased", return_offsets_mapping=True,
                                                do_lower_case=True,
                                                cache_dir=None)
obj = PreProcessBase(tokenizer=tokenizer, max_length=max_length, special_tokens_count=2, lang="en")
a = obj.cut_text(example=examples[0])
print(a)

# setattr(examples[0], "offset_mapping", [1,2,3])
# print(examples[0])