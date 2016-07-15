from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
import requests
import webbrowser
import time
import re
from bs4 import BeautifulSoup
from django.core.urlresolvers import resolve

# Create your views here.

#global variables
base_youtube_watch = 'https://www.youtube.com'
base_yt_url = 'https://www.youtube.com/results?search_query='
base_savedeo_url = 'https://savedeo.com/download?url='
base_alternate_url = 'https://youtubemultidownloader.com'
# base_ss_url = 'https://www.ssyoutube.com'
global flag_stay_video

global hit_threshold
hit_threshold = 1

#Homepage 
def home(request):
	return render(request, 'app/home.html')

def video(request):
	return render(request, 'app/video_form.html')

def playlist(request):
	return render(request, 'app/playlist.html')

# Save from Net Scraping using dryscrape.
# def get_download_links(watch_url):
# 	print("Yo")
# 	global hit_threshold
# 	global flag_stay_video
# 	abort = False
# 	abort_override = False
# 	download_url = base_ss_url + watch_url
# 	session2 = dryscrape.Session()
# 	session2.visit(download_url)
# 	time.sleep(2)
# 	response=session2.body()
# 	soup = BeautifulSoup(response,"lxml")
# 	sf_result = soup.find('div', {'class':'wrapper'}).find('div', {'class':'downloader-2'}).find('div',{'id':'sf_result'})
	
# 	hit_count = 1
# 	while True:
# 		print(hit_count)
# 		print("Inside3")
# 		if hit_count > hit_threshold:
# 			abort_override = True
# 			break
# 		media_result = sf_result.find('div', {'class':'media-result'})
# 		if media_result != None:
# 			info_box = media_result.find('div', {'class': 'info-box'})
# 			break
# 		else:
# 			session2 = dryscrape.Session()
# 			session2.visit(download_url)
# 			response=session2.body()
# 			soup = BeautifulSoup(response,"lxml")
# 			sf_result = soup.find('div', {'class':'wrapper'}).find('div', {'class':'downloader-2'}).find('div',{'id':'sf_result'})
# 		hit_count += 1
	
# 	if not abort_override:
# 		print("Hello")
# 		dropdown_box_list = info_box.find('div', {'class': 'link-box'}).find('div', {'class': 'drop-down-box'}).find('div', {'class': 'list'}).find('div', {'class': 'links'})
# 		download_link_groups = dropdown_box_list.findAll('div', {'class': 'link-group'})
# 		i=0
# 		list_links = []
# 		for group in download_link_groups:
# 			download_links = group.findAll('a')
# 			for link in download_links:
# 				download = str(link['download'])
# 				extension = re.split(r'\.(?!\d)', download)[-1]
# 				class_link = link['class']
# 				if class_link[0] != "no-audio":
# 					if extension == "mp4":
# 						i+=1
# 						video_format = link['title']
# 						list_links.append(link)
# 						print(str(i) + ". " + download + ", " + str(video_format) + ", Youtube Views: ")
			
# 		print(list_links)
# 		high_quality_link = list_links[0]
# 		to_download = high_quality_link
# 		to_download_url = to_download['href']
# 		highq_download_url = to_download_url
# 		if len(list_links) != 1:
# 			lowq_download_link = list_links[1]
# 			to_download = lowq_download_link
# 			to_download_url = to_download['href']
# 			lowq_download_url = to_download_url
# 		else:
# 			lowq_download_url =  highq_download_url	
			
# 		download_urls = {
# 			'high_quality_video': highq_download_url,
# 			'low_quality_video' : lowq_download_url
# 		}
# 		return download_urls
# 	else:
# 		return None

# Scraping from Savdeo using just BS. 
def get_download_links(watch_url):
	download_url = base_savedeo_url + base_youtube_watch + watch_url
	print(download_url)
	response = requests.get(download_url)
	soup = BeautifulSoup(response.text, 'lxml')
	try:
		table = soup.find('div',{'class':'clip'}).find('table')
		table_body = table.find('tbody')
		list_links = table_body.findAll('tr')
		list_download_links = []
		
		i=0 
		for link in list_links:
			video_format = link.findAll('td')[0].text
			if video_format == "mp4":
				download_link = link.findAll('td')[1].find('a')['href']
				list_download_links.append(download_link)
			i+=1
			if i>1:
				break
		
		highq_download_url = list_download_links[0]
		
		if len(list_download_links) != 1:
			lowq_download_url = list_download_links[1]
		else:
			lowq_download_url = highq_download_url

		download_urls = {
			'high_quality_video': highq_download_url,
			'low_quality_video' : lowq_download_url
		}
	except:
		download_url = base_alternate_url + watch_url
		print(download_url)
		response=requests.get(download_url)
		soup = BeautifulSoup(response.text,"lxml")
		result = soup.find('div',{'id':'Download_Quality'}).find('ul',{'class':'list-group'})
		list_download_links = result.findAll('li',{'class':'list-group-item'})[1].findAll('a')
		if list_download_links[0].text == "720P" or list_download_links[0].text == "360P":
			highq_download_url = list_download_links[0]['href']
		if list_download_links[1].text == "360P":
			lowq_download_url = list_download_links[1]['href']
		else:
			lowq_download_url = highq_download_url

		download_urls = {
			'high_quality_video': highq_download_url,
			'low_quality_video' : lowq_download_url
		}

	return download_urls


