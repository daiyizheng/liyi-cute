#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/15 11:25
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : io.py
from __future__ import annotations, print_function
import pickle
import json
from typing import Dict, Union, Text, Any, List, Tuple
from pathlib import Path
import os

from liyi_cute.shared.exceptions import FileNotFoundException, FileIOException

DEFAULT_ENCODING = "utf-8"


def write_text_file(content: Text,
                    file_path: Union[Text, Path],
                    encoding: Text = DEFAULT_ENCODING,
                    append: bool = False
                    ) -> None:
    """Writes text to a file. code come from
    Args:
        content: The content to write.
        file_path: The path to which the content should be written.
        encoding: The encoding which should be used.
        append: Whether to append to the file or to truncate the file.
    """
    mode = "a" if append else "w"
    with open(file_path, mode, encoding=encoding) as file:
        file.write(content)


def write_text_ann(outputs: List[Tuple[Text, Text, Text]],
                   out_file: Text,
                   ) -> None:
    for item in outputs:
        write_text_file(item[1], os.path.join(out_file, item[0] + ".txt"))
        write_text_file(item[2], os.path.join(out_file, item[0] + ".ann"))


def read_file(filename: Union[Text, Path],
              encoding: Text = DEFAULT_ENCODING
              ) -> Any:
    """Read text from a file."""

    try:
        with open(filename, encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundException(
            f"Failed to read file, " f"'{os.path.abspath(filename)}' does not exist."
        )
    except UnicodeDecodeError:
        raise FileIOException(
            f"Failed to read file '{os.path.abspath(filename)}', "
            f"could not read the file using {encoding} to decode "
            f"it. Please make sure the file is stored with this "
            f"encoding.")


def json_to_string(obj: Any,
                   **kwargs: Any
                   ) -> Text:
    """
    Returns:
        The objects serialized to JSON, as a string.
    """
    indent = kwargs.pop("indent", 2)
    ensure_ascii = kwargs.pop("ensure_ascii", False)
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii, **kwargs)


def string_to_json(file_path,
                   encoding: Text = DEFAULT_ENCODING,
                   **kwargs: Any
                   ) -> Dict:
    return json.load(open(file_path, "r", encoding=encoding), kwargs)


def list_files(path: Text
               ) -> List[Text]:
    """Returns all files excluding hidden files.

    If the path points to a file, returns the file."""

    return [fn for fn in list_directory(path) if os.path.isfile(fn)]


def _filename_without_prefix(file: Text
                             ) -> Text:
    """Splits of a filenames prefix until after the first ``_``."""
    return "_".join(file.split("_")[1:])


def list_directory(path: Text
                   ) -> List[Text]:
    """Returns all files and folders excluding hidden files.

    If the path points to a file, returns the file. This is a recursive
    implementation returning files in any depth of the path."""

    if not isinstance(path, str):
        raise ValueError(
            f"`resource_name` must be a string type. " f"Got `{type(path)}` instead"
        )

    if os.path.isfile(path):
        return [path]
    elif os.path.isdir(path):
        results = []
        for base, dirs, files in os.walk(path, followlinks=True):
            # sort files for same order across runs
            files = sorted(files, key=_filename_without_prefix)
            # add not hidden files
            good_files = filter(lambda x: not x.startswith("."), files)
            results.extend(os.path.join(base, f) for f in good_files)
            # add not hidden directories
            good_directories = filter(lambda x: not x.startswith("."), dirs)
            results.extend(os.path.join(base, f) for f in good_directories)
        return results
    else:
        raise ValueError(f"Could not locate the resource '{os.path.abspath(path)}'.")
