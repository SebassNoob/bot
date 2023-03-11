
## Annoybot documentation
This readme is to give a rundown on which commands can be found in which file in this subdirectory.

### admin.py
A cog dedicated to admin (ie. owner-only) commands. All commands in this cog are old prefixed commands. They are called with ``a${command_name}``.

### games.py
A cog dedicated to the games section of the bot. 

### mainfeatures.py
The original (core) set of commands that Annoybot launched with. These commands are typically very simple and short. 

### message.py
Special "message" commands. These are accessed through discord's ui through right clicking and selecting to "apps" in order to run the commands. These commands typically do something with the message that is selected.

### misc.py
Somewhat random commands that provide useful functionality to the bot. May not always be annoying, but they provide some value to interactions with other users.

### setups.py
A cog dedicated to the setup and usage of the bot. General information and settings can be used to customise the user's experience using the bot.

### troll.py
Commands designed to exploit discord's API to troll or otherwise annoy users.

### voice.py
These are used to play noises and sounds into a voice channel. 
