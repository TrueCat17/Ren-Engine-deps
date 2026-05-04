#!/usr/bin/env -S python3 -B

import os
from config import *


ok = True
for prog in ('nasm', 'libtoolize', 'automake', 'autoconf', 'make'):
	if os.system('command -v %s > /dev/null' % prog):
		print('You must install <%s>' % prog)
		ok = False


not_found_libs = []
for lib in libs:
	if not os.path.exists(sources_path + lib + '/'):
		not_found_libs.append(lib)

if not_found_libs:
	print('Download and unpack to <%s> next libs:' % sources_path)
	for lib in not_found_libs:
		print('  ' + lib)
elif ok:
	print('Ok.')
