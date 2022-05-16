#!/usr/bin/env -S python3 -B

from config import *
from progress import *

import os
import shutil
from urllib import request

from zipfile import ZipFile
import tarfile



# claudflare on jpeg-site set ban for python/urllib user-agent
user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'


def read_links():
	res = {}
	if not os.path.exists(scripts_path + 'links.txt'):
		print('File <links.txt> not found')
		os.sys.exit(1)
	
	f = open(scripts_path + 'links.txt', 'rb')
	for s in f:
		if s and not s.startswith(b'#'):
			lib, url = str(s, 'utf8').split(': ')
			res[lib.strip()] = url.strip()
	
	return res

urls = read_links()
links_of = set(urls.keys())
need_libs = set(libs)
if links_of != need_libs:
	no_links = need_libs.difference(links_of)
	if no_links:
		print('No links for libs: ' + ', '.join(no_links))
	extra_links = links_of.difference(need_libs)
	if extra_links:
		print('Extra links for libs: ' + ', '.join(extra_links))
	os.sys.exit(1)



if not os.path.exists(download_path):
	os.makedirs(download_path)
if not os.path.exists(sources_path):
	os.makedirs(sources_path)

def extract(f):
	if f.endswith('zip'):
		archive = ZipFile(f, 'r')
	elif f.endswith('gz'):
		archive = tarfile.open(f, 'r:gz')
	else:
		global was_error
		was_error = True
		print('  Archive <' + f + '> does not ends with zip or gz')
		return
	
	archive.extractall(os.path.dirname(f))


was_error = False
downloaded = []

progress_list = read_progress()
for i in range(len(progress_list)):
	lib, progress = progress_list[i]
	
	if lib not in urls:
		print('URL for <' + lib + '> is unknown') 
		continue
	if progress != 'start':
		continue

	
	for d in os.listdir(sources_path):
		if os.path.isdir(sources_path + d) and d.startswith(lib) and not d.startswith(lib + '_'):
			shutil.rmtree(sources_path + d)
			break
	
	url = urls[lib]
	
	try:
		print('Download <' + lib + '>')
		
		if 'git' in url:
			if ' ' in url: # there are params for git
				index = url.index(' ')
				only_url = url[0:index]
			else:
				only_url = url
			dirname, _ = os.path.splitext(os.path.basename(only_url))
			
			if not os.path.exists(download_path + dirname):
				os.chdir(download_path)
				cmd = 'git clone -c advice.detachedHead=false --depth=1 ' + url
				if os.system(cmd):
					print('Comand <' + cmd + '> failed')
					was_error = True
					continue
				
				if lib == 'freetype':
					cmd = 'cd ./freetype/ && ./autogen.sh && cd ..'
					if os.system(cmd):
						print('Comand <' + cmd + '> failed')
						was_error = True
						continue
			else:
				print('  use cached')
			
		else:
			file_path = download_path + os.path.basename(url)
			
			if not os.path.exists(file_path):
				req = request.Request(url)
				req.add_header('User-Agent', user_agent)
				
				sock = request.urlopen(req)
				content = sock.read()
				sock.close()
				
				f = open(file_path, 'wb')
				f.write(content)
				f.close()
			else:
				print('  use cached')
			
			extract(file_path)
		
		downloaded.append(lib)
		
		progress_list[i] = lib, 'downloaded'
		write_progress(progress_list)
		
	except BaseException as e:
		if type(e) is KeyboardInterrupt:
			os.sys.exit(1)
		
		was_error = True
		print('Error on download <' + lib + '>')
		print('You can repeat later or find and download by yourself')
		print(e)


if downloaded:
	print('Downloaded libs: ' + ', '.join(downloaded))
elif not was_error:
	print('Nothing to do')
