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
import hashlib
from hashlib import sha512
import urllib2, urllib, json
import re
# from __future__ import print_function
from alchemyapi import AlchemyAPI
#---------------------------------------------------------------------------

from tornado.options import define, options, parse_command_line
#define('port',address='0.0.0.0',default=8888,type=int)


#---------------------------------------------------------------------------
#IBM Bluemix alchemy API

#alchemyapi = AlchemyAPI()
#response = alchemyapi.keywords('text', demo_text, {'sentiment': 1})
# for each in response['keywords']:
#     try:
#         print(each['relevance'])
#     except:
#         pass


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
class SelectLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')

class StudentHandler(tornado.web.RequestHandler):
    def get(self):
        if (self.get_secure_cookie('student')):
            self.redirect('/studenthome')
        else:
            self.render('studentlogin.html')

class CollegeHandler(tornado.web.RequestHandler):
    def get(self):
        if (self.get_secure_cookie('college')):
            self.redirect('/collegehome')
        else:
            self.render('collegelogin.html')

class CompanyHandler(tornado.web.RequestHandler):
    def get(self):
        if (self.get_secure_cookie('company')):
            self.redirect('companylogin.html')
        else:
            self.render('companylogin.html')

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
        url = "https://api-us.clusterpoint.com/100629/stud/_search.json"
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
#------------------------------------------------------------------

#Home-handlers----------------------------------------------------

class StudentHomeHandler(tornado.web.RequestHandler):
    def get(self):
        studentID = repr(self.get_secure_cookie('student'))
        studentID = studentID.split("'")
        studentID = str(studentID[1])
        if studentID:
            url = "https://api-us.clusterpoint.com/100629/stud/_search.json"
            headers = {"Authorization":"Basic bGVvcGFuaWdyYWhpQGdtYWlsLmNvbToyM2xlbzIz"}
            string = "<regno>"+studentID+"</regno>"
            values = dict(query=string)
            r = requests.post(url,data=json.dumps(values), headers=headers)
            responseDict = json.loads(r.content)
            if responseDict['documents'] is not None:
                name = responseDict['documents'][0]['name']['first'] + " " + responseDict['documents'][0]['name']['last']
                degree = responseDict['documents'][0]['degree']
                collegename = responseDict['documents'][0]['collegeName']
                phone = responseDict['documents'][0]['phone']
                email = responseDict['documents'][0]['email']
                summary = responseDict['documents'][0]['summary']
                researchAreas = [ each['t'] for each in responseDict['documents'][0]['tag'] if each['type'] == "research" ]
                projectAreas = [ each['t'] for each in responseDict['documents'][0]['tag'] if each['type'] == "project" ]
                gpa = responseDict['documents'][0]['gpa']
                graduating = responseDict['documents'][0]['graduating']
                experience = dict()
                for each in responseDict['documents'][0]['experience']:
                    experience[each['title']] = each['desc']
                allKeys = [ each['t'] for each in responseDict['documents'][0]['tag']]
                projects = dict()
                for each in responseDict['documents'][0]['project']:
                    each['title'] = each['verified']
                research=dict()
                for each in responseDict['documents'][0]['research']:
                    research[each['title']] = each['verified']
                jobs = list()
                url = "https://api-us.clusterpoint.com/100629/jobs/_search.json"
                string="*"
                values = dict(query=string)
                r = requests.post(url,data=json.dumps(values), headers=headers)
                alljobs = json.loads(r.content)
                jobs = alljobs['documents']

                self.render('studenthome.html',name=name,degree=degree,collegename=collegename,phone=phone,email=email,summary=summary,researchAreas=researchAreas, projectAreas=projectAreas,gpa=gpa,graduating=graduating,experience=experience,allKeys=allKeys, projects=projects, research=research,jobs=jobs)
            else:
                redirect('/')
        else:
            self.redirect('/')


class StudentAddsProjectHandler(tornado.web.RequestHandler):
    def post(self):
        studentID = repr(self.get_secure_cookie('student'))
        studentID = studentID.split("'")
        studentID = str(studentID[1])
        if studentID:
            title = re.escape(self.get_argument("title"))
            abstract = re.escape(self.get_argument("abstract"))
            url = "https://api-us.clusterpoint.com/100629/stud/_search.json"
            headers = {"Authorization":"Basic bGVvcGFuaWdyYWhpQGdtYWlsLmNvbToyM2xlbzIz"}
            string = "<regno>"+studentID+"</regno>"
            values = dict(query=string)
            r = requests.post(url,data=json.dumps(values),headers=headers)
            responseDict = json.loads(r.content)
            print responseDict
            projectCount = len(responseDict['documents'][0]['project'])
            responseDict['documents'][0]['project'].append({'abstract':abstract, 'title':title})
            url2update = "https://api-us.clusterpoint.com/100629/stud/_partial_replace.json"
            r = requests.put(url2update,data=json.dumps(responseDict),headers=headers)
            self.redirect('/studenthome')    
        else:
            self.redirect('/')
 
