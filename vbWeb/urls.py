"""vbWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views as appviews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', appviews.home, name='home'),
    url(r'^video/$',appviews.video, name='video'),
    url(r'^video/download/$', appviews.download_video, name = 'download-video'),
    url(r'^playlist/$',appviews.playlist, name='playlist'),
    url(r'^playlist/confirm/$',appviews.confirm_playlist, name='confirm-playlist'),
    url(r'^playlist/download/$', appviews.get_playlist_videos_details, name = 'download-playlist'),
    url(r'^playlist/download/all$', appviews.download_all_videos_playlist, name = 'download-full-playlist'),
    url(r'^playlist/download/partial$', appviews.download_partial_videos_playlist, name = 'download-partial-playlist'),
]
