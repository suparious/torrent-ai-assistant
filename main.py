from icecream import ic
import feedparser
import requests
import json
import re
import os
import time

with open('config.json', 'r') as f:
    config = json.load(f)

rss_urls_tvshows = [entry['url'] for entry in config['rss_urls_tvshows']]
rss_urls_books = [entry['url'] for entry in config['rss_urls_books']]
keywords_tvshows = config['keywords_tvshows']
output_default = config['output_default']
output_tvshows = config['output_tvshows']
output_movies = config['output_movies']
output_books = config['output_books']

def sanitize_filename(filename):
    # Replace any characters that are not allowed in Windows file names
    return "".join([c for c in filename if c.isalnum() or c in " ._-"])

def download_torrent(url, filename, torrent_type):
    safe_filename = sanitize_filename(filename)
    ic(url, filename, torrent_type)
    r = requests.get(url, allow_redirects=True)
    if torrent_type == "tvshows":
        output = output_tvshows
    elif torrent_type == "movies":
        output = output_movies
    elif torrent_type == "books":
        output = output_books
    else:
        output = output_default
    if not os.path.exists(output):
        os.makedirs(output)
        ic(f"Created output folder: {output}")
    with open(os.path.join(output, safe_filename), 'wb') as f:
        f.write(r.content)

pattern = re.compile(r'S(\d{2})E(\d{2})')

for rss_url in rss_urls_tvshows:
    response = requests.get(rss_url)
    ic(response.status_code)
    feed = feedparser.parse(rss_url, agent='Mozilla/5.0')
    ic(feed.bozo)
    if feed.bozo:
        ic(feed.bozo_exception)
    ic(len(feed.entries))

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        matching_keyword = next((kw for kw in keywords_tvshows if kw in title), None)
        if matching_keyword:
            season_episode_match = pattern.search(title)
            if season_episode_match:
                ic(title)
                season, episode = season_episode_match.groups()
                unique_id = f"{matching_keyword}_S{season}_E{episode}"
                torrent_type = "tvshows"
                download_torrent(link, f"{unique_id}.torrent", torrent_type)
            time.sleep(2)

## For feeds where all entries should be downloaded
#for rss_url in rss_urls_books:
#    response = requests.get(rss_url)
#    ic(response.status_code)
#    feed = feedparser.parse(rss_url, agent='Mozilla/5.0')
#    ic(feed.bozo)
#    if feed.bozo:
#        ic(feed.bozo_exception)
#    ic(len(feed.entries))
#
#    for entry in feed.entries:
#        title = entry.title
#        link = entry.link
#        torrent_type = "books"
#        download_torrent(link, f"{title}.torrent", torrent_type)
#        time.sleep(2)
