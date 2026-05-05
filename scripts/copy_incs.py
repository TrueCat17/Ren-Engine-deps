#!/usr/bin/env -S python3 -B

import os
import shutil
from config import *

params = read_params()
platform = params['platform']


inc_path = scripts_path + '../' + platform + '/include/'
if os.path.exists(inc_path):
	shutil.rmtree(inc_path)



python_path = sources_path + 'cpython/'
if os.path.exists(python_path):
	shutil.copytree(
		python_path + 'Include/',
		inc_path + 'python3/',
		ignore = shutil.ignore_patterns('internal')
	)
	
	# remove __declspec (for cygwin)
	exports_file_paths = (
		python_path + 'Include/exports.h',
		inc_path + 'python3/exports.h'
	)
	os.system('sed -e "s/__declspec.*//" %s > %s' % exports_file_paths)
	
	src_path = python_path + 'pyconfig.h'
	dst_path = inc_path + 'python3/pyconfig.h'
	with open(src_path, 'rb') as src, open(dst_path, 'wb') as dst:
		macros = '_POSIX_C_SOURCE _XOPEN_SOURCE _XOPEN_SOURCE_EXTENDED __BSD_VISIBLE __EXTENSIONS__'.split(' ')
		
		for line in src:
			line = str(line, 'utf-8')
			
			for macro in macros:
				if line.startswith('#define ' + macro):
					line = '#ifndef ' + macro + '\n\t' + line + '#endif\n'
			
			dst.write(bytes(line, 'utf-8'))
else:
	print('Python sources not found')



ffmpeg_path = sources_path + 'ffmpeg/'
if os.path.exists(ffmpeg_path):
	os.makedirs(inc_path + 'libavcodec/')
	need_avcodec_headers = (
		'version_major.h',
		'version.h',
		'packet.h',
		'defs.h',
		'codec_par.h',
		'codec_id.h',
		'codec_desc.h',
		'codec.h',
		'avcodec.h',
	)
	for f in need_avcodec_headers:
		shutil.copyfile(ffmpeg_path + 'libavcodec/' + f, inc_path + 'libavcodec/' + f)
	
	def ignore_not_headers(_, fs):
		return [f for f in fs if not f.endswith('.h')]
	for lib in 'libavformat libavutil libswresample'.split(' '):
		shutil.copytree(
			ffmpeg_path + lib + '/',
			inc_path + lib + '/',
			ignore = ignore_not_headers,
		)
else:
	print('ffmpeg sources not found')



sdl_path = sources_path + 'SDL/'
if os.path.exists(sdl_path):
	shutil.copytree(sdl_path + 'include/SDL3', inc_path + 'SDL3')
else:
	print('SDL sources not found')


sdl_image_path = sources_path + 'SDL_image/'
if os.path.exists(sdl_image_path):
	shutil.copyfile(sdl_image_path + 'include/SDL3_image/SDL_image.h', inc_path + 'SDL3/SDL_image.h')
else:
	print('SDL_image sources not found')


sdl_ttf_path = sources_path + 'SDL_ttf/'
if os.path.exists(sdl_ttf_path):
	shutil.copyfile(sdl_ttf_path + 'include/SDL3_ttf/SDL_ttf.h', inc_path + 'SDL3/SDL_ttf.h')
else:
	print('SDL_ttf sources not found')
