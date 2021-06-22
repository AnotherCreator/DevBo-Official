# Pybo - A Crypto Inspired Discord Bot 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![License: MIT](https://img.shields.io/badge/Development_Server-PyBo-blue.svg)](https://discord.gg/25wb7AbaV5) [![License: MIT](https://img.shields.io/badge/Invite-PyBo-blue.svg)](https://discord.com/api/oauth2/authorize?client_id=733004304855597056&permissions=2435968598&scope=bot%20applications.commands)

<p align="center">
  <img width="676" height="267" src="https://github.com/AnotherCreator/Pybo-Discord-Bot/blob/master/images/Pybo_Banner.png">
</p>


Pybo (paɪ boʊ) is a [Discord](https://discord.com/brand-new) bot that utilizes the [discord.py](https://github.com/Rapptz/discord.py) 
API wrapper to run the bot. Pybo also integrates the [CoinMarketCap API](https://coinmarketcap.com/) to track and display the top 100 cryptocurrencies.

#### Quick Disclaimer:
The current version of Pybo (DevBo) being hosted here on Github will usually be the latest / stable version of the bot 
available. I am currently running two separate instances of the bot locally (DevBo | Github) and in the cloud (PyBo | Heroku). 
If you choose to invite the **official** PyBo hosted on the cloud, please be aware that there might still be some issues 
as I am continually exploring *Heroku* and *PostgreSQL*.


# Table of contents
- [Future Features](#future-features)
- [Usage](#usage)
- [Install](#install)
- [License](#license)

# Features
### Current Features
#### Infotainment
- [x] Crypto coin tracking (Local database)
- [x] Server leveling (Local database)
#### User functions
- [x] Administrative commands

### Future Features
#### Infotainment
- Increased interaction with cryptocurrency data
    - [ ] Personal 'portfolio' of simulated gains and losses of coins you 'own.'
    - [ ] Ability to buy/sell/trade coins based on current data
    - [ ] Interaction between users with their coins / fiat
- [ ] Server leveling (Heroku database)
- [ ] Server economy (Heroku database)
#### User functions
- [ ] More admin commands

# Usage

After inviting PyBo to your server, simply create a text channel called __bot-spam__ and type __;help__ into the
text bar to get a detailed list of commands. 
If you happen to join my personal [![License: MIT](https://img.shields.io/badge/Development_Server-PyBo-blue.svg)](https://discord.gg/25wb7AbaV5),
feel free to '@iTakeDonations#8077' to contact me.

# Install

### Requirements:
[Python >= 3.8](https://www.python.org/downloads/ "Python Download Page")  
[PostgreSQL >= 12.7](https://www.postgresql.org/download/ "PostgreSQL Download Page")

### PostgreSQL: 

Sample SQL script to initialize database tables:  
``` PostgreSQL
create table coin_info
(
    coin_id           integer not null,
    coin_name         varchar,
    coin_symbol       varchar,
    coin_price        real,
    coin_rank         integer,
    coin_daily_change real,
    coin_logo         varchar
);

alter table coin_info
    owner to postgres;

create unique index coin_info_coin_id_uindex
    on coin_info (coin_id);

create table user_info
(
    user_id    varchar not null,
    guild_id   varchar,
    user_level integer,
    user_xp    integer
);

alter table user_info
    owner to postgres;
```

Recommended values for user info:  
```PostgreSQL
    user_id    varchar not null,
    guild_id   varchar
    user_level integer
    user_xp    integer
```

Before running the bot, it is important to run __src/modules/market.py__ and call 'cache_coins()' in order to properly
initialize your coin data. After that, you can remove the function call and run [PyBo](src/pybo.py) by itself to turn
on the bot.

# License
[MIT](../LICENSE) © 2021 AnotherCreator