class StudentAddsResearchHandler(tornado.web.RequestHandler):
    def post(self):
        studentID = repr(self.get_secure_cookie('student'))
        studentID = studentID.split("'")
        studentID = str(studentID[1])
        if studentID:
            title = re.escape(self.get_argument("title"))
            print title
            abstract = re.escape(self.get_argument("abstract"))
            print abstract
            url = "https://api-us.clusterpoint.com/100629/stud/_search.json"
            headers = {"Authorization":"Basic bGVvcGFuaWdyYWhpQGdtYWlsLmNvbToyM2xlbzIz"}
            string = "<regno>"+studentID+"</regno>"
            values = dict(query=string)
            r = requests.post(url,data=json.dumps(values),headers=headers)
            responseDict = json.loads(r.content)
            projectCount = len(responseDict['documents'][0]['research'])
            mainID = responseDict['documents'][0]['id']
            
            research = responseDict['documents'][0]['research']
            
            research.append({"abstract":abstract, "title":title, "verified":"no"})
            payload = {'id':mainID, "research":research}
            url2update = "https://api-us.clusterpoint.com/100629/stud/_partial_replace.json"
            self.redirect('/studenthome')



class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("student")
        self.clear_cookie("company")
        self.clear_cookie("college")
        self.redirect('/')

class CompanyHomeHandler(tornado.web.RequestHandler):
    def get(self):
        company = repr(self.get_secure_cookie('company'))
        company = company.split("'")
        company = str(company[1])
        if company:
            url = "https://api-us.clusterpoint.com/100629/company/_search.json"
            headers = {"Authorization":"Basic bGVvcGFuaWdyYWhpQGdtYWlsLmNvbToyM2xlbzIz"}
            string = "<regno>"+company+"</regno>"
            values = dict(query=string)
            #r = requests.post(url,data=json.dumps(values), headers=headers)
            #responseDict = json.loads(r.content)
            twitterAct = "leo_cmu"
            url = "http://api.klout.com/v2/identity.json/twitter?screenName="+twitterAct+"&key=9h7k8hjkg8vkqb29656c9pmr"
            r = requests.get(url)
            response = json.loads(r.content)
            myid = response['id']
            url2 = "http://api.klout.com/v2/user.json/"+ str(myid)  +"?key=9h7k8hjkg8vkqb29656c9pmr"
            s = requests.get(url2)
            ans = json.loads(s.content)
            score = ans['score']['score']
            self.render('companyhome.html', score=score)

class CollgeHomeHandler(tornado.web.RequestHandler):
    def get(self):
        college = repr(self.get_secure_cookie('college'))
        college = college.split("'")
        college = str(college[1])
        if college:
            url = "https://api-us.clusterpoint.com/100629/stud/_search.json"
            headers = {"Authorization":"Basic bGVvcGFuaWdyYWhpQGdtYWlsLmNvbToyM2xlbzIz"}
            
            string = "<project><verified>no</verified></project>"
            values = dict(query=string)
            r = requests.post(url,data=json.dumps(values), headers=headers)
            responseDict = json.loads(r.content)
            title = list()
            abstract = list()
            studentID = responseDict['documents'][0]['id']
            for each in responseDict['documents'][0]['project']:
                if each['verified']=="no":
                    title.append(each['title'])
                    abstract.append(each['abstract'])
            self.render('collegehome.html', title=title, abstract=abstract, studentID=studentID)

class ReviewHandler(tornado.web.RequestHandler):
    def post(self):
        sid = self.get_argument('sid')
        abstract = self.get_argument('abstract')
        print abstract
        url = "https://api-us.clusterpoint.com/100629/stud/_search.json"
        headers = {"Authorization":"Basic bGVvcGFuaWdyYWhpQGdtYWlsLmNvbToyM2xlbzIz"}
        string = "<project><abstract>"+ abstract +"</abstract></project>"
        values = dict(query=string)
        r = requests.post(url,data=json.dumps(values), headers=headers)
        responseDict = json.loads(r.content)
        for each in responseDict['documents'][0]['project']:
            if each['abstract'] == abstract:
                mytext = each['abstract']
                alchemyapi = AlchemyAPI()
                response = alchemyapi.keywords('text', abstract, {'sentiment': 1})
                finalKeys = list()
                for each in response['keywords']:
                    try:
                        if float(each['relevance'])>0.5:
                            finalKeys.append(each['text'])
                            print finalKeys
                            self.render("tags.html", finalKeys=finalKeys)
                    except:
                        pass





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
    (r'/login',SelectLoginHandler),
    (r'/college',CollegeHandler),
    (r'/collegelogin',CollegeLoginHandler),
    (r'/collegehome',CollgeHomeHandler),
    (r'/student',StudentHandler),
    (r'/studentlogin',StudentLoginHandler),
    (r'/studenthome',StudentHomeHandler),
    (r'/addproject',StudentAddsProjectHandler),
    (r'/addresearch',StudentAddsResearchHandler),
    (r'/company',CompanyHandler),
    (r'/review',ReviewHandler),
    (r'/companylogin',CompanyLoginHandler),
    (r'/companyhome',CompanyHomeHandler),
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
