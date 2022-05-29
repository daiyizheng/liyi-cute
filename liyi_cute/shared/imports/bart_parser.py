# -*- coding:UTF-8 -*-

# author:user
# contact: test@test.com
# datetime:2022/3/29 12:07
# software: PyCharm

"""
文件说明：
    
"""
from __future__ import annotations


from typing import Optional, Text, Union, Dict, List
from collections import Iterable
import re, os, logging

from tqdm import tqdm

from liyi_cute.shared.imports.base_parser import BasePaeser
from liyi_cute.shared.imports.schemas.schema import Example, Entity, Relation
from liyi_cute.utils.common import iter_file_groups

logger = logging.getLogger(__file__)

class BratParser(BasePaeser):
    """Parser for brat rapid annotation tool (Brat).

    Args:
        task_name: do work name
        ignore_types: types to ignore, should be in {"T", "R"}. (default: None)
        error : Error handling, should be in {"raise", "ignore"}.  (default: "raise")
    """
    exts = {".ann", ".txt"}
    support_task_name = {"ner", "rel"} #  "ner", "rel" "env", "attr"
    types = {"T", "R"} # types = {"T", "R", "*", "E", "N", "AM"}
    def __init__(self, task_name,
                 ignore_types: Optional[Iterable[str]] = None,
                 error: str = "raise",
                 lang="en"):
        super().__init__(task_name,ignore_types, error, lang)


    async def parse(self, dirname: Union[str, bytes, os.PathLike],
                    encoding: str = "utf-8") -> List[Example]:
        """Parse examples in given directory.

        Args:
            dirname : Directory  containing brat examples.
            task_name: work name
            encoding : Encoding for reading text files and ann files

        Returns:
            examples (list[Example]): Parsed examples.
        """
        examples = []
        file_groups = iter_file_groups(dirname, self.exts, missing="error" if self.error == "raise" else "ignore")
        for key, (ann_file, txt_file) in tqdm(file_groups):
            txt = await self._parse_text(txt_file, encoding=encoding)
            ann = await self._parse_ann(ann_file, encoding=encoding)
            examples.append(Example(task_name=self.task_name, id=key,text=txt, **ann))

        examples.sort(key=lambda x: x.id if x.id is not None else "")
        self.examples = examples
        return examples


    async def _parse_text(self, txt:Text, encoding:Text)->Text:  # pylint: disable=no-self-use
        with open(txt, mode="r", encoding=encoding) as f:
            return f.read()


    async def _parse_ann(self, ann:Text, encoding:Text)->Dict:

        entity_matches, relation_matches = [], []
        with open(ann, mode="r", encoding=encoding) as f:
            for line in f:
                line = line.rstrip()

                if not line or line.startswith("#") or self._should_ignore_line(line):
                    continue
                ## 匹配实体
                if line.startswith("T"):
                    match = self._parse_entity(line)
                    if match:
                        entity_matches += [match]

                ## 匹配关系
                elif line.startswith("R"):
                    match = self._parse_relation(line)
                    if match:
                        relation_matches += [match]

                elif line.startswith("*"):
                    logger.warning(f"The '*' interface is not implemented, line: {line}")

                elif line.startswith("E"):
                    logger.warning(f"The 'E' interface is not implemented, line: {line}")

                elif line.startswith("N"):
                    logger.warning(f"The 'N' interface is not implemented, line: {line}")

                elif line.startswith("AM"):
                    logger.warning(f"The 'AM' interface is not implemented, line: {line}")

        # Format entities.
        entities = self._format_entities(entity_matches)
        self._check_entities(entities.values())
        if self.task_name=="ner":
            self.examples = {"entities": list(entities.values()), "relations": [], "events":[]}
            return self.examples

        # Format relations.
        relations = self._format_relations(relation_matches, entities)
        if self.task_name=="rel":
            self.examples = {"entities": list(entities.values()), "relations": relations, "events": []}
            return self.examples

        # Format events.
        # events = self._format_events(event_matches, entities) # "events": list(events.values()),
        self.examples = {"entities": list(entities.values()), "relations": [], "events":[]}
        return self.examples

    def _parse_entity(self, line):
        regex = re.compile(
            r"""(?P<id>T\d+)
                \t(?P<type>[^ ]+)
                \ (?P<start>\d+)
                \ (?P<end>\d+)
                \t(?P<mention>.+)""",
            re.X,
        )
        match = re.match(regex, line)
        if not match:
            self._raise_invalid_line_error(line)

        return match

    def _format_entities(self, entity_matches:Optional[List[re.compile]]):
        # pylint: disable=no-self-use
        return {
            match["id"]: Entity(
                mention=match["mention"],
                type=match["type"],
                start=int(match["start"]),
                end=int(match["end"]),
                id=match["id"],
            )
            for match in entity_matches
        }

    def _check_entities(self, entities:List):
        """pylint: disable=no-self-use"""
        pool = {}
        for entity in entities:
            id_ = pool.setdefault((entity.start, entity.end), entity.id)
            if id_ != entity.id:
                self._raise(RuntimeError("Detected identical span for"f" different entities: [{id_}, {entity.id}]"))


    def _parse_relation(self, line):
        regex = re.compile(
            r"""(?P<id>R\d+)
                \t(?P<type>[^ ]+)
                \ Arg[12]:(?P<arg1>T\d+)
                \ Arg[12]:(?P<arg2>T\d+)""",
            re.X,
        )
        match = re.match(regex, line)
        if not match:
            self._raise_invalid_line_error(line)

        return match

    def _format_relations(self, relation_matches, entities):
        relations = []
        for rel in relation_matches:
            arg1_id, arg2_id = rel["arg1"], rel["arg2"]
            arg1 = entities.get(arg1_id)
            arg2 = entities.get(arg2_id)
            if not arg1 or not arg2:
                self._raise(KeyError(f"Missing relation arg: {arg1_id if not arg1 else arg2_id}"))

            relations += [
                Relation(type=rel["type"], arg1=arg1, arg2=arg2, id=rel["id"])
            ]

        return relations

