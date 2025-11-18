# Trakt Lists Resources for Kometa

This document contains useful resources for finding Trakt lists to use with Kometa (Jellyfin Meta Manager) for creating automated collections.

## Community Resources

### Trakt.tv Official Community Lists

**Trakt Community Lists - TV Shows**
- **URL:** https://trakt.tv/shows/community/lists
- **Description:** Trakt's official community lists page for TV shows. Browse thousands of curated lists organized by popularity, reactions, comments, and update date. Lists include top-rated shows, genre collections, decade lists, and more.
- **Use Case:** Perfect for finding popular, well-maintained Trakt lists to use in Kometa. You can sort by popularity, reactions, or number of items to find the best lists.
- **Examples from the page:**
  - Trakt: Popular TV Shows (250 items, 821 likes)
  - Top 100 TV Comedy Shows (99 items, 138 likes)
  - BBC Culture - The 100 greatest TV series of the 21st Century (100 items, 98 likes)
  - Rolling Stone's 100 Best Sitcoms of All Time (100 items, 70 likes)

**Note:** Trakt also has community lists for movies at https://trakt.tv/movies/community/lists

### Reddit

**My Trakt Lists - Useful for Kodi Addons**
- **URL:** https://www.reddit.com/r/Addons4Kodi/comments/116961i/my_trakt_lists_hopefully_they_will_be_useful_for/
- **Description:** A comprehensive Reddit post containing a collection of Trakt lists organized by genre, mood, and theme. These lists are curated by the community and are perfect for use with Kometa to create automated collections in Jellyfin.
- **Use Case:** Browse through the lists mentioned in the post to find ones that match your preferences, then add them to your Kometa configuration.

## How to Use Trakt Lists in Kometa

### Step 1: Find a Trakt List

1. Visit the Reddit post or browse Trakt.tv
2. Find a list that matches what you want (e.g., "Feel Good Movies", "Mind-Bending Films", etc.)
3. Copy the list URL (e.g., `https://trakt.tv/users/USERNAME/lists/list-name`)

### Step 2: Add to Kometa Config

Add the list to your `config/movies.yml` file:

```yaml
collections:
  Feel Good Movies:
    trakt_list: https://trakt.tv/users/USERNAME/lists/feel-good-movies
    collection_order: release
  
  Mind-Bending Movies:
    trakt_list: https://trakt.tv/users/USERNAME/lists/mind-bending
    collection_order: release
  
  Date Night Movies:
    trakt_list: https://trakt.tv/users/USERNAME/lists/date-night
    collection_order: release
```

### Step 3: Run Kometa

```bash
cd ~/kometa
jellyfin-meta-manager
```

Kometa will:
- Connect to Trakt
- Read the list
- Create a collection in Jellyfin with all movies from that list
- Update the collection automatically when you run Kometa

## Creating Your Own Trakt Lists

You can also create your own lists on Trakt.tv:

1. Sign up for a free account at [Trakt.tv](https://trakt.tv)
2. Create a list (e.g., "My Favorite Action Movies")
3. Add movies to the list
4. Use the list URL in your Kometa config

## Tips

- **Public Lists:** Use public lists from the community - they're often well-maintained and updated regularly
- **Private Lists:** Create private lists for your personal curation (e.g., "Movies to Watch with Mom")
- **Collection Ordering:** Use `collection_order: release` for chronological order, or `collection_order: alphabetical` for alphabetical
- **Multiple Lists:** You can add as many Trakt lists as you want - each will become a separate collection in Jellyfin

## Additional Resources

- [Trakt.tv Official Website](https://trakt.tv)
- [Kometa Documentation - Trakt Lists](https://kometa.wiki/en/latest/)
- [Trakt API Documentation](https://trakt.docs.apiary.io/)

