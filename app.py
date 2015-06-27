import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.websocket
import tornado.httpclient
from tornado import gen
import os.path
import json
import requests
import random
import tornado.escape
from hashlib import sha512
#---------------------------------------------------------------------------

from tornado.options import define, options, parse_command_line
#define('port',address='0.0.0.0',default=8888,type=int)


#---------------------------------------------------------------------------

# from pymongo import MongoClient
# client = MongoClient()
# db = client['angelhack']

#-------------------------------------------------------
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        if (self.get_secure_cookie('user')):
            self.redirect('/check')
        else:
            self.render('index.html')
        
            

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect('/')



#------------------------WEB SOCKET HANDLER-----------------------------
class WSHandler(tornado.websocket.WebSocketHandler):
     
    def open(self):
        pass
        # print("socket opened server side")
            
    def on_message(self, message):
        self.db = db
        messageFromClient = json.loads(message)
        messageType = str(messageFromClient['messageType'])
        if messageType == "verifyLoginDetails":
            pass            
            # print messageToClient

    def on_close(self):
        pass
        # print("Socket closed server side")

        
handlers = [
    (r'/',IndexHandler),
    (r'/logout',LogoutHandler)

]

#---------------------------------------------------------------------------

if __name__ == "__main__":
    parse_command_line()
    # template path should be given here only unlike handlers
    app = tornado.web.Application(handlers, template_path=os.path.join(os.path.dirname(__file__), "templates"),
                                  static_path=os.path.join(os.path.dirname(__file__), "static"), cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=", debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
