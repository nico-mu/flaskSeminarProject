#!/usr/bin/env python3
'''
start the server
'''
from demo import app, socket

if __name__ == "__main__":
    socket.run(app)
