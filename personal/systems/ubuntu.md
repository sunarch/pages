---
layout: "default"
title: "Ubuntu"
description: "personal system"
permalink: "/refs/personal/systems/ubuntu"
---

# Ubuntu

See also [RC - Ubuntu](https://github.com/sunarch/sunarch-rc/tree/main/ubuntu).

## PPAs

- Deadsnakes (older python versions)
    - https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa
    - by [Felix Krull](https://launchpad.net/~fkrull)

- Grub Customizer
    - https://launchpad.net/~danielrichter2007/+archive/ubuntu/grub-customizer
    - Ubuntu repository version available

- OBS Studio
    - https://launchpad.net/~obsproject/+archive/ubuntu/obs-studio
    - Ubuntu repository version available

- Pygame + Python3
    - https://launchpad.net/~thopiekar/+archive/ubuntu/pygame
    - Ubuntu repository version available

- RuneScape
    - Ubuntu repository version available

- TeamViewer
    - added automatically when installing from downloaded DEB package

## setup

### primary

- "gnome" with all dependencies
- hunspell, hunspell-ar, hunspell-de-de, hunspell-en-us, hunspell-hu, hunspell-es
- exfat-fuse, exfat-utils
- ubuntu-wallpapers-eoan (Ubuntu 19.10 Wallpapers)

### delete

- gnome, gnome-core
- gnome-user-share, apache2-bin, libapache2-mod-dnssd
- evolution (& related), bogofilter (& related)
- gnome-contacts, libfolks-eds25
- gnome-maps, libfolks25
- gnome-documents, gnome-online-miners
- folks-common
- gnome-music
- aspell, aspell-en
- gnome-online-accounts
- ubuntu-web-launchers

### Git config

- ```git config --global user.email "EMAIL"```
- ```git config --global user.name “FULL_NAME”```
- ```git config --global user.signingkey KEY_ID```
- ```git config --global commit.gpgsign true```
- ```git config --global init.defaultBranch main```
- ```git config --global pull.rebase true```
- clone GitHub repositories into home > Documents > github
- clone GitLab repositories into home > Documents > gitlab

### todo

- nautilus settings
- gnome terminal settings
    - in Gnome Tweaks:
        - enable: Extensions > Kstatusnotifieritem/appindicator support
- add VPNs
- add bash, zsh configs
