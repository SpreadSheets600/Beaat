# ⚙️ Pokefier Bot Detailed Overview

## 📜 Description
The **Pokefier Bot** is a Discord bot designed to automate interactions with the Poketwo game. It supports various commands for trading, catching Pokémon, and managing configurations.

## ## 🚀 Execution Flow
1. **Initialization**: The bot initializes and sets up logging.
2. **Configuration**: Reads settings from a JSON file.
3. **Event Listening**: Listens for commands and messages on Discord.
4. **Command Processing**: Executes commands based on user input.

## ✨ Features

- **Automation**: Automates Pokémon catching and trading processes.
- **Custom Commands**: Execute a wide range of commands to interact with Poketwo.
- **Real-time Interaction**: Responds to game events instantaneously.
- **Logging**: Maintains detailed logs of operations and errors.
  
## 🛠️ Commands Overview

| Command             | Description                                                    |
|---------------------|----------------------------------------------------------------|
| **`trade <user>`**  | Request a trade with a specified user.                       |
| **`help`**          | Displays all available commands.                             |
| **`ping`**          | Checks the latency of the bot.                               |
| **`incense <time> <interval>`** | Starts an incense session with specified time and interval. Valid time options: `30m`, `1h`, `3h`, `1d`. Valid interval options: `10s`, `20s`, `30s`. |
| **`shardbuy <amount>`** | Buy a specified number of shards.                            |
| **`channeladd <channel_ids>`** | Adds specified channel IDs to the whitelist.          |
| **`channelremove <channel_ids>`** | Removes specified channel IDs from the whitelist.    |
| **`blacklistadd <pokemons>`** | Adds specified Pokémon to the blacklist.               |
| **`blacklistremove <pokemons>`** | Removes specified Pokémon from the blacklist.        |
| **`languageadd <languages>`** | Adds specified languages to the bot's supported languages. |
| **`languageremove <languages>`** | Removes specified languages from the supported list.   |
| **`solved`**       | Confirms that the captcha has been solved.                   |
| **`config`**       | Displays the current configuration settings.                  |
| **`say <message>`** | Make the bot send a specified message.                        |

## 🔍 Event Handling
- Detects and processes Pokémon spawn messages.
- Handles trade requests and confirmations.
- Logs information and errors for monitoring purposes.

## 📝 Configuration Read
The bot’s configuration is loaded from `config.json`, where you can set:
- **DELAY**: Delay times for processing.
- **TOKENS**: Bot tokens for multiple instances.
- **LOGGING**: Turn logging on or off.
- **OWNER_ID**: Your Discord ID for command permissions.
- **POKETWO_ID**: The ID for Poketwo interactions.
- **BLACKLISTED_POKEMONS**: Pokémon that should not be caught.
- **WHITELISTED_CHANNELS**: Channels where the bot is allowed to operate.
- **LANGUAGES**: Supported languages for commands.

## 📄 Licensing
This project is **open-source**, allowing users to modify it according to their requirements.

# Conclusion
The Pokefier Bot enhances your gameplay experience by automating essential tasks and providing real-time interaction with the Poketwo game. Customize it further to suit your specific needs!
