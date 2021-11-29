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

# features

## Data Classes

- [Python docs](https://docs.python.org/3/library/dataclasses.html)
- Towards Data Science: [9 Reasons Why You Should Start Using Python Dataclasses](https://towardsdatascience.com/9-reasons-why-you-should-start-using-python-dataclasses-98271adadc66)

# tools

## linting

### Pylint

- [Pylint User Manual](https://pylint.pycqa.org/en/latest/)

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

# Python games

- [list on Python wiki](https://wiki.python.org/moin/PythonGames)
- [Free Python Games](http://www.grantjenks.com/docs/freegames/) by [Grant Jenks](https://github.com/grantjenks)
- StackOverflow: [Does PyGame do 3d?](https://stackoverflow.com/questions/4865636/does-pygame-do-3d)

## [Pygame](https://www.pygame.org)

- interface to the Simple Directmedia Library (SDL)
- [Python Wiki](https://wiki.python.org/moin/PyGame)
- GitHub:[pygame/pygame](https://github.com/pygame/pygame)
- [docs](https://www.pygame.org/docs/)

## [Panda3d](https://www.panda3d.org/)

- GitHub: [panda3d/panda3d](https://github.com/panda3d/panda3d)
- [docs](https://docs.panda3d.org/1.10/python/index)

# snippets

## conditional compilation

- [Conditional compilation in Python](https://stackoverflow.com/questions/560040/conditional-compilation-in-python)
    - when calling python with the -O or -OO options, `__debug__` will be false

```Python
if __debug__:
    doSomething()
```

# other

- [Redirecting all kinds of stdout in Python](https://eli.thegreenplace.net/2015/redirecting-all-kinds-of-stdout-in-python/)

## multiple versions

- Unix & Linux StackExchange - [Install newer & older versions of python on debian?](https://unix.stackexchange.com/questions/188741/install-newer-older-versions-of-python-on-debian)

# music generation

- StackOverflow: [Is there a way to play raw 8bit PCM data using pygame?](https://stackoverflow.com/questions/69531725/is-there-a-way-to-play-raw-8bit-pcm-data-using-pygame)

## packages

- [zacharydenton/wavebender](https://github.com/zacharydenton/wavebender)
    - [Generate Audio with Python](https://zach.se/generate-audio-with-python/)
- [benmoran56/chippy](https://github.com/benmoran56/chippy)
