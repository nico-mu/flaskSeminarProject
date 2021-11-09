#!/usr/bin/python
'''
Main Module for the app
'''
# Versions  Python   3.8.2
#           Flask    2.0.2



from flask import Flask
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

import demo.views
