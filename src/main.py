#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V3
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import requests
import json
from flask import Flask, request, render_template

from dotenv import load_dotenv
load_dotenv()
GH_USER = os.getenv('GH_USER')
GH_TOKEN = os.getenv('GH_PAT')

epd = epd2in13_V3.EPD()
epd.init()
epd.Clear(0xFF)
font = ImageFont.truetype(os.path.join(picdir, 'alliance.otf'), 24)
fontsmall = ImageFont.truetype(os.path.join(picdir, 'alliance.otf'), 14)
time_image = Image.new('1', (epd.height, epd.width), 255)
time_draw = ImageDraw.Draw(time_image)

try:
    app = Flask(__name__)

    @app.route('/')
    def my_form():
        return render_template('form.html')

    @app.route('/', methods=['POST'])
    def my_form_post():
        text = request.form['text']
        r = requests.get('https://api.github.com/users/' + text, auth=(GH_USER, GH_TOKEN))
        if r.status_code == 404:
            time_draw.rectangle((10, 10, 250, 105), fill = 255, width=300)
            time_draw.text((10, 10), '404 - user not found', font = font, fill = 0)
            epd.display(epd.getbuffer(time_image))
            return render_template('form.html')
        elif r.status_code == 200:
            pass
        time_draw.rectangle((10, 10, 220, 105), fill = 255, width=300)
        time_draw.text((10, 10), r.json()['login'], font = font, fill = 0)
        if r.json()['bio'] is None:
            time_draw.text((10, 36), 'bio empty', font = fontsmall, fill = 0)
        else:
            time_draw.text((10, 34), 'bio: ' + str(r.json()['bio']), font = fontsmall, fill = 0)
        epd.display(epd.getbuffer(time_image))
        return render_template('form.html')

    app.run(port=5007, host="0.0.0.0")

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd.init()
    epd.Clear(0xFF)
    epd.sleep()
    exit()