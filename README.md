

[![PyPI downloads](https://static.pepy.tech/personalized-badge/alfred-py?period=total&units=international_system&left_color=grey&right_color=blue&left_text=pypi%20downloads)](https://pypi.org/project/liyi-cute)
[![Github downloads](https://img.shields.io/github/downloads/daiyizheng/liyi-cute/total?color=blue&label=Downloads&logo=github&logoColor=lightgrey)](https://img.shields.io/github/downloads/daiyizheng/liyi-cute/total?color=blue&label=Downloads&logo=github&logoColor=lightgrey)
[![license](https://img.shields.io/github/license/daiyizheng/liyi-cute?color=dfd)](LICENSE)
[![Slack](https://img.shields.io/badge/slack-chat-aff.svg?logo=slack)](https://join.slack.com/t/yolort/shared_invite/zt-mqwc7235-940aAh8IaKYeWclrJx10SA)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-pink.svg)](https://github.com/daiyizheng/liyi-cute/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22)

# liyi_cute: Text Tools
liyi_cute 是文本辅助工具，帮助NlPer减少模型输入前的预处理工作

## Usage:
```shell script
python setup.py install
```

```shell script
pip install liyi_cute
```
## install packages
```shell script
pip install -r requirements.txt

```
## 数据结构
```json
{
 "id": 1,
  "document": "xxxx",
  "": ""
}
```
# 信息抽取
实体抽取， 关系抽取，事件抽取， 属性抽取
以brat标注为例子:
标注文件开头标志
Entity: T
```yaml
[entities]
Protein
Entity

T8	Negative_regulation 659 668	deficient
T9	Gene_expression 684 694	expression
```
```json
{
"entities":[{"mention": "expression",
  "type": "Gene_expression",
  "start": 447,
  "end": 457,
  "id": "T1"}]
  }
```
Rlation: R
```yaml
[relations]

Protein-Component	Arg1:Protein, Arg2:Entity
Subunit-Complex	Arg1:Protein, Arg2:Entity

R1	Protein-Component Arg1:T11 Arg2:T19
R2	Protein-Component Arg1:T11 Arg2:T18

## 暂时不支持
Equiv	Arg1:Protein, Arg2:Protein, <REL-TYPE>:symmetric-transitive
*	Equiv T3 T4
```

```json
   {"relations": [{"type": "Part-of",
                 "arg1": {"mention": "c-Rel","type": "Protein","start": 139,"end": 144,"id": "T1"},
                 "arg2": {"mention": "NF-kappa B","type": "Complex", "start": 163, "end": 173, "id": "T2"},
                 "id": "R1"}]}
```

Event: E 暂时不支持
```yaml
[events]

Gene_expression Theme:Protein
Binding Theme+:Protein

E3	Binding:T9 Theme:T4 Theme2:T5 Theme3:T6
E4	Binding:T20 Theme:T16 Theme2:T17 Theme3:T19

## 暂时不支持
E6	Negative_regulation:T10 Cause:E3 Theme:E5
```
Attribute: A 暂时不支持
```yaml
[attributes]

Negation        Arg:<EVENT>
Confidence        Arg:<EVENT>, Value:Possible|Likely|Certain

```
