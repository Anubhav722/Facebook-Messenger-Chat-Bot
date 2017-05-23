from django.conf.urls import include, url
from .views import FBChatBotView
urlpatterns = [
	url(r'^af1a0e5aeffd59bd1ac7f09d62d9f9f41cd42cc8396cc74a47/?$', FBChatBotView.as_view(), name='bot'),
]