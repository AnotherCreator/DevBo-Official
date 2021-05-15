# Pybo - A Crypto Inspired Discord Bot 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![License: MIT](https://img.shields.io/badge/Dev_Server-PyBo-blue.svg)](https://discord.gg/25wb7AbaV5) [![License: MIT](https://img.shields.io/badge/Bot_Invite-PyBo-blue.svg)](https://discord.com/api/oauth2/authorize?client_id=733004304855597056&permissions=2435968598&scope=bot%20applications.commands)

<p align="center">
  <img width="676" height="267" src="https://github.com/AnotherCreator/Pybo-Discord-Bot/blob/master/images/Pybo_Banner.png">
</p>


Pybo (paɪ boʊ) is a [Discord](https://discord.com/brand-new) bot that integrates the 
[CoinMarketCap API](https://coinmarketcap.com/) to track and display the top 100 cryptocurrencies.


# Table of contents
- [Usage](#usage)
- [Install](#local-installation)
- [License](#license)

# Usage

# Local Installation

### Requirements:
[Python >= 3.8](https://www.python.org/downloads/ "Python Download Page")  
[PostgreSQL >= 12.7](https://www.postgresql.org/download/ "PostgreSQL Download Page")  
[psycopg2 >= 2.8.6](https://pypi.org/project/psycopg2/ "Library Download")  
[Discord.py >= 1.7.2](https://discordpy.readthedocs.io/en/stable/intro.html "Library Download")

### PostgreSQL: 

SQL Script to initialize local database tables:  
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

Before running the bot, it is important to run __src/modules/market.py__ and call 'cache_coins()' in order to properly
initialize your coin data. After that, you can remove the function call and run [PyBo](src/pybo.py) by itself to turn
on the bot.

# License
[MIT](../LICENSE) © 2021 AnotherCreator