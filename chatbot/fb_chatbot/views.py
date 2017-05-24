# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, requests, random, re
from pprint import pprint

from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.

jokes = {
         'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                    """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
         'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                    """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
         'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                    """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] 
         }

PAGE_ACCESS_TOKEN = 'EAATlAEoSaTQBAL66HkhAbskaZCxGYOL4iuTHZAacmBQz9hYC924DVOZAZBpPiqaFpkCqjZCMgZB4Ox4oJ4P88jkpZA6buIeonXPAEKTVkZBWMNfXIpWWrH4TLEJ83OJNcIECybY4HUgVVGKPteQqqXQuqlOmEvGcnk73bHXpiFx9wwZDZD'
# class FBChatBotView(generic.View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("Hello World!")

def post_facebook_message(fbid, recevied_message):
	tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
	joke_text = ''
	for token in tokens:
		if token in jokes:
			joke_text = random.choice(jokes[token])
			break

	if not joke_text:
		joke_text = "I didn't understand! Send 'stupid', 'fat', 'dumb' for a Yo mama joke!"

	user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()

	try:
		pprint("The user's first name is: %s" %user_details['first_name'])
		pprint("The user's last name is %s" %user_details['last_name'])
		pprint("The user's profile_pic is %s" %user_details['profile_pic'])
		joke_text = "Yo' " + user_details['first_name'] + '..!' + joke_text

	except KeyError:
		pass

	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	# post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=<page-access-token>'
	# response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	pprint(status.json())

class FBChatBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '7697631870':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
    	return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		# pprint(incoming_message)
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					pprint(message)

					post_facebook_message(message['sender']['id'], message['message']['text'])

		return HttpResponse()