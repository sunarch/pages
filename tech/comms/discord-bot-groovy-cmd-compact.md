---
layout: "default"
title: "Groovy commands - compact"
description: "comms | tech refs"
permalink: "/refs/tech/comms/groovy-cmd-compact"
---

*updated: 2021-04-27*

```
-join                              - Makes the bot join your voice channel.
-disconnect                        - Disconnects the bot from your voice channel and clears the queue.

-play [link or search query]       - Loads your input and adds it to the queue. If there is no playing track, then it will start playing.
-play file                         - Plays the file attached to the message.
-queue                             - Displays the queue.
-next                              - Skips to the next song.
-back                              - Skips to the previous song.
-clear                             - Removes all tracks from the queue.
-jump [track position or title]    - Skips to the specified track.
-remove [track position or title]  - Removes the specified track from the queue.
-remove range [start], [end]       - Removes all the tracks from the specified start to the specified end. Inclusive.
-shuffle                           - Randomizes the tracks in the queue.
-search [query]                    - Searches for your query on YouTube and lets you choose which songs to queue. To queue a track of the results, just type it's number.
-move [track], [new position]      - Moves the specified song to the specified position.
```

```
-loop track                        - Starts looping your current playing track.
-loop queue                        - Starts looping your current queue.
-loop off                          - Stops looping.
-lyrics                            - Displays lyrics for the playing track.
-lyrics [query]                    - Searches for your query and displays the returned lyrics.
-pause                             - Pauses playback
-resume                            - Resumes playback.
 -song [song]                      - Displays info about the specified track in the queue.
-song                              - Displays info about the playing track.
-reset effects                     - Resets all audio effects.
 -fast forward [amount]            - Fast forwards the player by your specified amount. The default amount is 10 seconds
-rewind [amount]                   - Rewinds the player by your specified amount. The default amount is 10 seconds.
-seek [position]                   - Sets the playing track's position to the specified position.
-stop                              - Stops the current playing track.
```
