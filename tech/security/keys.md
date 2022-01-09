---
layout: "default"
title: "keys"
description: "tech refs"
permalink: "/refs/tech/security/keys"
---

# PGP

## GPG

#### Secret key backup

```bash
gpg --output backupkeys.pgp --armor --export-secret-keys --export-options export-backup user@email
```
(from [How to export a GPG private key and public key to a file](https://newbedev.com/how-to-export-a-gpg-private-key-and-public-key-to-a-file))
