#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/26 14:22
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : json_parser.py
from __future__ import annotations, print_function

import json
import os
from collections import Iterable
from typing import Optional, Union, List, Text, Dict

from tqdm import tqdm

from liyi_cute.shared.imports.base_parser import BasePaeser
from liyi_cute.shared.imports.schemas.schema import Example
from liyi_cute.shared.imports.schemas.schemaItem import ExampleSchema
from liyi_cute.utils.common import iter_file_groups, check_key
from liyi_cute.utils.constants import NEED_KEYS
from liyi_cute.utils.io import read_file


class JsonParser(BasePaeser):
    exts = {".json"}
    support_task_name = {"ner", "rel"} #  "ner", "rel" "env", "attr"
    types = {"T", "R"} # types = {"T", "R", "*", "E", "N", "AM"}
    def __init__(self,task_name,
                 ignore_types: Optional[Iterable[str]] = None,
                 error: str = "raise",
                 lang="en") -> None:
        super(JsonParser, self).__init__(task_name, ignore_types, error, lang)


    async def parse(self,
              dirname: Union[str, bytes, os.PathLike],
              encoding: str = "utf-8") -> List[Example]:
        examples = []
        file_groups = iter_file_groups(dirname, self.exts, missing="error" if self.error == "raise" else "ignore")
        for key, (json_file, ) in tqdm(file_groups):
            examples += await self._parse_json(json_file, encoding)
        return examples

    async def _parse_json(self,
                    json_file:Text,
                    encoding:Text) -> List[Example]:
        data = json.loads(read_file(json_file, encoding))
        if isinstance(data, list):
            sample = data[0] if len(data) else []
        elif isinstance(data, Dict):
            sample = data
            data = [data]
        else:
            raise NotImplementedError

        check_key(sample, NEED_KEYS)
        examples = ExampleSchema().load(data, many=True)
        return examples
