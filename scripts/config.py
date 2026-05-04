import os

libs = ['cpython', 'jemalloc', 'ffmpeg', 'zlib-ng', 'brotli', 'freetype', 'libjpeg-turbo', 'libwebp', 'SDL', 'SDL_image', 'SDL_ttf']
if os.sys.platform == 'cygwin':
	libs.remove('jemalloc')

scripts_path = os.path.dirname(os.path.abspath(__file__)) + '/'

for c in scripts_path:
	if c >= 'a' and c <= 'z': continue
	if c >= 'A' and c <= 'Z': continue
	if c >= '0' and c <= '9': continue
	if c not in '+-_/:':
		print('Path contains bad symbol: ' + c)
		os.sys.exit(1)

sources_path  = scripts_path + '../sources/'


params_path = scripts_path + 'params.txt'

def read_params():
	res = {}
	
	with open(params_path, 'rb') as f:
		for line in f:
			name, value = str(line, 'utf-8').strip().split(' ')
			res[name] = value
	
	return res

def write_params(params):
	with open(params_path, 'wb') as f:
		for name in params:
			value = params[name]
			f.write(bytes(name + ' ' + value + '\n', 'utf-8'))
