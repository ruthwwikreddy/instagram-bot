# 📸 Instagram Scraper using Instaloader

This Python script scrapes Instagram data from any public or private profile using the `Instaloader` library.

---

## 🚀 Features

- Download all posts (images, videos, captions)
- Save post data to CSV
- Scrape private profiles using session ID
- Optional scraping for:
  - Reels (IGTV)
  - Highlights
  - Current Stories
  - Tagged posts

---

## 🔧 Requirements

- Python 3.7+
- Instaloader module

Install it using pip:

```bash
pip install instaloader
```

---

## ⚙️ Setup

1. Clone the Repository

```bash
git clone https://github.com/yourusername/instagram-scraper
cd instagram-scraper
```

2. Open `scraper.py` and update the following:

```python
USERNAME_TO_SCRAPE = "target_username"
SESSION_ID = "your_instagram_sessionid_here"
```

> 💡 You can find your `sessionid` by logging into Instagram via browser → open DevTools → Application → Cookies → Copy the `sessionid` value.

3. Run the Script

```bash
python scraper.py
```

---

## 📁 Output

- A folder named after the Instagram username will be created.
- All posts (images/videos) are downloaded.
- A CSV file (`posts_data.csv`) will contain metadata of all posts.
- Additional folders are created if optional features are enabled (e.g., `_reels`, `_highlights`).

---

## ✨ Optional Additional Features (Reels, Highlights, Stories, Tags)

You can enable these by modifying the last sections of the script:

```python
# Reels
for reel in profile.get_igtv_posts():
    L.download_post(reel, target=reel_folder)

# Highlights
for highlight in profile.get_highlights():
    for item in highlight.get_items():
        L.download_storyitem(item, target=highlight_folder)

# Active Stories
for story in L.get_stories(userids=[profile.userid]):
    for item in story.get_items():
        L.download_storyitem(item, target=story_folder)

# Tagged Posts
for post in profile.get_tagged_posts():
    L.download_post(post, target=tagged_folder)
```

---

## ⚠️ Disclaimer

- This script is for educational and personal use only.
- Scraping data from Instagram may violate their terms of service.
- Use responsibly and at your own risk.

---

## 🧑‍💻 Author

Made with ❤️ by [Ruthwik Reddy]
