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
import json
import logging
from google.appengine.api import urlfetch
from random import randint

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	main_template = jinja_environment.get_template('templates/main.html')
    	self.response.out.write(main_template.render())
    def post(self):
        base_url = "http://api.giphy.com/v1/gifs/search?q="
        api_key_url = "&api_key=dc6zaTOxFJmzC"
        search = self.request.get('search')
        search_term = search + '%20hunger%20games'
        if search_term:
           url = base_url + search_term + api_key_url
           parsed_data = json.loads(urlfetch.fetch(url).content)
           if parsed_data['data']:
            random_index = randint(0,len(parsed_data['data']))
            gif_url = parsed_data['data'][random_index]['images']['original']['url']
            msg = "okay"
           else:
             msg ="not found"
             gif_url=""
           template = jinja_environment.get_template('templates/complete.html')
           #self.response.out.write(url)
           self.response.out.write(template.render({"search_term" : search, "url" : gif_url, "msg": msg}))
        else:
           self.response.write(('Please enter a search term'))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
