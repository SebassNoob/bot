## Annoybot
[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=SebassNoob_bot)](https://sonarcloud.io/summary/new_code?id=SebassNoob_bot)

A discord.py bot primarily used to annoy your friends, harmlessly.

### Highlights (Most used)

- roast: roast your friends with some dank roasts
- ghosttroll: ghost ping your friends in 3 different channels
- playnoise: play a stupid noise into your voice channel
- autoresponse: automatically respond to certain keywords
- ratio: produces a classic twitter ratio to ratio your friends

And so much more! We have games, trolling, memes, dark jokes, we have it!

Why wait? Piss your friends off now!




#### updating bot checklist
1. write patch notes
2. update /help
3. git commit and push to origin on dev repl
4. turn off prod (a$sysexit)
5. download .db files from prod locally
6. git pull from origin
7. paste .db

#### setup

Require:
1. python >= 3.10
2. sqlite3
3. java 8

To install:
1. ``poetry install``
2. `` java -classpath sqlite-jdbc-3.41.0.0.jar:. SetupDb``
3. ``python3 main.py``

##### contributing
uhh just open a pr, thanks

##### reverting
1. git checkout <commit_id>
2. git reset --hard <commit_id>

##### versioning

- Most recent: 1.8.4
- History: >1.5.0

When using github releases, format versions as: 'v(version_name)-(alpha/beta/rc).(id)'

eg: v1.8.0-beta.2



