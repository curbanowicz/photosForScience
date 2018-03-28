#Christine Urbanowicz
#March 24, 2017
#Attempting to use flickr api to download photos that match a search
#AND create a table with relevant info (date taken, user name, caption)
#I don't know what I am doing. No idea whatsoever. 

#https://github.com/sybrenstuvel/flickrapi
#https://github.com/philadams/flickr-images-grab
#http://www.bertcarremans.be/downloading-images-flickr-api-python/ #main source of code
#https://github.com/bertcarremans/Vlindervinder/tree/master/flickr
#https://github.com/pep-dortmund/pars/issues/3 version problem with exception (config and flickr_api)
#https://www.flickr.com/groups/51035612836@N01/discuss/72157605575890661/ 

from flickrapi import FlickrAPI
#flickr_api interface is for python 2 but not 3
import urllib
import os
from random import randint
import time
import keyAndFolderConfig
import pandas
import json
from pprint import pprint

def download_flickr_photos(keywords, size='original',max_nb_img=-1):

    if not (isinstance(keywords, str) or isinstance(keywords, list)):
        raise AttributeError('keywords must be a string or a list of strings')
        
    if not (size in ['thumbnail', 'square', 'small', 'medium', 'original']): #added small
        raise AttributeError('size must be "thumbnail", "square", "medium" or "original"')
                             
    if not (max_nb_img == -1 or (max_nb_img > 0 and isinstance(max_nb_img, int))):
        raise AttributeError('max_nb_img must be an integer greater than zero or equal to -1')
    
    flickr = FlickrAPI(keyAndFolderConfig.API_KEY, keyAndFolderConfig.API_SECRET)
    
    if isinstance(keywords, str):
        keywords_list = []
        keywords_list.append(keywords)
    else:
        keywords_list = keywords
        
    if size == 'thumbnail':
        size_url = 'url_t'
    elif size == 'square':
        size_url = 'url_q'
    elif size == 'small': #added small
        size_url = 'url_n'
    elif size == 'medium':
        size_url = 'url_z' #changed medium to the smaller medium
    elif size == 'original':
        size_url = 'url_o'
    
    for keyword in keywords_list:
        count = 0
                             
        #print('Downloading images for', keyword)

        results_folder = keyAndFolderConfig.IMG_FOLDER + keyword.replace(" ", "_") + "/"
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        photos = flickr.walk(
                     text=keyword,
                     extras='description,geo,license,'+size_url,
                     license='0,1,2,3,4,5,6,7,8,9,10', # cu: modified to include 0, 3
                     per_page=50,
                     has_geo=1)

        photo_list = []

        for photo in photos:
            t = randint(1, 3)
            time.sleep(t)
            count += 1
            if max_nb_img != -1:
                if count > max_nb_img:
                    print('Reached maximum number of images to download')
                    break

            if count == 1:
                print("photo object attributes are: ")
                print(photo.keys())

            #print(flickr.photos.getInfo(photo_id=photo.get('id'))[0][0].keys())
            try:
                url=photo.get(size_url)
                urllib.request.urlretrieve(url,  results_folder + str(count) +".jpg")
                print('Downloading image #' + str(count) + ' from url ' + url)

                photo_info = {}
                photo_info['url'] = url
                photo_info['title'] = photo.get('title') #cu added this block
                photo_info['description'] = photo.get('description')
                photo_info['uid'] = photo.get('id')
                photo_info['user_id'] = photo.get('owner')
                geo = {
                    'lat': photo.get('latitude'),
                    'lon': photo.get('longitude'),
                }
                photo_info['geo'] = geo
                photo_info['license'] = photo.get('license')

                photo_list.append(photo_info)

            except Exception as e:
                print(e, 'Download failure')
                             
        print("Total images downloaded:", str(count - 1))
        for photo in photo_list:
            print(photo)


download_flickr_photos('artic fox', size='small', max_nb_img=5) 

#flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
#extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
#cats = flickr.photos.search(text='kitten', per_page=500, extras=extras)
#photos = cats['photos']
#from pprint import pprint
#pprint(photos)
