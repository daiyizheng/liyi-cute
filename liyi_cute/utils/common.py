#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/15 11:26
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : common.py

from __future__ import annotations

import asyncio
import copy
import glob
import itertools
import os
import logging

from collections.abc import Iterable
from typing import Union, Optional, Dict, Text, Any, List, Coroutine, TypeVar, Set

from liyi_cute.shared.exceptions import NotImplementedException

T = TypeVar("T")


def iter_file_groups(
        dirname: Union[str, bytes, os.PathLike],
        exts: Union[str, Iterable[str]],
        missing: str = "error",
) -> Iterable[tuple[str, list[str]]]:
    def _format_ext(ext):
        return f'.{ext.lstrip(".")}'

    def _iter_files(dirname):
        if os.path.isfile(dirname):
            dirpath = os.path.dirname(dirname)
            filename = os.path.splitext(os.path.basename(dirname))[0]
            filenames = []
            for suffix in exts:
                filenames.append(filename+suffix)
            for filename in filenames:
                yield os.path.join(dirpath, filename)
        else:
            for dirpath, _, filenames in os.walk(dirname):
                for filename in filenames:
                    if os.path.splitext(filename)[1] in exts:
                        yield os.path.join(dirpath, filename)

    if isinstance(dirname, bytes):
        dirname = dirname.decode()  # type: ignore

    missings = {"error", "ignore"}
    if missing not in missings:
        raise ValueError(f"Param `missing` should be in {missings}")

    if isinstance(exts, str):
        return glob.iglob(
            os.path.join(dirname, f"**/*{_format_ext(exts)}"), recursive=True
        )

    exts = {*map(_format_ext, exts)}
    num_exts = len(exts)
    files = _iter_files(dirname)

    if os.path.isfile(dirname):
        dirname = os.path.dirname(dirname)  ## 路劲，非文件

    for key, group in itertools.groupby(
            sorted(files), key=lambda x: os.path.splitext(os.path.relpath(x, dirname))[0]
    ):
        sorted_group = sorted(group, key=lambda x: os.path.splitext(x)[1])
        if len(sorted_group) != num_exts and missing == "error":
            raise RuntimeError(f"Missing files: {key!s}.{exts}")

        yield key, sorted_group


def check_key(js: Optional[Dict, List[Dict]],
              need_keys: Set
              ) -> None:
    if isinstance(js, dict):
        curr_keys = set(js.keys())
    elif isinstance(js, list):
        if len(js):
            curr_keys = set(js[0].keys())
        else:
            raise KeyError("json file keys is empty")
    else:
        raise NotImplementedException
    if curr_keys != need_keys:
        raise KeyError("json only need keys about : %s" % " ".join(need_keys))


def run_in_loop(
        f: Coroutine[Any, Any, T], loop: Optional[asyncio.AbstractEventLoop] = None
) -> T:
    """Execute the awaitable in the passed loop.

    If no loop is passed, the currently existing one is used or a new one is created
    if no loop has been started in the current context.

    After the awaitable is finished, all remaining tasks on the loop will be
    awaited as well (background tasks).

    WARNING: don't use this if there are never ending background tasks scheduled.
        in this case, this function will never return.

    Args:
       f: function to execute
       loop: loop to use for the execution

    Returns:
        return value from the function
    """

    if loop is None:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    result = loop.run_until_complete(f)

    # Let's also finish all running tasks:
    pending = asyncio.Task.all_tasks()
    loop.run_until_complete(asyncio.gather(*pending))

    return result


def doubleQuotes(text):
    """
    双引号改成单引号
    :param text:
    :return:
    """
    return text.replace('"', "'")