@require_GET
def download_video(request):
	global hit_threshold
	abort_override = False
	query_range = 2
	refresh_search_range = 2
	search = request.GET.get('search', '')
	if search:
		for i in range(0,refresh_search_range):
			search_url = base_yt_url + search
			response = requests.get(search_url)
			soup = BeautifulSoup(response.text,"lxml")
			list_results = soup.find('div', {'id': 'results'}).find('ol',{'class':'section-list'}).find('ol',{'class':'item-section'}).findAll('li')
			watch_result_list = []
			i=0
			for result in list_results:
				if result.find('div', {'class': 'pyv-afc-ads-container'}):
					continue
				elif result.find('div', {'class': re.compile(r'yt-lockup-channel')}) != None:
					continue
				elif result.find('div', {'class': re.compile(r'yt-lockup-playlist')}) != None:
					continue
				else:
					hit_count = 1
					while True:
						if hit_count > hit_threshold:
							abort_override = True
							break
						watch_result = result.find('div', {'class': "yt-lockup-content"})
						if watch_result != None:
							i+=1
							watch_result_list.append(watch_result)
							break
						hit_count += 1
						
					if(i>query_range):
						break

			#To get thumbnail photos of videos
			video_duration_list = []
			thumbnail_video_list = []
			i=0
			for result in list_results:
				if result.find('div', {'class': 'pyv-afc-ads-container'}):
					continue
				elif result.find('div', {'class': re.compile(r'yt-lockup-channel')}) != None:
					continue
				elif result.find('div', {'class': re.compile(r'yt-lockup-playlist')}) != None:
					continue
				else:
					hit_count = 1
					while True:
						if hit_count > hit_threshold:
							abort_override = True
							break
						thumbnail_result = result.find('div', {'class': re.compile(r'yt-lockup-thumbnail')})
						if thumbnail_result != None:
							i+=1
							thumbnail_src = thumbnail_result.find('span', {'class': 'yt-thumb-simple'}).find('img')['src']
							thumbnail_video_list.append(thumbnail_src)
							video_time_no_text = thumbnail_result.find('span', {'class': 'video-time'})
							if video_time_no_text != None:
								video_time = video_time_no_text.text
								video_duration_list.append(video_time)
							break
						hit_count += 1
							
					if(i>query_range):
						break
			list_video_details = []
			for i in range(0,query_range+1):
				bool_views = False
				video = {}
				hit_count = 1
				while True:
					if hit_count > hit_threshold:
						break
					try:
						video_views_no_text = watch_result_list[i].find('ul', {'class': 'yt-lockup-meta-info'})
						if video_views_no_text != None:
							try:
								video_views = video_views_no_text.findAll('li')[1].text
							except:
								bool_views = True
							break
						hit_count+=1
					except:
						bool_views = True
				if hit_count > hit_threshold or bool_views:
					continue
				video_views = video_views.split()[0]
				watch_url = watch_result_list[i].find('h3', {'class': 'yt-lockup-title'}).find('a')['href']
				video_title = watch_result_list[i].find('h3', {'class': 'yt-lockup-title'}).find('a').text
				if len(video_duration_list) > i :
					video_time = video_duration_list[i]
				else:
					video_time = " : "
				thumbnail_src = thumbnail_video_list[i]
				img_break = thumbnail_src.split('&')
				res1 = "w=480"
				res2 = "w=360"
				thumbnail_src = img_break[0] + "&" + res1 + "&" + res2
				for i in range(2,len(img_break)):
					thumbnail_src = thumbnail_src + "&" + img_break[i]
				download_links = get_download_links(watch_url)
				if download_links != None:
					high_quality_video_link = download_links['high_quality_video']
					low_quality_video_link = download_links['low_quality_video']
					video = {
						'title': video_title,
						'thumbnail': thumbnail_src,
						'watch_link': base_youtube_watch+watch_url,
						'views': video_views,
						'highq_link': high_quality_video_link,
						'lowq_link': low_quality_video_link,
						'time': video_time,
					}
					list_video_details.append(video)

			if not list_video_details:
				continue
			context = {
				'list_videos': list_video_details,
			}
			return render(request, 'app/video_list.html', context)
			break
	else:
		url = request.GET.get('url', '')
		watch_url = "/" + url.split('/')[3]
		print(watch_url)
		while True:
			download_links = get_download_links(watch_url)
			if download_links != None:
				break
		webbrowser.open_new(download_links['high_quality_video'])
		return render(request, 'app/home.html')

