#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/15 11:46
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : loading.py
from __future__ import annotations

import asyncio
import logging
import os
from typing import Optional, Iterable, Text, Union, List, Any

import liyi_cute.utils.common
from liyi_cute.shared.exceptions import NotImplementedException
from liyi_cute.shared.imports.base_parser import BasePaeser

from liyi_cute.shared.imports.schemas.schema import Example
from liyi_cute.utils.io import list_files

logger = logging.getLogger(__file__)


def parser(
        task_name: Text,
        dirname: Union[str, bytes, os.PathLike],
        fformat: Text = "ann",
        ignore_types: Optional[Iterable[str]] = None,
        error: str = "raise",
        lang="en",
        encoding: str = "utf-8",
        loop: Optional[asyncio.AbstractEventLoop] = None, ) -> List[Example]:
    return liyi_cute.utils.common.run_in_loop(
        parser_async(
            task_name=task_name,
            dirname=dirname,
            fformat=fformat,
            ignore_types=ignore_types,
            error=error,
            lang=lang,
            encoding=encoding
        ),
        loop=loop,
    )


def _parser_factor(task_name: Text,
                   fformat: Text = "ann",
                   ignore_types: Optional[Iterable[str]] = None,
                   error: Text = "raise",
                   lang: Text = "en") -> Optional["BasePaeser"]:
    from liyi_cute.shared.imports import bart_parser, json_parser, conll_parser

    if fformat == "ann":
        parser_reader = bart_parser.BratParser(task_name=task_name,
                                               ignore_types=ignore_types,
                                               error=error,
                                               lang=lang)
    elif fformat == "json":
        parser_reader = json_parser.JsonParser(task_name=task_name,
                                               ignore_types=ignore_types,
                                               error=error,
                                               lang=lang)
    elif fformat == "conll":
        parser_reader = conll_parser.ConllParser(task_name=task_name,
                                                 ignore_types=ignore_types,
                                                 error=error,
                                                 lang=lang)
    else:
        raise NotImplementedException
    return parser_reader


async def parser_async(
        task_name: Text,
        dirname: Union[str, bytes, os.PathLike],
        fformat: Text = "ann",
        ignore_types: Optional[Iterable[str]] = None,
        error: str = "raise",
        lang: Text = "en",
        encoding: str = "utf-8") -> List[Example]:
    return await _parser_factor(task_name,
                                fformat,
                                ignore_types,
                                error,
                                lang).parse(dirname, encoding)


def load_data(resource_name: Text,
              task_name: Text = None
              ) -> List[Any]:
    if not os.path.exists(resource_name):
        raise ValueError(f"File '{resource_name}' does not exist.")

    if os.path.isfile(resource_name):
        files = [resource_name]
    else:
        files = list_files(resource_name)

    examples = []
    for f in files:
        examples += _load(f, task_name)

    return [example for example in examples if example]


def _load(filename: Text,
          task_name: Text = None
          ) -> List[Any]:
    """Loads a single training data file from disk."""

    reader = _reader_factory(filename)

    if reader:
        return reader.read(filename, task_name=task_name)
    else:
        raise None


def _reader_factory(filename: Text) -> Optional["DataReader"]:
    """Generates the appropriate reader class based on the file format."""
    if not os.path.isfile(filename):
        raise ValueError(f"Unknown data format for file '{filename}'.")
    from liyi_cute.shared.formats.readerwriter import (JsonDataReader,
                                                       BratDataReader)
    fformat = filename.split(".")[-1].lower()

    if fformat == "json":
        reader = JsonDataReader()
    elif fformat == "ann":
        reader = BratDataReader()
    else:
        raise NotImplementedException

    return reader
