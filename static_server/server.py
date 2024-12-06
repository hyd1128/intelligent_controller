#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/5 17:32
# @Author : limber
# @desc :

import os

from flask import Flask, send_from_directory


current_dir = os.path.dirname(os.path.abspath(__file__))
static_file_path = os.path.join(current_dir, "static")
app = Flask(__name__, static_folder=static_file_path)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

def main():
    app.run(
        host="0.0.0.0",
        port=8041,
        debug=False
    )

if __name__ == '__main__':
    main()

