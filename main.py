# -*- coding: utf-8 -*-
import os
import RssNewsParser
import logging
from flask import Flask


app = Flask(__name__)
@app.route('/')
def parse_news():
    RssNewsParser.read_file('news.db', '/tmp/news.db')
    # 建立資料庫
    conn = RssNewsParser.open_or_create_db('/tmp/news.db')
    pts = RssNewsParser.PTS_parser(conn)
    msg = pts.fetch_and_push_data()
    RssNewsParser.close_db(conn)
    # 寫回 cloud storage
    with open('/tmp/news.db', 'rb') as fin:
        RssNewsParser.upload_file(fin.read(), 'news.db', 'application/x-sqlite3')
    os.remove('/tmp/news.db')
    return msg



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
