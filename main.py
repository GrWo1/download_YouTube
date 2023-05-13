import google.oauth2.credentials
import os
import requests

from dotenv import load_dotenv
from googleapiclient.discovery import build
from pytube import YouTube


load_dotenv()


class CheckYoutube:

    YOUTUBE_API = os.getenv('YOUTUBE_API')  # Ключи API, полученные на Google Console

    CHANNEL_NAME = 'Деньги не спят'  # Имя канала
    QUERY = 'Валютные качели: куда улетит рубль'  # Название видео на канале

    def __int__(self, url_image, video_response):
        self.url_image = url_image
        self.video_response = video_response

    def connect_youtube(self):
        """Авторизация с помощью API ключа. Получение ID канала по его имени.
        Получение списка видео."""

        youtube = build('youtube', 'v3', developerKey=self.YOUTUBE_API)
        channel_request = youtube.channels().list(
            part='id',
            forUsername=self.CHANNEL_NAME,
        )
        channel_response = channel_request.execute()
        # channel_id = channel_response['items'][0]['id']
        search_request = youtube.search().list(
            part='id',
            # channelId=self.channel_id,
            q=self.QUERY,
            type='video',
        )
        search_response = search_request.execute()
        video_id = search_response['items'][0]['id']['videoId']
        video_request = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id
        )
        self.video_response = video_request.execute()
        self.url_image = self.video_response['items'][0]['snippet']['thumbnails']['maxres']['url']
        return self.video_response

    def get_image_video(self):
        """Сохраняем изображение видео в папку /images/{название канала}."""

        title = self.video_response['items'][0]['snippet']['title']
        title = title.replace('/', '|')
        folder_path = f'./images/{self.CHANNEL_NAME}'
        os.mkdir(folder_path)
        filename = os.path.join("./images", f'{self.CHANNEL_NAME}', f"{title}.png")
        image = requests.get(self.url_image)
        with open(filename, "wb") as f:
            f.write(image.content)
    # # Вывод метаданных для первого видео в результате поиска
    # print('Title:', video_response['items'][0]['snippet']['title'])
    # print('Description:', video_response['items'][0]['snippet']['description'])
    # print('Duration:', video_response['items'][0]['contentDetails']['duration'])
    # print('Views:', video_response['items'][0]['statistics']['viewCount'])


if __name__ == '__main__':
    response = CheckYoutube()
    content = response.connect_youtube()
    print('Название:', content['items'][0]['snippet']['title'])
    print('Описание:', content['items'][0]['snippet']['description'])
    response.get_image_video()
