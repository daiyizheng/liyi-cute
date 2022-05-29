#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/26 10:53
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : convert.py
from __future__ import annotations, print_function

import os
from typing import Text, Tuple, List

from liyi_cute.shared.exceptions import NotImplementedException
from liyi_cute.shared.formats.readerwriter import JsonDataWriter, BratDataWriter
from liyi_cute.shared.loadings import load_data
from liyi_cute.utils.io import write_text_file, write_text_ann


def convert_data(data_file: Text,
                 out_file: Text,
                 output_format: Text,
                 task_name:Text=None
                 )->None:
    if not os.path.exists(data_file):
        print(
            "Data file '{}' does not exist. Provide a valid NLU data file using "
            "the '--data' argument.".format(data_file)
        )
        return

    if output_format == "json":
        td = load_data(data_file, task_name)
        output = JsonDataWriter().dumps(td)
        write_text_file(output, out_file)

    elif output_format == "ann":
        td = load_data(data_file)
        outputs = BratDataWriter().dumps(td)
        write_text_ann(outputs, out_file)

    else:
        raise NotImplementedException