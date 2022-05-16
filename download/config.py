import os

libs = ['cpython', 'jemalloc', 'ffmpeg', 'zlib', 'brotli', 'freetype', 'libjpeg', 'libpng', 'libwebp', 'SDL', 'SDL_image', 'SDL_ttf']

scripts_path = os.path.dirname(os.path.abspath(__file__)) + '/'
scripts_path = scripts_path.replace('\\', '/')

for c in scripts_path:
	if c >= 'a' and c <= 'z': continue
	if c >= 'A' and c <= 'Z': continue
	if c >= '0' and c <= '9': continue
	if c not in '+-_/:':
		print('Path contains bad symbol: ' + c)
		os.sys.exit(1)

download_path = scripts_path + 'cache/'
sources_path  = scripts_path + '../sources/'
