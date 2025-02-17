# Pokefier Bot Implementation Details

## Execution Flow
- The bot initializes and logs its activities.
- It reads configuration from a JSON file, including settings for delays, tokens, and other operational parameters.
- The bot listens to commands and messages on Discord and processes them accordingly.

## Commands Overview
The bot listens for specific commands which can be used by the owner. Below are the commands implemented:

### Commands
- **trade `<user>`**
  - Purpose: Request a trade with a specified user.
  
- **help**
  - Purpose: Displays all available commands.

- **ping**
  - Purpose: Checks the latency of the bot.

- **incense `<time>` `<interval>`**
  - Purpose: Starts an incense session with specified time and interval.
  - Valid Time Options: `30m`, `1h`, `3h`, `1d`
  - Valid Interval Options: `10s`, `20s`, `30s`

- **shardbuy `<amount>`**
  - Purpose: Allows the owner to buy a specified number of shards.

- **channeladd `<channel_ids>`**
  - Purpose: Add specified channel IDs to the whitelist.

- **channelremove `<channel_ids>`**
  - Purpose: Remove specified channel IDs from the whitelist.

- **blacklistadd `<pokemons>`**
  - Purpose: Add specified Pokémon to the blacklist.
  
- **blacklistremove `<pokemons>`**
  - Purpose: Remove specified Pokémon from the blacklist.

- **languageadd `<languages>`**
  - Purpose: Add specified languages to the bot's supported languages.

- **languageremove `<languages>`**
  - Purpose: Remove specified languages from the supported list.

- **solved**
  - Purpose: Confirms that the captcha has been solved.

- **config**
  - Purpose: Displays the current configuration settings.

- **say `<message>`**
  - Purpose: Make the bot send a specified message.

## Event Handling
The bot handles various events including:
- Capturing messages from Poketwo and determining actions based on content.
- Processing trade requests and confirmations.
- Managing Pokémon spawn messages and responding accordingly.
- Log information for actions taken and errors encountered.

## Logging
Logs are maintained at various levels (info, warning, error, and debug) to trace the bot's operations and any issues.

## Configuration Details
Configuration parameters are read from `config.json`, including:
- DELAY
- TOKENS
- OWNER_ID
- LOGGING
- POKETWO_ID
- BLACKLISTED_POKEMONS
- WHITELISTED_CHANNELS
- Supported languages

## License
This project is open-source, available for modification according to the user's needs.

# Conclusion
The Pokefier bot runs autonomously to interact with the Poketwo game on Discord, following predefined command structures and configurations, with the ability to catch Pokémon, engage in trades, and maintain a log of all activities.
