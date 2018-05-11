# -*- coding: utf-8 -*-
import os
import RssNewsParser
from flask import Flask


app = Flask(__name__)
@app.route('/')
def parse_news():
    RssNewsParser.read_file('news.db', '/tmp/news.db')
    # 建立資料庫
    conn = RssNewsParser.open_or_create_db('/tmp/news.db')
    pts = RssNewsParser.PTS_parser(conn)
    pts.fetch_and_push_data()
    RssNewsParser.close_db(conn)
    # 寫回 cloud storage
    with open('/tmp/news.db', 'rb') as fin:
        RssNewsParser.upload_file(fin.read(), 'news.db', 'application/x-sqlite3')
    os.remove('/tmp/news.db')



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
