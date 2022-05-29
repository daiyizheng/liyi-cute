#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/27 16:12
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : cut_sentence.py
from typing import Optional, List

from liyi_cute.processor.process import Process

from liyi_cute.shared.imports.schemas.schema import Example


class CutSentence(Process):
    def __call__(self,
                 examples: List[Example],
                 is_fine_cut: bool = False,
                 is_chinese:bool = False,
                 *args,
                 **kwargs) -> List[Example]:

        if isinstance(examples, Example):
            examples = [examples]
        from liyi_cute.processor.tokenizers.sent_tokenizer import SentTokenize
        sent_tokenizer = SentTokenize()
        new_examples = []

        for ex in examples:
            cut_sents_list = sent_tokenizer(text=ex.text,
                                            is_chinese=is_chinese,
                                            is_fine_cut=is_fine_cut,
                                            *args,
                                            **kwargs)

            sents = cut_sents_list["sentences"]
            offset_mapping = cut_sents_list["offset_mapping"]

            assert "".join(sents) == ex.text, "linconsistent length: %s" %ex.text

            new_examples += self.info_alignment(id=ex.id,
                                                task_name=ex.task_name,
                                                sentences=sents,
                                                offset_mapping=offset_mapping,
                                                entities=ex.entities,
                                                relations=ex.relations,
                                                events=ex.events)
        # 校验
        new_examples = [self.check_position(id=ex.id,
                                            task_name=ex.task_name,
                                            text=ex.text,
                                            entities=ex.entities,
                                            relations=ex.relations,
                                            events=ex.events
                                            )
                        for ex in new_examples]


        return new_examples



