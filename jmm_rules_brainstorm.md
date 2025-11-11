# Jellyfin Meta Manager (JMM) Rules Brainstorm

This document contains a comprehensive list of potential tags you can automate using Jellyfin Meta Manager (JMM). Use this as a blueprint for building your `movies.yml` configuration file.

---

## Automation Methods: A Deeper Dive

There are two primary methods we'll use to automate tags. The key is to let computers handle objective facts and use human curation (either your own or the community's) for subjective opinions.

### 1. Trakt Lists (For Subjective & Thematic Tags)

This is the recommended way to automate subjective tags without writing a custom "agent".

-   **Your Personal Lists:** For hyper-specific tags like `girly-pop` or `inspirational`, you create a private list on [Trakt.tv](https://trakt.tv/). You are the curator. JMM reads this list and applies the tag.
-   **Public Community Lists:** For broader themes like `feel-good` or `mind-bending`, you can find popular, well-maintained **public lists** on Trakt. Instead of curating your own, you leverage the work of the community. You find a list you like, and point JMM to it.

**This is the best way to automate opinions.**

### 2. TMDb Data (For Objective, Factual Tags)

For factual tags, JMM can pull data directly from TheMovieDB (TMDb). This is perfect for tagging based on official genres, keywords, release dates, awards, etc.

---

## Expanded Tag Ideas & Automation Logic

### Category 1: Subjective, Thematic, & Tonal Tags
**(Recommended Method: Your Own or Public Trakt Lists)**

| Desired Tag | Trakt List Name | Description |
| :--- | :--- | :--- |
| `girly-pop` | Girly Pop | Movies that are women-empowering or considered "chick flicks". |
| `date-night` | Date Night | Good movies for a date night. |
| `feel-good` | Feel Good Movies | Uplifting and heartwarming films. |
| `inspirational`| Inspirational | Stories of perseverance and achievement. |
| `raunchy` | Raunchy Comedies | Comedies with adult or crude humor. |
| `mind-bending`| Mind-Bending | Movies with complex plots, twists, or surrealism. |
| `rainy-day` | Rainy Day Flicks | Comforting or engaging movies perfect for a day indoors. |
| `holiday` | Holiday Movies | Films centered around specific holidays (Christmas, Halloween, etc.). |
| `guilty-pleasure`| Guilty Pleasures | Movies you love, regardless of critical reception. |
| `cult-classic` | Cult Classics | Films with a dedicated, passionate fanbase. |
| `slow-burn` | Slow Burn | Stories that build tension and atmosphere gradually. |
| `atmospheric` | Atmospheric | Movies with a strong, immersive mood or feeling. |
| `bleak` | Bleak & Somber | Films with a dark, pessimistic, or melancholic tone. |
| `whimsical` | Whimsical | Playful, quaint, and fanciful films. |
| `ensemble-cast`| Ensemble Casts | Movies featuring a large cast of principal actors. |
| `so-bad-its-good`| So Bad It's Good | Enjoyably bad movies. |

### Category 2: Objective & Factual Tags
**(Recommended Method: TMDb Data)**

#### Sub-Category: Genre, Medium & Era

| Desired Tag | Automation Logic (TMDb) |
| :--- | :--- |
| `animation` | Genre is "Animation". |
| `anime` | Keyword is "anime". |
| `live-action` | Genre is NOT "Animation". |
| `stop-motion` | Keyword is "stop motion". |
| `hand-drawn` | Keyword is "hand-drawn animation". |
| `cgi-animation`| Keyword is "cgi" or "computer animation". |
| `black-and-white`| `colors` field in TMDb data is empty or indicates B&W. |
| `silent-film` | Keyword is "silent film". |
| `oscar-winner` | Award information indicates a "Best Picture" Oscar win. |
| `golden-globe-winner`| Award information indicates a "Best Motion Picture" Golden Globe win. |
| `60s` | Release year is between 1960-1969. |
| `70s` | Release year is between 1970-1979. |
| `80s` | Release year is between 1980-1989. |
| `90s` | Release year is between 1990-1999. |
| `2000s` | Release year is between 2000-2009. |
| `2010s` | Release year is between 2010-2019. |
| `2020s` | Release year is between 2020-2029. |

#### Sub-Category: Topics, Keywords & Concepts

| Desired Tag | Automation Logic (TMDb) |
| :--- | :--- |
| `money` | Keyword is "money", "wall street", or "finance". |
| `dystopian` | Keyword is "dystopia". |
| `cyberpunk` | Keyword is "cyberpunk". |
| `steampunk` | Keyword is "steampunk". |
| `post-apocalyptic`| Keyword is "post-apocalyptic". |
| `time-travel` | Keyword is "time travel". |
| `space-travel`| Keyword is "space travel". |
| `alien-invasion`| Keyword is "alien invasion". |
| `heist` | Keyword is "heist". |
| `mockumentary`| Keyword is "mockumentary". |
| `spy` | Keyword is "spy" or "espionage". |
| `disaster` | Keyword is "disaster". |
| `martial-arts`| Keyword is "martial arts". |
| `superhero` | Keyword is "superhero". |
| `film-noir` | Keyword is "film noir". |
| `coming-of-age`| Keyword is "coming of age". |
| `road-trip` | Keyword is "road trip". |
| `satire` | Keyword is "satire". |
| `biopic` | Keyword is "biography". |
| `conspiracy` | Keyword is "conspiracy". |
| `addiction` | Keyword is "addiction". |
| `survival` | Keyword is "survival". |
| `courtroom-drama`| Keyword is "courtroom drama". |
| `political-thriller`| Keyword is "political thriller". |
| `robots-androids`| Keyword is "robot" or "android". |
| `virtual-reality`| Keyword is "virtual reality". |
| `alternate-history`| Keyword is "alternate history". |
| `magic` | Keyword is "magic". |
| `mythology` | Keyword is "mythology". |
| `car-chase` | Keyword is "car chase". |
| `buddy-cop` | Keyword is "buddy cop". |

#### Sub-Category: Based on Source Material

| Desired Tag | Automation Logic (TMDb) |
| :--- | :--- |
| `based-on-a-book`| Keyword is "based on book". |
| `based-on-comic`| Keyword is "based on comic". |
| `based-on-video-game`| Keyword is "based on video game". |
| `based-on-play` | Keyword is "based on play". |
| `based-on-true-story`| Keyword is "based on true story". |

#### Sub-Category: Horror Sub-Genres
*(Apply only to your "Horror" library)*

| Desired Tag | Automation Logic (TMDb) |
| :--- | :--- |
| `slasher` | Keyword is "slasher". |
| `supernatural`| Keyword is "supernatural". |
| `psychological`| Often tagged with the "psychological thriller" keyword. |
| `monster` | Keyword is "monster" or "creature feature". |
| `body-horror` | Keyword is "body horror". |
| `zombie` | Keyword is "zombie". |
| `vampire` | Keyword is "vampire". |
| `werewolf` | Keyword is "werewolf". |
| `ghost` | Keyword is "ghost". |
| `folk-horror` | Keyword is "folk horror". |
| `cosmic-horror`| Keyword is "cosmic horror". |
| `gothic` | Keyword is "gothic". |

#### Sub-Category: Documentary Types
*(Apply only to your "Documentary" library)*

| Desired Tag | Automation Logic (TMDb) |
| :--- | :--- |
| `docu-nature` | Keyword is "nature" or "animal". |
| `docu-history` | Genre is "History". |
| `docu-people` | Keyword is "biography". |
| `docu-events` | Keyword relates to specific historical events. |
| `docu-science` | Keyword is "science" or "technology". |
| `true-crime` | Keyword is "true crime". |
| `docu-sports` | Keyword is "sports". |
| `docu-music` | Keyword is "music" or "concert film". |
| `docu-political`| Keyword is "politics". |