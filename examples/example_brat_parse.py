#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/29 18:40
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : example_brat_parse.py.py
import asyncio

from liyi_cute.shared.imports.bart_parser import BratParser
from liyi_cute.shared.loadings import parser


async def sigle_parse():
    # Initialize a parser.
    brat = BratParser(task_name="rel", error="ignore")
    examples = await brat.parse("../datasets/bio/")
    return examples


if __name__ == '__main__':

    ##
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(sigle_parse())
    pending = asyncio.Task.all_tasks()
    loop.run_until_complete(asyncio.gather(*pending))
    print(result)

    ## 脚本使用
    r = parser(task_name="rel", dirname="../datasets/bio/", error="ignore")
    print(r)


