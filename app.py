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
import pycps
from hashlib import sha512
import urllib2, urllib, json
#---------------------------------------------------------------------------

from tornado.options import define, options, parse_command_line
#define('port',address='0.0.0.0',default=8888,type=int)


#---------------------------------------------------------------------------

#clusterpoint APIS

# head = {
#     "Authorization":"Basic bGVvcGFuaWdyYWhpQGdtYWlsLmNvbToyM2xlbzIz"
# }
# url = "https://api-us.clusterpoint.com/100629/zeno/_search.json"
# values = dict(query='abhilash')
# r = requests.post(url,data=json.dumps(values), headers=headers)
# print r.content


#-------------------------------------------------------
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        if (self.get_secure_cookie('user')):
            self.redirect('/home')
        else:
            self.render('index.html')

#Login Handlers----------------------------------------
class CollegeLoginHandler(tornado.web.RequestHandler):
    def post(self):
        username = re.escape(self.get_argument("u"))
        rawPassword = re.escape(self.get_argument("p"))
        #Processing password
        m = hashlib.md5()
        m.update(rawPassword)
        password = m.hexdigest()
        #We have username and password. Now verify using clusterpoint
        url = "https://api-us.clusterpoint.com/100629/college/_search.json"
        headers = {"Authorization":"Basic bGVvcGFuaWdyYWhpQGdtYWlsLmNvbToyM2xlbzIz"}
        string = "<u>"+username+"</u><p>"+password+"</p>"
        values = dict(query=string)
        r = requests.post(url,data=json.dumps(values), headers=headers)
        responseDict = json.loads(r.content)
        if responseDict['documents'] is not None:
            collegeID = responseDict['documents'][0]['u']
            self.set_secure_cookie('college', collegeID)
            self.redirect('/collegehome')
        else:
            self.redirect('/')

class StudentLoginHandler(tornado.web.RequestHandler):
    def post(self):
        username = re.escape(self.get_argument("u"))
        rawPassword = re.escape(self.get_argument("p"))
        #Processing password
        m = hashlib.md5()
        m.update(rawPassword)
        password = m.hexdigest()
        #We have username and password. Now verify using clusterpoint
        url = "https://api-us.clusterpoint.com/100629/student/_search.json"
        headers = {"Authorization":"Basic bGVvcGFuaWdyYWhpQGdtYWlsLmNvbToyM2xlbzIz"}
        string = "<regno>"+username+"</regno><pwd>"+password+"</pwd>"
        values = dict(query=string)
        r = requests.post(url,data=json.dumps(values), headers=headers)
        responseDict = json.loads(r.content)
        if responseDict['documents'] is not None:
            studentID = responseDict['documents'][0]['regno']
            self.set_secure_cookie('student', studentID)
            self.redirect('/studenthome')
        else:
            self.redirect('/')

class CompanyLoginHandler(tornado.web.RequestHandler):
    def post(self):
        username = re.escape(self.get_argument("u"))
        rawPassword = re.escape(self.get_argument("p"))
        #Processing password
        m = hashlib.md5()
        m.update(rawPassword)
        password = m.hexdigest()
        #We have username and password. Now verify using clusterpoint
        url = "https://api-us.clusterpoint.com/100629/company/_search.json"
        headers = {"Authorization":"Basic bGVvcGFuaWdyYWhpQGdtYWlsLmNvbToyM2xlbzIz"}
        string = "<id>"+username+"</id><pwd>"+password+"</pwd>"
        values = dict(query=string)
        r = requests.post(url,data=json.dumps(values), headers=headers)
        responseDict = json.loads(r.content)
        if responseDict['documents'] is not None:
            companyID = responseDict['documents'][0]['id']
            self.set_secure_cookie('company', companyID)
            self.redirect('/companyhome')
        else:
            self.redirect('/')



            

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
    (r'/collegelogin',CollegeLoginHandler),

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
