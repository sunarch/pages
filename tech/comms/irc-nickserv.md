---
layout: "default"
title: "NickServ (IRC)"
description: "catalog | tech refs"
permalink: "/refs/tech/comms/irc/nickserv"
---

```/msg NickServ REGISTER $password $email```

```/msg NickServ VERIFY REGISTER $nick $token```

```/msg NickServ SET ENFORCE ON```

```/msg NickServ GROUP $mainnick $password```
on OFTC: `/msg NickServ GROUP $other_nick $password`

```/msg NickServ SET EMAIL $email```

```/msg NickServ INFO $nick [ALL]```

```/msg NickServ IDENTIFY $nick $password```
on OFTC: `/msg NickServ IDENTIFY $password $nick`

```/msg NickServ SET PASSWORD $password```

on OFTC: `/msg NickServ SET CLOAK ON`
