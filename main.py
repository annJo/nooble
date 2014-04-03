#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import sys
import re
import json
sys.path.insert(0, 'libs')
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

template_dir = os.path.join(os.path.dirname(__file__),'templates')
docs_dir = os.path.join(os.path.dirname(__file__),'docs')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
docs_env = jinja2.Environment(loader = jinja2.FileSystemLoader(docs_dir),autoescape= True)



d = {}

d2 = {4:5}

def strip_tags(html,fname):
    if html is None:
        return None
    else:
        strippped_Html = re.sub('<script[^>]*>[^<]*</script>','',html)
        soup = BeautifulSoup(strippped_Html)
        tokens = soup.get_text()
        tokens = tokens.lower()
        tokens = re.sub('[^\w\s]+','',tokens)
        tokens_list = tokens.split()
        #print tokens_list

        for i in tokens_list:
            if i in d:
                if fname in d[i]:
                    d[i][fname] = d[i][fname] + 1
                else:
                    d[i][fname] = 1
            else:
                d[i] = {fname:1}




for root, dirs, files in os.walk("docs"):
       filenames = files
            
for name in filenames:
       strip_tags(open("docs/"+name,"r").read(),name)


class Handler(webapp2.RequestHandler):
    def write(self,*a, **kw):
        self.response.write(*a, **kw)

    def render(self, template,*a, **kw):
        self.write(self.render_str(template,*a, **kw))

    def render_str(self, template,*a, **params):
        #t = jinja2_env.get_template(template)
        #print "fksldjfklsdj : ",params
        if(a[0] == 'render'):
            t = jinja_env.get_template(template)
        else:
            t = docs_env.get_template(template)
        print "params :",params
        return t.render(params = params)
          
    

class MainPage(Handler):
    def get(self):
        self.render('index.html','render')

class QueryResolver(Handler):
        
    def post(self):
        query = self.request.get("field")
        print query
	if query in d:
        	params = d[query]
        else:
		params = 'Not found'

	self.response.out.write(json.dumps(params))
        
        
        
app = webapp2.WSGIApplication([('/', MainPage),('/queryResolver',QueryResolver)], debug=True)
