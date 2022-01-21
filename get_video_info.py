import json
from pymediainfo import MediaInfo
import pandas as pd
from pathlib import Path
import os
import re
import numpy as np
pattern = re.compile(r'\.mp4')

root_path = './animal_video'
df = pd.read_csv('1.csv')
vedio_cnt = len(df)


oldpath = Path(root_path)
video_infos = []

for i in range(vedio_cnt):
    path = Path(root_path) / df['family'][i] / df['genus'][i] / df['keyword'][i] / df['action'][i].strip()
    path.mkdir(exist_ok=True, parents=True)
    if oldpath != path:
        oldpath = path
        filenames = [f for f in os.listdir(path)]
        for filename in filenames:
            if re.search(pattern, filename):
                video_id = filename.split('.')[0]
                file_path = os.path.join(path, filename)
                # print(file_path)
                media_info = MediaInfo.parse(file_path)
                data = media_info.to_json()
                data = json.loads(data)
                data = data['tracks']
                duration = data[0]['duration'] / 1000
                fps = data[0]['frame_rate']
                size = str(data[1]['height']) + "P"
                video_infos.append([video_id, size, fps, duration])

# df = pd.DataFrame(columns=["video_path", "resolution", "fps", "duration"], data=video_infos)
# df.to_csv('video_info.csv', index=True)


def merger_csv():
    df = pd.read_csv('1.csv')
    data_list = df.values
    temp = []
    for data in data_list:
        temp.append(np.hstack((data, search_info(data[-1]))))
    # print(np.array(df.columns))
    df = pd.DataFrame(columns=np.hstack((np.array(df.columns),["resolution", "fps", "duration"])), data=temp)
    df.to_csv('video_info_all.csv', index=True)


def search_info(video_path):
    for video_info in video_infos:
        if video_path in video_info:
            return video_info[1:]
    return []

merger_csv()
