#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/27 13:08
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : base_parser.py
from __future__ import annotations

from typing import Optional, Text, Union, Dict, List, Any
from collections import Iterable
import re, os, logging
from copy import deepcopy

from liyi_cute.shared.exceptions import NotImplementedException, NotExistException, FileNotFoundException

logger = logging.getLogger(__file__)

class BasePaeser(object):
    exts = {".ann", ".txt", ".json"}
    support_task_name = {"ner", "rel" "env", "attr"}
    types = {"T", "R", "*", "E", "N", "AM"}
    supported_language_list = ["en", "zh"]
    errors = {"raise", "ignore"}
    def __init__(self,
                 task_name,
                 ignore_types: Optional[Iterable[str]] = None,
                 error: str = "raise",
                 lang="en"):
        self.examples:List = []
        ##任务类型
        if task_name not in self.support_task_name:
            raise NotImplementedException("The task interface is not implemented")
        self.task_name = task_name

        ## 判断忽略的类型
        self.re_ignore_types: Optional[re.Pattern] = None
        if ignore_types:
            unknown_types = set(ignore_types) - self.types
            if unknown_types:
                raise NotExistException(f"Unknown types: {unknown_types!r}")
            ## 忽略类型正则
            self.re_ignore_types = re.compile(r"|".join(re.escape(x) for x in ignore_types))

        ##
        if error not in self.errors:
            raise NotExistException(f"`error` should be in {self.errors!r}")
        self.error = error

        ## 支持语言
        if lang not in self.supported_language_list:
            raise NotExistException(f"{lang} is not support")
        self.lang = lang

        self.examples = []

    def _should_ignore_line(self, line:Text):
        if self.re_ignore_types:
            return re.match(self.re_ignore_types, line)

        return False

    def _raise(self, error)->None:
        if self.error == "raise":
            raise error

    def _raise_invalid_line_error(self, line:Text)->None:
        self._raise(NotExistException(f"Invalid line: {line}"))


    async def parse(self,  dirname: Union[str, bytes, os.PathLike],
              encoding: str = "utf-8"):
        raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        task_name = kwargs.pop("task_name", None)
        ignore_types = kwargs.pop("ignore_types", None)
        error = kwargs.pop("error", "raise")

        return cls(task_name=task_name,
                   ignore_types=ignore_types,
                   error=error)







