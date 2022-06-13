#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/12 21:52
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : __main__.py
from __future__ import annotations, print_function

from datetime import datetime
from colorama import Fore, Back, Style
import argparse


from liyi_cute import __version__

dt = datetime.now()

__VERSION__ = f'👍    {__version__}'
__AUTHOR__ = '😀    Yizheng Dai'
__CONTACT__ = '😍    qq: 387942239'
__DATE__ = f"👉    {dt.strftime('%Y.%m.%d')}, since 2022.04.06"
__LOC__ = '👉    Hangzhou, China'
__git__ = '👍    https://github.com/daiyizheng/liyi-cute'


def arg_parse():
    """
    parse arguments
    :return:
    """
    parser = argparse.ArgumentParser(prog="liyi-cute")
    parser.add_argument('--version', '-v',
                        action="store_true", help='show version info.')

    return parser.parse_args()


def print_welcome_msg():
    print('-'*70)
    print(Fore.BLUE + Style.BRIGHT + '              Alfred ' + Style.RESET_ALL +
          Fore.WHITE + '- Valet of Artificial Intelligence.' + Style.RESET_ALL)
    print('         Author : ' + Fore.CYAN +
          Style.BRIGHT + __AUTHOR__ + Style.RESET_ALL)
    print('         Contact: ' + Fore.BLUE +
          Style.BRIGHT + __CONTACT__ + Style.RESET_ALL)
    print('         At     : ' + Fore.LIGHTGREEN_EX +
          Style.BRIGHT + __DATE__ + Style.RESET_ALL)
    print('         Loc    : ' + Fore.LIGHTMAGENTA_EX +
          Style.BRIGHT + __LOC__ + Style.RESET_ALL)
    print('         Star   : ' + Fore.MAGENTA +
          Style.BRIGHT + __git__ + Style.RESET_ALL)
    print('         Ver.   : ' + Fore.GREEN +
          Style.BRIGHT + __VERSION__ + Style.RESET_ALL)
    print('-'*70)
    print('\n')


def main():
    args = arg_parse()
    if args.version:
        print(print_welcome_msg())
        exit(0)

if __name__ == '__main__':
    main()