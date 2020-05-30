#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on May 29, 2020
Desc: Twitter HTML parser
Author: Mashiro 
URL: https://2heng.xin
License: MIT
"""
from bs4 import BeautifulSoup
from .get_config import GetConfig

config = GetConfig()

def TweetDecoder(rss_data):
  """
  :params object: Summary from FeedParaser
  :return object
  """
  soup = BeautifulSoup(rss_data['summary'], features='html.parser')

  data = {
      'gif': [],
      'gif_poster': [],
      'video': [],
      'video_poster': [],
      'image': [],
      'plain': None
  }

  for link in soup.find_all('a'):
    link.replace_with(' ' + link.get('href') + ' ')

  for video in soup.find_all('video'):
    # print(video.get('src'))
    if ('https://video.twimg.com/tweet_video' in video.get('src')):
      data['gif'].append(video.get('src'))
      data['gif_poster'].append(video.get('poster'))
      video.replace_with('')
    if ('https://video.twimg.com/ext_tw_video' in video.get('src')):
      data['video'].append(video.get('src'))
      data['video_poster'].append(video.get('poster'))
      video.replace_with('')
    if ('https://video.twimg.com/amplify_video' in video.get('src')):
      data['video'].append(video.get('src'))
      data['video_poster'].append(video.get('poster'))
      video.replace_with('')

  for image in soup.find_all('img'):
    # print(video.get('src'))
    data['image'].append(image.get('src'))
    image.replace_with('')

  for br in soup.find_all('br'):
    br.replace_with('\n')

  # print(soup.prettify())
  # print(str(data))
  data['plain'] = soup.prettify() + '\n'+config['MASTODON']['TweetSourcePrefix']+' ' + rss_data['link']
  return data 

if __name__ == '__main__':
  test_normal = """
流程图工具 Excalidraw 可以做出下面这样的图示效果，可惜中文没有手写效果。<a href="https://excalidraw.com/" target="_blank" rel="noopener noreferrer">https://excalidraw.com/</a><a href="https://2heng.xin/" target="_blank" rel="noopener noreferrer">https://2heng.xin/</a><br><img src="https://pbs.twimg.com/media/EZJh5RPUMAEz4aS?format=jpg&name=orig" referrerpolicy="no-referrer"><img src="https://s3-view.2heng.xin/aws_cached/2019/07/14/53c2adbc381e3aa17968d5d36feee002.md.png" referrerpolicy="no-referrer"><img src="https://s3-view.2heng.xin/aws_cached/2020/05/19/b1a7d8ff391616ad152f9958c6302ba0.md.jpg" referrerpolicy="no-referrer"><img src="https://s3-view.2heng.xin/aws_cached/2020/05/18/671a82563dfe40885196166683bf6f0b.md.jpg" referrerpolicy="no-referrer">
"""

  test_gif = """
【Vitafield Rewilder Series - Wilted Cypress - Firewatch】<br><br>Now available at the Store until June 10, 03:59(UTC-7)!<br><br>#Arknights #Yostar <br><video src="https://video.twimg.com/tweet_video/EZLxKmTUMAARbSa.mp4" autoplay loop muted webkit-playsinline playsinline controls="controls" poster="https://pbs.twimg.com/tweet_video_thumb/EZLxKmTUMAARbSa.jpg" style="width: 100%"></video>
"""

  test_video = """
Arknights Official Trailer – Code of Brawl<br><br>"Doctor, relying on me isn't a very wise decision"<br><br>HD version: <br><br>#Arknights #Yostar <a href="http://youtu.be/SJ1qvqEmkVQ" target="_blank" rel="noopener noreferrer">http://youtu.be/SJ1qvqEmkVQ</a><br><video src="https://video.twimg.com/ext_tw_video/1265470079203827712/pu/vid/1280x720/B-BRCBM0djUAqJl0.mp4?tag=10" controls="controls" poster="https://pbs.twimg.com/ext_tw_video_thumb/1265470079203827712/pu/img/VujsmqbQORfHDeCP.jpg" style="width: 100%"></video>
"""
  print(TweetDecoder(test_video))