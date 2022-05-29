#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/29 17:07
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : data_output.py
from __future__ import annotations, print_function

from typing import List, Any, Text, Tuple, Optional, Union

from liyi_cute.shared.imports.schemas.schema import Entity, Example

from liyi_cute.processor.process import Process
from liyi_cute.utils.common import is_cut_number, check_key


class DataOutput(Process):

    @staticmethod
    def entities_merge(texts: List,
                       offset_mappings: List,
                       pred: List) -> Tuple[str, list, List[Tuple[Union[int, Any], Union[int, Any]]]]:

        text_len = [len(text) for text in texts]
        new_text = ""
        new_pred = []
        new_offset_mapping = []
        for index in range(len(texts)):
            assert len(offset_mappings[index]) == len(
                pred[index]), "offset_mapping length is not equal pred length, text is %s" % "".join(texts)
            new_text += texts[index]
            new_pred.extend(pred[index])
            if index == 0:
                new_offset_mapping.extend(offset_mappings[index])

            else:
                curr_offset_mapping = [(text_len[index - 1] + start, text_len[index - 1] + end) \
                                       for start, end in offset_mappings[index]]
                new_offset_mapping.extend(curr_offset_mapping)

        return new_text, new_pred, new_offset_mapping

    def realtions_output(self):
        pass

    def events_output(self):
        pass

    @staticmethod
    def entspan2entlist(text: Text,
                        span_entity: List[Entity, Text],
                        offset_mapping: List
                        ) -> List[Text]:

        raise NotImplementedError

        # labels = ["O"] * len(offset_mapping)
        # for l in span_entity:
        #     start_ids = l.start
        #     end_ids = l.end
        #     metion_type = l.type
        #     labels[start_ids] = "B-" + metion_type
        #     for idx in range(start_ids + 1, end_ids):
        #         labels[idx] = "I-" + metion_type
        # return labels

    @staticmethod
    def entlist2entspan(text: Optional[Text, List],
                        entities: List[Text],
                        offset_mapping: List
                        ) -> List[Entity]:
        labels_span = []
        # text格式的数据 conll数据格式
        index = 0
        idx = 0
        while index < len(entities):
            if entities[index].startswith("B-"):  # "B-xxx"
                start_ids = index
                ent_type = entities[index].split("-")[-1]
                while index + 1 < len(entities) and entities[index + 1].startswith("I-"):
                    index += 1
                end_ids = index
                labels_span.append(Entity(
                    id="T" + str(idx),
                    start=start_ids,
                    end=end_ids,
                    mention=text[offset_mapping[start_ids][0]:offset_mapping[end_ids][1]] \
                        if isinstance(text, str) else text[start_ids: end_ids],
                    type=ent_type
                ))
                index += 1
                idx += 1
            elif entities[index].startswith("O"):
                index += 1
            else:
                index += 1
                print("\033[1;35m Not beginning with B-, text: %s\033[0m" % (" ".join(text)))
                print("\033[1;35m Not beginning with B-, text: %s\033[0m" % (" ".join(entities)))

        return labels_span

    def __call__(self,
                 examples: List[Any],
                 pred: List[Any],
                 task_name: Text=None,
                 fformat: Text = "conll",
                 is_remove_special_symbols=True,
                 *args,
                 **kwargs) -> List[Example]:

        if not is_remove_special_symbols:
            raise NotImplementedError

        new_examples = []

        ids = ["-".join(ex.id.split("-")[:-1]) for ex in examples]
        keys, numbers = is_cut_number(ids)
        assert sum(numbers) == len(examples), "inconsistent length"

        task_name = examples[0].task_name if task_name==None else task_name
        texts = [ex.text for ex in examples]
        offset_mappings = [ex.offset_mapping for ex in examples]

        index = 0
        start = 0
        while index < len(numbers):
            end = start + numbers[index]
            new_entity = []
            new_relitions = []
            new_events = []
            check_key(curr_keys=set(ids[start: end]), need_keys={keys[index]})
            if task_name == "ner":
                new_text, new_pred, new_offset_mapping = self.entities_merge(texts=texts[start:end],
                                                                             offset_mappings=offset_mappings[start:end],
                                                                             pred=pred[start:end])
                new_entity = self.entlist2entspan(text=new_text,
                                                  entities=new_pred,
                                                  offset_mapping=new_offset_mapping)
            elif task_name == "rel":
                raise NotImplementedError

            elif task_name == "evt":
                raise NotImplementedError

            new_examples.append(Example(id=keys[index],
                                        task_name=task_name,
                                        text="".join(texts[start:end]),
                                        entities=new_entity,
                                        relations=new_relitions,
                                        events=new_events))
            index += 1
            start = end

        return new_examples
