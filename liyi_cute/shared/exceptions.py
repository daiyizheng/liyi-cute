#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/27 17:09
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : exceptions.py
from __future__ import annotations

class LiyiException(Exception):
    """Base exception class for all errors."""

class FileIOException(LiyiException):
    """error while doing file IO."""

class FileNotFoundException(LiyiException, FileNotFoundError):
    """file doesn't exist."""

class NotImplementedException(NotImplementedError):
    """error while doing file IO."""

class NotExistException(ValueError):
    """error while doing file IO."""

class ParamNotExistException(LiyiException):
    """miss parameter"""

class NotSupportedException(LiyiException):
    """not support format error"""