#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/29 15:32
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : conll_parser.py
from __future__ import annotations, print_function

import os
from typing import Text, Optional, Iterable, Union, List

from liyi_cute.utils.io import read_file
from tqdm import tqdm

from liyi_cute.utils.common import iter_file_groups

from liyi_cute.shared.imports.base_parser import BasePaeser
from liyi_cute.shared.imports.schemas.schema import NerExample


class ConllParser(BasePaeser):
    exts = {".txt"}
    support_task_name = {"ner"}  # "ner", "rel" "env", "attr"
    types = {"T"}  # types = {"T", "R", "*", "E", "N", "AM"}

    def __init__(self, task_name: Text,
                 ignore_types: Optional[Iterable[str]] = None,
                 error: Text = "raise",
                 lang: Text = "en") -> None:
        super(ConllParser, self).__init__(task_name=task_name,
                                          ignore_types=ignore_types,
                                          error=error,
                                          lang=lang)

    async def _parse_text(self,
                          txt_file: Text,
                          encoding: Text
                          ) -> List[NerExample]:
        lines = read_file(txt_file, encoding)
        line = lines.strip()
        examples = []
        if line:
            lines_list = lines.split("\n\n")
            for index, line_s in enumerate(lines_list):
                line_list = line_s.split("\n")
                data = []
                tag = []
                for line in line_list:
                    if not line.strip():
                        continue
                    data.append(line.split("\t")[0])
                    tag.append(line.split("\t")[1])
                if data:
                    examples.append(NerExample(
                        id=str(index),
                        text=data,
                        entities=tag
                    ))
        return examples

    async def parse(self,
                    dirname: Union[str, bytes, os.PathLike],
                    encoding: str = "utf-8"
                    ) -> List[NerExample]:
        examples = []
        file_groups = iter_file_groups(dirname, self.exts, missing="error" if self.error == "raise" else "ignore")
        for key, (txt_file,) in tqdm(file_groups):
            examples += await self._parse_text(txt_file, encoding)
        return examples
