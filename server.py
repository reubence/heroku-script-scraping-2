# Paste your python program here
import datetime
import gspread
import pandas as pd
from instaloader import Instaloader, Profile
gc = gspread.service_account(filename='data/sheets-json-secret-key.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1pNg9FxXvoEHcE3QyyHKAn60hlg6WP69kAK3GXia1tQU/edit?usp=sharing')
L = Instaloader()

start_date = datetime.date(year=2020, month=8, day=1)
end_date = datetime.date(year=2020, month=8, day=31)
df = pd.read_csv('data/Page Rank Handles.csv', encoding='cp1252')
handles = df['Insta Handle'].dropna().tolist()
#s
rows = []
for handle in handles[49:]:
    print(handle)
    profile = Profile.from_username(L.context, handle)
    total_posts = 0
    for post in profile.get_posts():
        if end_date < post.date_utc.date():
            continue
        if post.date_utc.date() < start_date:
            break
        print(total_posts)
        rows.append([handle, ' '.join(post.caption_mentions), ' '.join(post.tagged_users)])
        total_posts += 1
insta = pd.DataFrame(rows, columns=['handle', 'mentions', 'tags'])
insta.to_csv('data/mentions_insta_july_2.csv', index=False)
worksheet = sh.get_worksheet(0)

worksheet.update([insta.columns.values.tolist()] + insta.values.tolist())
