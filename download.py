from __future__ import unicode_literals
import youtube_dl
import os
import json
import psycopg2
import database


PATH_justDownloaded = os.path.abspath('/'.join(os.getcwd().split('/')[:-1]) + '/resources/downloaded')


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print(f'Done downloading - {d["total_bytes"]}')


selected_database = database.videos_database

conn = mysql.connector.connect(host=selected_database.url,
                               database=selected_database.database_name,
                               user=selected_database.user_name,
                               password=selected_database.password,
                               port=selected_database.port)

cur = conn.cursor()

# Description of ydl_opts:
# https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
ydl_opts = {
    'format': 'best',
    'outtmpl': PATH_justDownloaded + '/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s',
    # 'postprocessors': [{
    #     'key': 'FFmpegExtractAudio',
    #     'preferredcodec': 'mp3',
    #     'preferredquality': '192',
    # }],
    'ignoreerrors': 'True',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}


def clear_string(string):
    if string is None:
        return ""
    else:
        return string.replace("\"", "").replace("\'", "")


with open('../resources/links.txt', 'r') as file:
    urls = [x.replace('\n', '') for x in file.readlines()]

x = []

query = f'INSERT INTO videos (title, owner, description, file_name, source, video_url, downloaded, videoStorage_id, path, length, fps, resolution_W, resolution_H, geo_coordinates_W, geo_coordinates_H, recording_date, upload_date, quality, tags) VALUES '
for url in urls:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        if info_dict.get('entries'):
            for entry in info_dict.get('entries'):
                query = query + f'("{clear_string(entry.get("title"))}","{entry.get("uploader_url")}", "{clear_string(entry.get("description")).encode("ascii", "ignore")}", "{entry.get("playlist_index")} - {clear_string(entry.get("title"))}.{entry.get("ext")}", "{entry.get("extractor")}", "{entry.get("video_url")}", 1, 1, "{PATH_justDownloaded}", "{entry.get("duration")}", "{entry.get("fps")}", "{entry.get("width")}", "{entry.get("height")}", 2.3, 2.3, "recording_date", "{entry.get("upload_date")}", "{entry.get("quality")}", "tags"),'

            for entry in info_dict.get('entries'):
                if entry:
                    with open(f'../resources/jsons/{entry.get("uploader_id")}_{entry.get("id")}.json',
                              "w") as json_file:
                        json_file.write(json.dumps(entry))

query1 = query[:-1] + ';'
cur.execute(query1)
conn.commit()
conn.close()
