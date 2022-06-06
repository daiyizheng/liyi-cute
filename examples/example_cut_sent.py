#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/15 13:26
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : example_cut_sent.py

## 脚本使用
from liyi_cute.shared.loadings import parser

examples = parser(task_name="ner", dirname="../datasets/pmid/", error="ignore")