# -*- coding: utf-8 -*-
import re
import feedparser
import os
from datetime import datetime
from pytube import YouTube # 下載 youtube 聲音
from RssNewsParser.db import insert_record
from RssNewsParser.storage import upload_file

class PTS_parser:
    def __init__(self, conn):
        self.conn = conn # sql connection
        self.tag_re = re.compile(r'<[^>]+>') # 移除tag
        self.space_re = re.compile(r'\s') # 移除看不到的符號
        self.bracket_re = re.compile(r'\([^>]+\)') # 移除小括號內的文字，因為不會被念出來

    def text_preprocess(self, str):
        text = self.tag_re.sub('', str)
        text = self.space_re.sub('', text)
        text = self.bracket_re.sub('', text)
        return text

    def fetch_and_push_data(self):
        msg = []
        docs = feedparser.parse('https://about.pts.org.tw/rss/XML/newsfeed.xml')
        for doc in docs.entries:
            title = doc.title_detail['value']
            content = doc.summary_detail['value']
            date = datetime.strptime(doc.published, '%a, %d %b %Y 00:00:00 +0800').strftime('%Y-%m-%d')
            match = re.search('http://img.youtube.com/vi/(\w+)/mqdefault.jpg', content)
            content = self.text_preprocess(content)

            if not match:
                ###　沒有影片就略過
                continue
            youtube_key = match.group(1)
            yt = YouTube('http://youtube.com/watch?v=%s' % (youtube_key))
            if re.search('公視晚間新聞', yt.title):
                output_key = "PTSN_%s_%s" % (date, youtube_key)
                source = 'PTSN'
            elif re.search('公視早安新聞',yt.title):
                output_key = "PTSD_%s_%s" % (date, youtube_key)
                source = 'PTSD'
            elif re.search('', yt.title):
                output_key = "PTSG_%s_%s" % (date, youtube_key)
                source = 'PTSG'
            else:
                continue
            msg.append(yt.title)
            ### save data
            try:
                insert_record(self.conn, output_key, source, date, content, 'pts/audio/%s.mp4' % (output_key), youtube_key)
            except:
                continue
            yt.streams.filter(only_audio=True, subtype='mp4').order_by('resolution').desc().first().download(output_path='/tmp', filename='%s' % (output_key))
            wave = '/tmp/%s.mp4' % (output_key)
            with open(wave, 'rb') as fin:
                upload_file(fin.read(), 'pts/audio/%s.mp4' % (output_key), 'audio/mp4')
            os.remove(wave)
        return "\n".join(msg)
