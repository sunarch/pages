---
layout: "default"
title: "programs"
description: "systems - sunarch"
permalink: "/refs/personal/systems/programs"
---

# programs

================================================================================

## comms

### messaging

- Mattermost ([mattermost.com](https://mattermost.com/))
    - Linux: downloaded tar.gz
- Discord ([discord.com](https://discord.com/))
    - Linux: via downloaded deb package
- Telegram Desktop
    - Linux: local
- Signal ([signal.org](https://www.signal.org/))
    - Linux: manually set software source

### Matrix.org client

- Element ([element.io](https://element.io/))
    - web client: [https://app.element.io](https://app.element.io)

### IRC client

- Quassel IRC
- HexChat
- Pidgin : IRC client (and other messaging)

### email client

- Mozilla Thunderbird
- [Windows only] Outlook (MS Office)

### videochat

- Microsoft Teams
    - Linux: web interface, preview native app via downloaded deb
        - sets software repo
- [Windows only] Zoom
- [Windows only] Skype

================================================================================

## connections

### browser

- Mozilla Firefox
- Tor Browser
    - local
- Brave Browser
    - Linux: manually set software channel
- LibreWolf
    - https://librewolf.net/
- GhostBrowser
    - https://ghostbrowser.com/
    - Linux support in development
- [Linux only] Chromium
    - Linux package: "chromium-browser" (not available anymore)
    - Linux: Snap package
- [Linux only] GNOME Web (Epiphany browser)
    - `epiphany-browser`
- [Windows only] Google Chrome

### FTP client

- FileZilla

### torrent client

- Tixati ([tixati.com](https://tixati.com/))
    - Linux: via downloaded deb package

### remote desktop

- TeamViewer ([teamviewer.com](https://www.teamviewer.com/en/))
    - Linux: via downloaded deb package
- VNC Viewer (by RealVNC) ([realvnc.com](https://www.realvnc.com/en/connect/download/viewer/))

### SSH client

- [Linux only] ssh (terminal)
- [Windows only] PuTTY

### VPN client

- [Linux only] OpenSSH via config
- FortiClient
- [Windows only] hide.me VPN

### other

- BOINC Manager

================================================================================

## console

### Linux & Windows

- bash
    - Windows: bundled w/Git
    - Ubuntu built-in

### Linux only

- guake : dropdown terminal
- zsh : shell
- Oh My ZSH! ([ohmyz.sh](https://ohmyz.sh/)) : terminal extension
    - for zsh, Linux only
    - installed via command
- screen : terminal multiplexer
- cmatrix

### Windows only

- cmd : shell
    - Windows built-in
- PowerShell : shell
    - Windows built-in
- Git Bash : terminal
    - Windows: bundled w/Git
- Windows Terminal : terminal
    - from Microsoft Store
- Windows PowerShell : terminal
    - Windows built-in
- cmd / Parancssor : terminal
    - Windows built-in

================================================================================

## devops

### git

- Git
    - Linux: `git`, `git-extras`
- Git GUI
    - Windows: bundled w/Git
- [Windows only] GitHub Desktop

### prog. lang.

- Python
    - editor: IDLE
    - Ubuntu: 3.8
    - Windows: 3.9
        - extra local: 3.8 (for DH)
    - pip
        - panda3d
        - pygame (v2)
        - requests
- [Linux only] PyEnv
    - https://github.com/pyenv/pyenv
- gcc (for C)
    - 1a-ubt, 1b-win: bundled w/MinGW64
    - Linux-current: gcc-8
    - dependencies on Linux: libasan5, libatomic1, libc-dev-bin, libc6-dev, lbgcc-8-dev, libitm1, liblsan0, libmpx2, libtsan0, libubsan1, linux-libc-dev, manpages-dev
- Ruby : (for Jekyll local)
- make, make-doc
    - Windows: bundled w/MinGW64
- Racket
    - editor: DrRacket
- Gephi
    - for Graphviz
- Java
    - Oracle JDK
        - bin in path or linked to other bin folder
    - Azul Zulu builds of OpenJDK
        - needed for worldographer: JDK FX
        - [download page](https://www.azul.com/downloads/?package=jdk-fx)
    - [Linux only] OpenJDK
- Haskell
    - GHC - Glasgow Haskell Compiler
    - Linux: `ghc`
    - cabal - package installer
        - Linux: `cabal-install`

### docker

- Docker
- [Windows only] Docker Desktop

### virtualization

- [Oracle VM VirtualBox](https://www.virtualbox.org)
- [QEMU](https://www.qemu.org)

### references

- Game of Life
    - Linux: install locally
- Sound of sorting
    - Linux? install locally

================================================================================

## editors and IDEs

### IDE

- PyCharm Community Edition
- Visual Studio Code : (for JavaScript)
- Thonny  : with bundled Python
- Code::Blocks : (for C)
- IntelliJ IDEA Community Edition (for Clojure)
- Eclipse

### text editor

- Atom: https://atom.io/
    - Linux:
        - repository package no longer available
        - snap
        - downloadable deb and rpm on homepage
- [Linux only] geany
    - plugins
        - automark
        - extrasel
        - git-changebar
        - lineoperations
        - overview
        - spellcheck
- [Linux only] vim
- [Windows only] Notepad++
- [Windows only] Notepad / Jegyzettömb
    - Windows built-in

### hex editor

- [Linux only] bless
- [Windows only] HxD

### SQLite

- [Linux only] `sqlitebrowser`

================================================================================

## documents

### PDF viewer

- [Linux only] "Document Viewer" - evince
- [Windows only] Adobe Reader DC

### LaTeX editor

- TeXworks
- [Linux only] TeXstudio
    - not primarily used
- [Linux only] Texmaker
    - not primarily used
- [Windows only] MiKTeX : LaTeX distribution
    - MiKTeX Console : LaTeX package management

### office pack

- LibreOffice
    - Linux: "libreoffice" (full meta-package, not necessary)
        - installed with distribution: libreoffice-calc, libreoffice-draw, libreoffice-impress, libreoffice-math, libreoffice-writer
        - libreoffice-l10n-... : hu, de, es, ar
        - libreoffice-help-hu
    - https://www.libreoffice.org/
- MS Office: Word, Excel, PowerPoint, OneNote
    - Linux: web interface
    - Windows: via Office 365
    - https://www.office.com/
- [Windows only] MS Office: Publisher, Access
    - via Office 365
- OnlyOffice
    - https://www.onlyoffice.com/

### epub editor

- Sigil

### diff viewer

- Meld

### other

- Zotero

### Linux only

- hyphen-... : de, es, hu

================================================================================

## media

### media player

- VLC media player (by VideoLAN)
    - Linux extras:
        - "vlc-plugin-fluidsynth"
- Spotify
    - Linux: https://www.spotify.com/us/download/linux/
        - web interface
        - snap
        - manually added source line (see homepage)
    - Windows: Microsoft Store
- [Linux only] mpv
    - `mpv` : video player
    - `celluloid` : GTK frontend for mpv
- [Windows only] Netflix
    - Windows: Microsoft Store
- [Windows only] Windows Media Player

### image editor

- GIMP
- Inkscape : vector graphics / svg editor
- Worldographer : hexagonal map builder
- [Windows only] Paint
- [Windows only] Paint 3D

### audio editor

- Audacity
- Sonic Pi
- LMMS
- Musescore 3 : sheet music editor

### video editor

- blender
- DaVinci Resolve
    - bundled: Blackmagic RAW Player
    - bundled: Fairlight Studio Utility
- [Linux only] shotcut
    - installed separately, not from repo
- [Windows only] "Videoszerkesztő"
- [Windows only] Corel VideoStudio Pro X5

### streaming

- OBS Studio (64 bit)
- [Windows only] Twitch Studio

### Adobe CC (Windows only)

- Adobe Lightroom Classic CC
- Adobe Lightroom CC
- Adobe Photoshop CC
- Adobe Creative Cloud

================================================================================

## utilities

### system tools

- [Linux only] `gnome-system-tools`

### package managers

- [Linux only] apt
    - Ubuntu default
- [Linux only] `synaptic` - apt frontend
    - install before it: `apt-xapian-index`
        - `sudo update-apt-xapian-index -vf`

### todo & notes

- Notion
    - Linux: web interface
- Todoist
    - Linux: Snap, AppImage

### file sharing

- Dropbox
    - Ubuntu: `nautilus-dropbox` - downloads proprietary Dropbox binary from website
- OneDrive
    - Linux:
        - online interface
        - onedriver
            - GitHub - [jstaf / onedriver](https://github.com/jstaf/onedriver)
            - Launchpad - [jstaf / onedriver](https://launchpad.net/~jstaf/+archive/ubuntu/onedriver)
                - not used anymore, see GitHub ReadMe
            - AUR - [onedriver](https://aur.archlinux.org/packages/onedriver/)
            - OpenSUSE Build Service: [onedriver](https://software.opensuse.org/download.html?project=home%3Ajstaf&package=onedriver)
    - Windows built-in

### file explorer

- [Linux only] Nautilus (Ubuntu default)
    - `nautilus-gtkhash` - hashing plugin
- [Linux only] Thunar (Xfce default)
- [Linux only] ranger : terminal-based

### system monitor

- [Linux only] htop (console)
    - also has app list entry
- [Linux only] GNOME System Monitor
- [Windows only] Task Manager
- [Windows only] System monitor (?)

### finance and budgeting

- GNUCash - https://www.gnucash.org/
    - https://github.com/Gnucash/
    - GPLv2/3
    - C, C++, Scheme
- HomeBank - http://homebank.free.fr/en/
    - https://code.launchpad.net/homebank
    - GPLv2
- Eqonomize - http://eqonomize.github.io/
    - https://github.com/Eqonomize/Eqonomize
    - GPLv3
- Grisbi - https://en.grisbi.org/
    - manual mostly French
    - https://github.com/grisbi/grisbi
    - GPLv2
- hledger - https://hledger.org/
    - Haskell port of ledger
    - https://github.com/simonmichael/hledger/
- ledger - https://www.ledger-cli.org/
    - https://github.com/ledger/ledger
    - BSD license
    - C++
- Skrooge - https://skrooge.org/
    - for KDE
- Firefly III - https://www.firefly-iii.org/
    - https://github.com/firefly-iii/firefly-iii
    - PHP
    - AGPLv3

### Linux only

- AppImageLauncher
    - https://github.com/TheAssassin/AppImageLauncher
    - https://launchpad.net/~appimagelauncher-team/+archive/ubuntu/stable
- flameshot
    - "Powerful yet simple-to-use screenshot software"
    - https://github.com/flameshot-org/flameshot

### Windows only

- WinDirStat: disk usage
- "Vezérlőpult"
- Bitdefender
- 7-Zip File Manager
- Speccy (by Piriform)
- Recuva (by Piriform)
- "Feladatkezelő"
- "Windows Felügyeleti Eszközök"
- Microsoft Store
- RapidCRC
- "Térképek"
    - Windows built-in
- "Diktafon"
    - Microsoft Store
- "Metszet és vázlat"
    - Microsoft Store
- "Képernyő-billentyűzet"
    - Windows built-in
- "Időjárás"
    - Microsoft Store

================================================================================

## devices

### Linux & Windows

- Brasero : disk burner
- Document Scanner
- Cheese : webcam recorder
- Sound Juicer : audio CD ripper
- calibre 64bit : E-book management
- Raspberry Pi Imager

### Linux only

### Windows only

- Canon Scan > IJ Scan Utility
- Canon Scan > Quick Menu
- Samsung Magician : SSD management
- ARMOURY CRATE
- WD Discovery
- PlayMemories Home : Sony Handycam
- Garmin Express
- Lenovo Vantage
- Lenovo Service Bridge
- System Update (Lenovo)

================================================================================

## references

# multiplatform

- Obsidian ([obsidian.md](https://obsidian.md/))
    - Linux: AppImage, Snap, Flatpak
    - enforces LF line endings for all opened files
        - there is no setting to change it (yet?)
- abevjava (ÁNYK)
    - requires Java

# Linux only

- instead - Simple text adventures/visual novels engine

### Windows only

- CCleaner (by Piriform)
- Defraggler (by Piriform)
    - not usable for SSDs
- FormatFactory : converter
- XnView
- Garmin BaseCamp
- Nokia Suite

================================================================================