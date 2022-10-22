# Tot Server
This repository represents a small webserver to be used with the 
[ToT ! Chat Conan Mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2847709656)

## Requirements
- Python (Tested with 3.10 and 3.11)
- Flask
- pyyaml
- flask
- aiohttp
- discord


## Usage
In order to use the server you will need to provide a valid configuration with the name `config.yaml`.
Currently, the only available `Reaction` is the `DiscordMessageReaction` which sends a predefined message
via webhook to a Discord channel.

```yaml
-
    type: "discord" # type of the reaction entity
    name: "Helpful Harold" # Name of the reaction entity
    location: # location of the entity on the map
      - x # x coordinate of the reaction entity
      - y # y coordinate of the reaction entity
      - z # z coordinate of the reaction entity
    prefix_message: "The character"
    postfix_message: "is really cool!"
    channel: 2  # Number of the channel the entity should consider
                # 1 is global, 2 is local
    keyphrase: A_KEYPHRASE_TO_REACT_TO # The entity will only react if
                                       # the keyphrase is part of the message
    radius: 50 # The maximum distance a message can be away to be reacted too
    url: DISCORD_WEBHOOK_URL # The webhook 
```