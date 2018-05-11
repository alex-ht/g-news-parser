# -*- coding: utf-8 -*-
import RssNewsParser

if __name__ == '__main__':
    # 建立資料庫
    conn = RssNewsParser.open_or_create_db('news.db')
    pts = RssNewsParser.PTS_parser(conn)
    pts.fetch_and_push_data()
    RssNewsParser.close_db(conn)
