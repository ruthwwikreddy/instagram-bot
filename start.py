import instaloader
import time
import random
import os
import csv

# === Setup ===
USERNAME_TO_SCRAPE = "choesen_133"
SESSION_ID = "58396807841%3ABWkeciRKaUP9hA%3A5%3AAYdZ5RV4ED4RxKoiDpkBeAfrRFeMvKLxoY9cAdyW7w"

# === Initialize Instaloader ===
L = instaloader.Instaloader(download_pictures=True, download_videos=True, download_video_thumbnails=True,
                             download_geotags=True, save_metadata=True, compress_json=False)

# === Load session manually ===
L.context._session.cookies.set('sessionid', SESSION_ID, domain='.instagram.com')
print("[*] Loaded session successfully!")

# === Scrape Profile ===
try:
    profile = instaloader.Profile.from_username(L.context, USERNAME_TO_SCRAPE)
    print(f"[*] Accessing profile @{USERNAME_TO_SCRAPE}...")
except Exception as e:
    print(f"[!] Failed to access profile: {e}")
    exit(1)

# === Basic Profile Info ===
print("\n--- Profile Info ---")
print(f"Username      : {profile.username}")
print(f"Full Name     : {profile.full_name}")
print(f"Bio           : {profile.biography}")
print(f"External URL  : {profile.external_url}")
print(f"Followers     : {profile.followers}")
print(f"Following     : {profile.followees}")
print(f"Posts         : {profile.mediacount}")
print(f"Is Private    : {profile.is_private}")

print("--------------------\n")

# === Create Output Folder ===
if not os.path.exists(USERNAME_TO_SCRAPE):
    os.makedirs(USERNAME_TO_SCRAPE)

# === CSV Setup for Saving Post Data ===
csv_file = open(f"{USERNAME_TO_SCRAPE}/posts_data.csv", mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Shortcode", "Caption", "Date", "Likes", "Comments", "URL", "Is Video", "Is Carousel"])

# === Scrape Posts ===
print(f"[*] Scraping posts from @{USERNAME_TO_SCRAPE}...")
count = 0

for post in profile.get_posts():
    count += 1
    print(f"[+] Downloading Post {count}: {post.shortcode}")
    
    # Save post info into CSV
    csv_writer.writerow([
        post.shortcode,
        post.caption.replace('\n', ' ') if post.caption else "",
        post.date_utc.strftime("%Y-%m-%d %H:%M:%S"),
        post.likes,
        post.comments,
        f"https://www.instagram.com/p/{post.shortcode}/",
        post.is_video,
        post.typename == "GraphSidecar"  # True if it's a carousel (multiple photos/videos)
    ])
    
    # Download actual post
    try:
        L.download_post(post, target=USERNAME_TO_SCRAPE)
    except Exception as e:
        print(f"[!] Failed to download post {count}: {e}")

    time.sleep(random.randint(2, 5))

csv_file.close()

print(f"\n[*] Finished downloading {count} posts and saved CSV data.")

# === Scrape Reels ===
print(f"[*] Scraping reels (short videos) from @{USERNAME_TO_SCRAPE}...")

reel_folder = f"{USERNAME_TO_SCRAPE}_reels"
if not os.path.exists(reel_folder):
    os.makedirs(reel_folder)

for reel in profile.get_igtv_posts():
    print(f"[+] Downloading Reel: {reel.shortcode}")
    try:
        L.download_post(reel, target=reel_folder)
    except Exception as e:
        print(f"[!] Failed to download reel: {e}")
    time.sleep(random.randint(2, 5))

# === Scrape Story Highlights ===
print(f"[*] Scraping highlights from @{USERNAME_TO_SCRAPE}...")

for highlight in profile.get_highlights():
    print(f"[+] Highlight: {highlight.title}")
    for item in highlight.get_items():
        try:
            L.download_storyitem(item, target=f"{USERNAME_TO_SCRAPE}_highlights")
        except Exception as e:
            print(f"[!] Failed to download highlight item: {e}")
        time.sleep(random.randint(2, 4))

# === Scrape Current Active Stories (if public) ===
print(f"[*] Scraping active stories from @{USERNAME_TO_SCRAPE}...")

try:
    for story in L.get_stories(userids=[profile.userid]):
        for item in story.get_items():
            try:
                L.download_storyitem(item, target=f"{USERNAME_TO_SCRAPE}_stories")
            except Exception as e:
                print(f"[!] Failed to download story item: {e}")
            time.sleep(random.randint(1, 3))
except Exception as e:
    print(f"[!] Could not fetch active stories: {e}")

# === Scrape Tagged Posts ===
print(f"[*] Scraping posts where @{USERNAME_TO_SCRAPE} is tagged...")

try:
    for post in profile.get_tagged_posts():
        print(f"[+] Downloading Tagged Post: {post.shortcode}")
        try:
            L.download_post(post, target=f"{USERNAME_TO_SCRAPE}_tagged")
        except Exception as e:
            print(f"[!] Failed to download tagged post: {e}")
        time.sleep(random.randint(2, 5))
except Exception as e:
    print(f"[!] Could not fetch tagged posts: {e}")

print("\n[*] Full scraping completed successfully!")

