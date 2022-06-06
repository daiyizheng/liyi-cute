# imports
## BratParser
```python
from liyi_cute.shared.imports.bart_parser import BratParser
brat = BratParser(task_name="rel/ner", error="ignore")
examples = await brat.parse("to/you/path")

```