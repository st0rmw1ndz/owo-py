# OwO

Python wrapper for the OwO API.

For more information about OwO, see https://whats-th.is/.

## Example Usage

```python
>>> from pathlib import Path
>>> from owo import Owo

>>> owo = Owo(key="OWO_API_KEY", domain="frosty.is-la.me")

>>> owo.shorten_url("https://st0rm.win")
'https://frosty.is-la.me/[REDACTED]'

>>> owo.upload_text("hello, world!")
'https://frosty.is-la.me/[REDACTED].txt'

>>> owo.upload_file(Path("README.md"))
'https://frosty.is-la.me/[REDACTED].md'
```

## Installation

```
pip install git+https://github.com/st0rmw1ndz/owo.git
```