#!/usr/bin/env -S python3 -B

import os

from config import *


libs_on = [
	'math', '_struct', '_random', '_pickle',
	'_sha256', '_sha512', 'binascii', 'unicodedata',
	'zlib', 'select', 'fcntl', '_socket', 'array',
	'_posixsubprocess',
]
libs_off = ['pwd', '_ssl', '_md5']


for i in os.listdir(sources_path):
	if i.startswith('cpython'):
		mods = sources_path + i + '/Modules/'
		break
else:
	print('Python-dir not found')
	os.sys.exit(1)

setup_file = mods + 'Setup'

src = open(setup_file, 'rb')
lines = [str(i, 'utf8') for i in src]
src.close()

dst = open(setup_file, 'wb')

def set_on(name, lines):
	need_continue = False
	l = len(lines)
	last = l - 1
	for i in range(l):
		s = lines[i]
		if need_continue or s.startswith('#' + lib + ' '):
			lines[i] = s[1:]
			need_continue = s.endswith('\\\n') and i != last and lines[i + 1].startswith('#')
			if not need_continue:
				return

def set_off(name, lines):
	need_continue = False
	l = len(lines)
	last = l - 1
	for i in range(l):
		s = lines[i]
		if need_continue or s.startswith(lib + ' '):
			lines[i] = '#' + s
			need_continue = s.endswith('\\\n') and i != last and not lines[i + 1].startswith('#')
			if not need_continue:
				return

for lib in libs_on:
	set_on(lib, lines)
for lib in libs_off:
	set_off(lib, lines)

for s in lines:
	dst.write(bytes(s, 'utf8'))
