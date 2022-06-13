#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 13:19
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : Encoding.py
from __future__ import annotations, print_function

from collections import UserDict
from typing import List, Text

import torch


class Encoding(UserDict):
    pass

    @staticmethod
    def convert_to_tensors(data: List,
                           dtype: Text = "long"
                           ) -> torch.Tensor:
        return torch.tensor(data, dtype=torch.long if dtype == "long" else torch.float)
