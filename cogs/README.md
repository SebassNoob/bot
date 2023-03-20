
# Annoybot documentation
This readme is to give a rundown on which commands can be found in which file in this subdirectory. 

Last updated: 1.9.0

## Private features

### admin.py
A cog dedicated to admin (ie. owner-only) commands. All commands in this cog are old prefixed commands. They are called with ``a${command_name}``.

#### servers
Generates a list of servers with their names mapped to their ids.

#### sysexit
Calls ``sys.exit()`` on all threads.

#### restart
Restarts main process via ``os.execv(sys.argv[0])``

#### sync 
Syncs current command tree to discord's command tree

#### manualBackup
Manually sends database files to the webhook for db backups. Usually for transferring databases between environments.



## Public features

Refer to ``/help`` in discord or ``other/setups.py`` under method ``Setups.pages``.

### games.py
A cog dedicated to the games section of the bot. 

1. memorygame (see ``MemButton``, ``MemGame``)
2. tictactoe (see ``TicTacToeButton``, ``TicTacToe``)
3. vocabularygame (see ``./json/words.txt``)
4. typingrace (see ``./json/typingrace.txt``)
5. wouldyourather (see ``./json/wyr_options.json``)
6. truthordare (see ``./json/TorD.csv``)

### mainfeatures.py
The original (core) set of commands that Annoybot launched with. These commands are typically very simple and short. 

1. roast (see ``./json/roast.txt``)
2. insult (see https://pypi.org/project/pyinsults/)
3. urmom (see ``./json/urmom.txt``)
4. uninspire (see ``./json/uninspire.txt``)
5. dmthreaten (see ``./json/dmthreaten.txt``)
6. dadjoke (see https://pypi.org/project/dadjokes/)
7. dumbdeath (see ``./json/dumbdeath.csv``)
8. darkjoke (see ``./json/darkjoke.txt``)

### message.py
Special "message" commands. (contextmenu) These are accessed through discord's ui through right clicking a message and selecting "apps" in order to run the commands. These commands typically do something with the message that is selected.

### member.py
Special "member" commands. (contextmenu) These are accessed through discord's ui through right clicking a member and selecting "apps" in order to run the commands. These commands typically do something with the member that is selected.

### misc.py
Somewhat random commands that provide useful functionality to the bot. May not always be annoying, but they provide some value to interactions with other users.

### setups.py
A cog dedicated to the setup and usage of the bot. General information and settings can be used to customise the user's experience using the bot.

### troll.py
Commands designed to exploit discord's API to troll or otherwise annoy users.

### voice.py
These are used to play noises and sounds into a voice channel. 
