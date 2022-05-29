#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/15 16:57
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : readerwriter.py
from __future__ import annotations

import abc
import logging
from typing import Text, List, Any, Union, Tuple, Optional
from pathlib import Path

from liyi_cute.shared.imports.schemas.schema import Example
from liyi_cute.shared.imports.schemas.schemaItem import ExampleSchema
from liyi_cute.shared.loadings import parser
from liyi_cute.utils.io import read_file, write_text_file

logger = logging.getLogger(__file__)


class DataReader(abc.ABC):
    """Reader for NLU training data.
    """

    def __init__(self) -> None:
        """Creates reader instance."""
        self.filename: Text = ""

    def read(self, filename: Union[Text, Path], **kwargs: Any) -> "List[Any]":
        """Reads TrainingData from a file."""
        self.filename = str(filename)
        return self.reads(read_file(filename), **kwargs)

    @abc.abstractmethod
    def reads(self, s: Text, **kwargs: Any) -> "List[Any]":
        """Reads TrainingData from a string."""
        raise NotImplementedError


class DataWriter:
    """A class for writing training data to a file."""

    def dump(self, filename: Text, example: "Any") -> None:
        """Writes a TrainingData object to a file."""
        s = self.dumps(example)
        write_text_file(s, filename)

    @abc.abstractmethod
    def dumps(self, example: "Any") -> Text:
        """Turns TrainingData into a string."""
        raise NotImplementedError


class JsonDataReader(DataReader):
    """A class for reading JSON files."""
    def reads(self, filename: Text, **kwargs: Any) -> List[Example]:
        """Transforms string into json object and passes it on."""

        examples = parser(task_name=kwargs.get("task_name", "unk"),
                          fformat="json",
                          dirname=filename,
                          error="ignore")
        return examples


class JsonDataWriter(DataWriter):
    def dumps(self,
              examples: List[Example],
              **kwargs
              ) -> Text:
        return ExampleSchema().dumps(examples, many=True)


class BratDataReader(DataReader):
    def read(self, filename: Union[Text, Path],
             **kwargs: Any
             ) -> "List[Example]":

        examples = parser(task_name="unk",
                          fformat="ann",
                          dirname=filename,
                          error="ignore")

        return examples


class BratDataWriter(DataWriter):
    def dumps(self,
              examples: Optional[Example, List[Example]],
              **kwargs
              ) -> List[Tuple[Text, Text, Text]]:

        if isinstance(examples, Example):
            examples = [examples]

        list_tupe = []
        for ex in examples:
            file_name = ex.id
            text = ex.text
            entities = [ent.id + "\t" + ent.type + " " + str(ent.start) + " " + str(ent.end) + "\t" + ent.mention for
                        ent in ex.entities]
            relations = [rel.id + "\t" + rel.type + " " + "Arg1:" + rel.arg1.id + " " + "Arg2:" + rel.arg2.id for rel in
                         ex.relations]
            logger.warning("BratDataWriter about events write is not implemented")
            events = []
            content = entities + relations + events
            content = "\n".join(content)
            list_tupe.append((file_name, text, content))
        return list_tupe
