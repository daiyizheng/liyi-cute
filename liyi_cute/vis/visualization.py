#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/26 22:52
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : visualization.py
from __future__ import annotations, print_function

from typing import Dict, Set

import spacy
from spacy import displacy

from liyi_cute.shared.exceptions import NotExistException
from liyi_cute.shared.imports.schemas.schema import Example
from liyi_cute.utils.constants import GRADIENTS


class Visualize(object):
    def __init__(self, lang="en_core_web_sm"):
        self.nlp = spacy.load(lang)

    def dep_visualization(self,
                          example: Example,
                          is_serve: bool = False,
                          options: bool = None,
                          jupyter: bool = False
                          ) -> None:
        doc = self.nlp(example.text)
        if not options:
            options = {"font": "Source Sans Pro", 'distance': 120}  # "compact": True, "bg": "#09a3d5","color": "white"
        if is_serve:
            displacy.serve(doc, style='dep', options=options)
        displacy.render(doc, style='dep', jupyter=jupyter, options=options)

    def ner_visualization(self,
                          example: Example,
                          is_serve: bool = False,
                          options: Dict = None,
                          jupyter: bool = False
                          ) -> None:

        ents = []
        for ent in example.entities:
            ents.append({"start": int(ent.start), "end": int(ent.end), "label": ent.type})
        doc = {"text": example.text, "ents": ents}
        """
        colors = {"DRUG": "linear-gradient(#FF2D2D, #ff7575, #FF9797)",
                  "GENE": "linear-gradient(#79FF79, #93FF93, #A6FFA6)",
                  "MUTATION": "linear-gradient(#FF9D6F, #FFAD86, #FFBD9D)"}
        options = {"colors": colors, "ents": ["DRUG", "GENE", "MUTATION"]}
        """
        if not options:
            options = self.spacy_options(doc)
        if is_serve:
            displacy.serve(doc, style='ent', manual=True, options=options)
        displacy.render(doc, style="ent", options=options, manual=True, jupyter=jupyter)

    def spacy_options(self, doc: Dict) -> Dict:
        """
        :param doc:
        :return:
        """
        labels = set()
        ents = doc.get("ents", [])
        for en in ents:
            if "label" not in en:
                raise NotExistException(f"key error: label")
            labels.add(en.get("label").upper())

        op_colors = {}
        for index, label in enumerate(labels):
            idx = index % len(labels)
            op_colors.update({label: GRADIENTS[idx]})

        return {"ents": list(labels), "colors": op_colors}

    def info_show(self,
                  exampele: Example,
                  keep_tag: Set = None
                  ) -> None:
        doc = self.nlp(exampele.text)
        print("{:<15} | {:<8} | {:<8} | {:<15} | {:<20}".format('Token', 'Tag', 'Relation', 'Head', 'Children'))
        print("-" * 70)

        for token in doc:
            # Print the token, dependency nature, head and all dependents of the token
            if keep_tag is None:
                print("{:<15} | {:<8} | {:<8} | {:<15} | {:<20}".format(str(token.text),
                                                                        str(token.tag_),
                                                                        str(token.dep_),
                                                                        str(token.head.text),
                                                                        str([child for child in token.children])))
            else:
                if token.tag_ in keep_tag:
                    print("{:<15} | {:<8} | {:<8} | {:<15} | {:<20}".format(str(token.text),
                                                                            str(token.tag_),
                                                                            str(token.dep_),
                                                                            str(token.head.text),
                                                                            str([child for child in token.children])))
