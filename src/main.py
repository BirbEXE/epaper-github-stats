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
from urllib.request import urlopen
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
fontmedium = ImageFont.truetype(os.path.join(picdir, 'alliance.otf'), 16)
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
        rj = r.json()
        if r.status_code == 404:
            time_draw.rectangle((10, 10, 250, 105), fill = 255, width=300)
            time_draw.text((10, 10), '404 - user not found', font = font, fill = 0)
            epd.display(epd.getbuffer(time_image))
            return render_template('form.html')
        elif r.status_code == 200:
            pass
        time_draw.rectangle((0, 0, 250, 122), fill = 255, width=300)
        time_draw.text((10, 10), rj['login'], font = font, fill = 0)
        if rj['bio'] is None:
            time_draw.text((10, 36), 'bio empty', font = fontsmall, fill = 0)
        else:
            time_draw.text((10, 36), 'bio: ' + str(rj['bio']), font = fontsmall, fill = 0)
        time_draw.text((10, 58), 'followers: ' + str(rj['followers']), font = fontmedium, fill = 0)
        time_draw.text((10, 76), 'public repos: ' + str(rj['public_repos']), font = fontmedium, fill = 0)
        time_draw.text((10, 94), 'public gists: ' + str(rj['public_gists']), font = fontmedium, fill = 0)
        avatarurl = rj['avatar_url']
        avatar = Image.open(urlopen(avatarurl))
        avatar.convert('1')
        avatar = avatar.resize((40, 40))
        time_image.paste(avatar, (208, 80))
        epd.display(epd.getbuffer(time_image))
        return render_template('form.html')

    app.run(port=5007, host="0.0.0.0")

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd.init()
    epd.Clear(0xFF)
    epd.sleep()
    exit()