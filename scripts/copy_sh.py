#!/usr/bin/env -S python3 -B

import os
from config import *

def copy(cmd):
	ok = True
	for lib in libs:
		if not os.path.isdir(sources_path + lib):
			print('Path for <%s> not found' % lib)
			ok = False
	if not ok:
		os.sys.exit(1)
	
	
	for f in os.listdir(scripts_path + cmd):
		if not f.endswith('.sh'): continue
		
		name = f[:-len('.sh')]
		
		src = scripts_path + cmd + '/' + f
		dst = sources_path + name + '/' + cmd + '.sh'
		
		with open(src, 'rb') as f:
			content = str(f.read(), 'utf-8')
		
		content = content.replace('CC="gcc"', 'CC="%s"' % cc)
		
		if not lto:
			content = content.replace('--with-lto', '--without-lto')
			content = content.replace('-flto', '')
		
		if not pgo:
			content = content.replace('--enable-optimizations', '--disable-optimizations')
		
		content = content.replace('000res/', copy_libs_to)
		
		content = content.replace('-j4', '-j%i' % count_threads)
		
		with open(dst, 'wb') as f:
			f.write(bytes(content, 'utf-8'))
		
		os.system('chmod +x "%s"' % dst)
		
		for script in ('./autogen.sh', './configure'):
			path = sources_path + name + '/' + script
			if os.path.exists(path):
				os.system('chmod +x "%s"' % path)


def set_platform():
	global platform, cc
	print('1/6: Platform')
	
	if 'linux' in os.sys.platform:
		print('Choose platform:')
		print('1. i686   (x32)')
		print('2. x86_64 (x64)')
		
		action = input('Input number of action (empty = auto): ')
		if action not in ('1', '2'):
			action = '2' if os.sys.maxsize > 2**32 else '1'
		
		platform =   'linux-i686' if action == '1' else 'linux-x86_64'
		cc = 'i686-linux-gnu-gcc' if action == '1' else 'x86_64-linux-gnu-gcc'
	
	else:
		platform = 'win32'
		cc = 'i686-pc-cygwin-gcc'
	
	print('  platform  = %s' % platform)
	print('  compilier = %s' % cc)
	print()
	
	if os.system('command -v %s > /dev/null' % cc):
		print('Compilier <%s> not found' % cc)
		os.sys.exit(1)


def set_lto():
	global lto
	
	print('2/6: LTO')
	if platform == 'win32':
		print('Disabled for win32.')
		lto = False
	else:
		print('Link Time Optimization make building very slow.')
		lto = input('Input 1 to enable LTO: ') == '1'
	
	global copy_libs_to
	copy_libs_to = '../' + platform + '/' + ('lto' if lto else 'no_lto') + '/'
	os.makedirs(scripts_path + copy_libs_to, exist_ok = True)
	
	print('  LTO: %s' % ('enabled' if lto else 'disabled'))
	print()


def set_pgo():
	print('3/6: PGO for python')
	print('Profile Guided Optimization make building very slow.')
	
	global pgo
	pgo = input('Input 1 to enable PGO: ') == '1'
	
	print('  PGO: %s' % ('enabled' if pgo else 'disabled'))
	print()


def set_multithreading():
	global count_threads
	print('4/6: Multithreading')
	print('  Recommended use N build-threads on N-core PC.')
	print('  But more threads require more memory.')
	
	answer = input('Input count threads for building (empty = auto): ')
	if answer.isdigit() and int(answer) > 0:
		count_threads = int(answer)
	else:
		count_threads = os.cpu_count()
	print('  Using %i threads' % count_threads)
	print()



set_platform()
set_lto()
set_pgo()
set_multithreading()

write_params({
	'platform': platform,
})


print('5/6: Copy files to configure libs')
copy('conf')
print('6/6: Copy files to build libs')
copy('make')
