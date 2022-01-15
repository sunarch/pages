---
layout: "default"
title: "shell scripts"
description: "programming language"
permalink: "/refs/tech/programming/languages/shell-scripts"

type: "scripting"
standard: "no"
homepage: ""
docs: ""
wikipedia: "https://en.wikipedia.org/wiki/Shell_script"
---

- type: {{ page.type }}
- standard: {{ page.standard }}

- [Wikipedia]({{ page.wikipedia }})

# Unix shells

- sh (Bourne shell)
    - [Wikipedia](https://en.wikipedia.org/wiki/Bourne_shell)
- [KornShell](http://www.kornshell.org/) (ksh)
    - [Wikipedia](https://en.wikipedia.org/wiki/KornShell)
- C shell (csh)
    - [Wikipedia](https://en.wikipedia.org/wiki/C_shell)
    - [repository](http://bxr.su/NetBSD/bin/csh/)
- [TCSH](https://www.tcsh.org/) (tcsh)
    - [Wikipedia](https://en.wikipedia.org/wiki/Tcsh)
- [Bash](https://www.gnu.org/software/bash/) (bash)
    - [Wikipedia](https://en.wikipedia.org/wiki/Bash_(Unix_shell))
- [Z shell / Zsh](https://www.zsh.org/) (zsh)
    - [Wikipedia](https://en.wikipedia.org/wiki/Z_shell)

# Windows

## cmd

## PowerShell

### timing

- StackOverflow - [Timing a command's execution in PowerShell](https://stackoverflow.com/questions/3513650/timing-a-commands-execution-in-powershell)

```PowerShell
Measure-Command { .\script.ps1 | Out-Default }
```

# other

## download an entire website

- [How To Download A Website With Wget The Right Way](https://simpleit.rocks/linux/how-to-download-a-website-with-wget-the-right-way/) by Marcelo Canina

```
wget --wait=2 \
     --level=inf \
	 --limit-rate=20K \
	 --recursive \
	 --page-requisites \
	 --user-agent=Mozilla \
	 --no-parent \
	 --convert-links \
	 --adjust-extension \
	 --no-clobber \
	 -e robots=off \
	 https://example.com
```
