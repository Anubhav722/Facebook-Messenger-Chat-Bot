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

# PAGE_ACCESS_TOKEN = 'EAATlAEoSaTQBAL66HkhAbskaZCxGYOL4iuTHZAacmBQz9hYC924DVOZAZBpPiqaFpkCqjZCMgZB4Ox4oJ4P88jkpZA6buIeonXPAEKTVkZBWMNfXIpWWrH4TLEJ83OJNcIECybY4HUgVVGKPteQqqXQuqlOmEvGcnk73bHXpiFx9wwZDZD'

PAGE_ACCESS_TOKEN = 'EAATlAEoSaTQBAL66HkhAbskaZCxGYOL4iuTHZAacmBQz9hYC924DVOZAZBpPiqaFpkCqjZCMgZB4Ox4oJ4P88jkpZA6buIeonXPAEKTVkZBWMNfXIpWWrH4TLEJ83OJNcIECybY4HUgVVGKPteQqqXQuqlOmEvGcnk73bHXpiFx9wwZDZD'
# class FBChatBotView(generic.View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("Hello World!")

def post_facebook_message(fbid, recevied_message):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	# post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=<page-access-token>'
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
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