@require_GET
def confirm_playlist(request):
	if request.is_ajax():
		search_url = request.GET.get('playlist_url','')
		response = requests.get(search_url)
		soup = BeautifulSoup(response.text, 'lxml')
		content = soup.find('div',{'id': 'page-container'}).find('div',{'id': 'content'}).find('div',{'class': 'branded-page-v2-col-container'})
		inner_content = content.find('div',{'class': 'branded-page-v2-col-container-inner'}).find('div',{'class': 'branded-page-v2-primary-col'})
		header_content = inner_content.find('div',{'id': 'pl-header'}).find('div',{'class': 'pl-header-content'})
		playlist_title = header_content.find('h1',{'class': 'pl-header-title'}).text
		playlist_details = header_content.find('ul', {'class', 'pl-header-details'}).findAll('li')
		playlist_author = playlist_details[0].text
		playlist_video_count = int(playlist_details[1].text.split()[0])
		playlist_views = playlist_details[2].text.split()[0]
		playlist_image = inner_content.find('div', {'id':'pl-header'}).find('div',{'class':'pl-header-thumb'}).find('img')['src']
		playlist_image_src = playlist_image
		data = {
			'title' : str(playlist_title),
			'author': str(playlist_author),
			'views' : str(playlist_views),
			'videos_count' : str(playlist_video_count),
			'playlist_image' : playlist_image_src, 
		}
		return JsonResponse(data)
	else:
		return Http404

@require_GET
def get_playlist_videos_details(request):
	search_url = request.GET.get('url','')
	response = requests.get(search_url)
	soup = BeautifulSoup(response.text, 'lxml')
	content = soup.find('div',{'id': 'page-container'}).find('div',{'id': 'content'}).find('div',{'class': 'branded-page-v2-col-container'})
	inner_content = content.find('div',{'class': 'branded-page-v2-col-container-inner'}).find('div',{'class': 'branded-page-v2-primary-col'})
	playlist_content = inner_content.find('ul', {'id': 'browse-items-primary'}).find('div', {'id': 'pl-video-list'}).find('tbody', {'id':'pl-load-more-destination'})
	list_videos = playlist_content.findAll('tr')
	list_video_details = []
	for tr in list_videos:
		video_title = tr.find('td', {'class': 'pl-video-title'}).find('a').text
		video_image = tr.find('td', {'class': 'pl-video-thumbnail'}).find('span',{'class': 'yt-thumb-default'}).find('span', {'class':'yt-thumb-clip'}).find('img')['data-thumb']
		video_time = tr.find('td', {'class': 'pl-video-time'}).find('div', {'class': 'timestamp'}).find('span').text
		video = {
			'title' : video_title,
			'image' : video_image,
			'time' : video_time,
		}
		list_video_details.append(video)

	context = {
		'list_videos' : list_video_details,
	}
	return render(request, 'app/playlist_videos.html', context)

@require_GET
def download_all_videos_playlist(request):
	if request.is_ajax:
		search_url = request.GET.get('playlist_url','')
		response = requests.get(search_url)
		soup = BeautifulSoup(response.text, 'lxml')
		content = soup.find('div',{'id': 'page-container'}).find('div',{'id': 'content'}).find('div',{'class': 'branded-page-v2-col-container'})
		inner_content = content.find('div',{'class': 'branded-page-v2-col-container-inner'}).find('div',{'class': 'branded-page-v2-primary-col'})
		playlist_content = inner_content.find('ul', {'id': 'browse-items-primary'}).find('div', {'id': 'pl-video-list'}).find('tbody', {'id':'pl-load-more-destination'})
		list_videos = playlist_content.findAll('tr')
		list_watch_urls = []
		for tr in list_videos:
			video = tr.find('td', {'class': 'pl-video-title'}).find('a')
			watch_url = video['href']
			list_watch_urls.append(watch_url)
		for url in list_watch_urls:
			while True:
				download_links = get_download_links(url)
				if download_links != None:
					break
			webbrowser.open(download_links['high_quality_video'])

@require_GET
def download_partial_videos_playlist(request):
	if request.is_ajax:
		search_url = request.GET.get('playlist_url','')
		index_videos = request.GET.getlist('index_videos','')
		print(index_videos)
		response = requests.get(search_url)
		soup = BeautifulSoup(response.text, 'lxml')
		content = soup.find('div',{'id': 'page-container'}).find('div',{'id': 'content'}).find('div',{'class': 'branded-page-v2-col-container'})
		inner_content = content.find('div',{'class': 'branded-page-v2-col-container-inner'}).find('div',{'class': 'branded-page-v2-primary-col'})
		playlist_content = inner_content.find('ul', {'id': 'browse-items-primary'}).find('div', {'id': 'pl-video-list'}).find('tbody', {'id':'pl-load-more-destination'})
		list_videos = playlist_content.findAll('tr')
		list_watch_urls = []
		index = 1
		for tr in list_videos:
			#Checking whether index is in the list provided by the user.
			if str(index) in index_videos:
				video = tr.find('td', {'class': 'pl-video-title'}).find('a')
				watch_url = video['href']
				watch_url = watch_url.split('&')[0]
				list_watch_urls.append(watch_url)
			index+=1
		print("holo")
		print(list_watch_urls)

		for url in list_watch_urls:
			while True:
				download_links = get_download_links(url)
				if download_links != None:
					break
			webbrowser.open(download_links['high_quality_video'])

