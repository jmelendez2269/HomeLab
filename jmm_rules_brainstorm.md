# Jellyfin Meta Manager (JMM) Rules Brainstorm

This document contains a comprehensive list of potential tags you can automate using Jellyfin Meta Manager (JMM). Use this as a blueprint for building your `movies.yml` configuration file.

---

## Automation Methods

There are two primary methods we'll use to automate tags:

1.  **Trakt Lists (For Subjective Tags):** For personal, thematic, or mood-based tags, the best approach is to create a public list on [Trakt.tv](https://trakt.tv/). You give the list a name (e.g., "Date Night") and add movies to it. JMM then reads this list and applies a tag of your choice (e.g., `date-night`) to those movies in Jellyfin. This gives you full manual control over subjective categories.

2.  **TMDb Data (For Objective Tags):** For factual tags, JMM can pull data directly from TheMovieDB (TMDb). This is perfect for tagging based on official genres, keywords, release dates, awards, etc.

---

## Tag Ideas & Automation Logic

### Category 1: Subjective & Thematic Tags
**(Recommended Method: Trakt List)**

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

### Category 2: Objective & Factual Tags
**(Recommended Method: TMDb Data)**

#### Sub-Category: Genre, Medium & Era

| Desired Tag | Automation Logic (TMDb) |
| :--- | :--- |
| `animation` | Genre is "Animation". |
| `anime` | Keyword is "anime". |
| `live-action` | Genre is NOT "Animation". |
| `based-on-a-book`| Keyword is "based on book". |
| `based-on-comic`| Keyword is "based on comic". |
| `based-on-video-game`| Keyword is "based on video game". |
| `oscar-winner` | Award information indicates a "Best Picture" Oscar win. |
| `golden-globe-winner`| Award information indicates a "Best Motion Picture" Golden Globe win. |
| `70s` | Release year is between 1970-1979. |
| `80s` | Release year is between 1980-1989. |
| `90s` | Release year is between 1990-1999. |
| `2000s` | Release year is between 2000-2009. |
| `2010s` | Release year is between 2010-2019. |
| `2020s` | Release year is between 2020-2029. |

#### Sub-Category: Topics & Keywords

| Desired Tag | Automation Logic (TMDb) |
| :--- | :--- |
| `money` | Keyword is "money", "wall street", or "finance". |
| `dystopian` | Keyword is "dystopia". |
| `cyberpunk` | Keyword is "cyberpunk". |
| `post-apocalyptic`| Keyword is "post-apocalyptic". |
| `time-travel` | Keyword is "time travel". |
| `space-travel`| Keyword is "space travel". |
| `alien-invasion`| Keyword is "alien invasion". |
| `heist` | Keyword is "heist". |
| `mockumentary`| Keyword is "mockumentary". |
| `found-footage`| Keyword is "found footage". |
| `spy` | Keyword is "spy". |
| `disaster` | Keyword is "disaster". |
| `martial-arts`| Keyword is "martial arts". |
| `superhero` | Keyword is "superhero". |
| `film-noir` | Keyword is "film noir". |

#### Sub-Category: Documentary Types
*(These rules should be applied only to your "Documentary" library)*

| Desired Tag | Automation Logic (TMDb) |
| :--- | :--- |
| `docu-nature` | Keyword is "nature" or "animal". |
| `docu-history` | Genre is "History". |
| `docu-people` | Keyword is "biography". |
| `docu-events` | Keyword relates to specific historical events. |
| `docu-science` | Keyword is "science" or "technology". |
| `true-crime` | Keyword is "true crime". |
| `docu-sports` | Keyword is "sports". |

#### Sub-Category: Horror Sub-Genres
*(These rules should be applied only to your "Horror" library)*

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

---

This list should provide a fantastic starting point. You can now go through this file, remove any tags you don't want, and add any others you can think of.
