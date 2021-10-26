---
layout: "default"
title: "Python"
description: "programming language"
permalink: "/refs/tech/programming/languages/python"

type: "general"
standard: "yes"
homepage: "https://www.python.org/"
docs: "https://docs.python.org/3/"
wikipedia: "https://en.wikipedia.org/wiki/Python_(programming_language)"
---

- type: {{ page.type }}
- standard: {{ page.standard }}
- [homepage]({{ page.homepage }})
- [documentation]({{ page.docs }})
- [Wikipedia]({{ page.wikipedia }})

### description

scripting, readability, extensible

# [Python Discord](https://www.pythondiscord.com/)

## [Python Discord Pixels](https://pixels.pythondiscord.com/)

- [Pixel History for the Python Discord Pixels Event of May/June 2021](https://www.kaggle.com/joebanks/python-discord-pixels) by Joe Banks

# videos

- [What Does It Take To Be An Expert At Python?](https://youtu.be/7lmCu8wz8ro)
    - metaclasses, decorators, generator, context manager

```
# decorator for turning a generator into a context manager
from contextlib import contextmanager
```

## finance

- [12 Factors of Pain and Suffering (How Developers Screw Up)](https://youtu.be/wm-az9nQJvg)

# snippets

## conditional compilation

- [Conditional compilation in Python](https://stackoverflow.com/questions/560040/conditional-compilation-in-python)
    - when calling python with the -O or -OO options, `__debug__` will be false

```Python
if __debug__:
    doSomething()
```
