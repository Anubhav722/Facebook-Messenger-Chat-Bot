# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
# Create your views here.

# class FBChatBotView(generic.View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("Hello World!")

class FBChatBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '7697631870':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')