#!/usr/bin/env -S python3 -B

import os
import shutil
from config import *
from progress import *


def read_ignore(path):
	ignore_from_root, ignore, important_from_root, important = [], [], [], []
	
	with open(path, 'rb') as f:
		for b in f:
			s = str(b, 'utf-8').strip()
			if not s or s[0] == '#': continue
			
			if s[0] == '!':
				templates_from_root, templates = important_from_root, important
				s = s[1:]
			else:
				templates_from_root, templates = ignore_from_root, ignore
			
			if s[0] == '/':
				templates_from_root.append(s)
			else:
				templates.append(s)
	
	return ignore_from_root, ignore, important_from_root, important

def in_templates(path, templates_from_root, templates):
	for template in templates_from_root:
		if path.startswith(template):
			return True
	for template in templates:
		if template in path:
			return True
	return False

def need_ignore(path, ignore_from_root, ignore, important_from_root, important):
	if path.startswith('/.git/') or path.startswith('/.github/'):
		return True
	if in_templates(path, ignore_from_root, ignore):
		if not in_templates(path, important_from_root, important):
			return True
	return False


was_error = False
copied = []

progress_list = read_progress()
def copy(lib):
	for i, (tmp_lib, tmp_progress) in enumerate(progress_list):
		if tmp_lib == lib:
			progress = tmp_progress
			break
	else:
		print('Unknown lib <%s>' % lib)
		return
	
	if progress != 'downloaded':
		return
	
	if not os.path.isdir(download_path + '/' + lib):
		print('Path for <%s> not found' % lib)
		os.sys.exit(1)
	
	ignore_path = scripts_path + 'ignore/' + lib + '.txt'
	ignore_from_root, ignore, important_from_root, important = read_ignore(ignore_path)
	
	src = download_path + lib + '/'
	dst = sources_path + lib + '/'
	if os.path.exists(dst):
		shutil.rmtree(dst)
	
	try:
		print('Copy <%s>' % lib)
		
		for p, ds, fs in os.walk(src):
			old_directory = p.rstrip('/') + '/'
			new_directory = dst + p[len(src):].rstrip('/') + '/'
			
			for f in fs:
				old_f = old_directory + f
				new_f = new_directory + f
				path_from_root = old_f[len(src)-1:]
				
				if not need_ignore(path_from_root, ignore_from_root, ignore, important_from_root, important):
					os.makedirs(new_directory, exist_ok = True)
					shutil.copy2(old_f, new_f)

		copied.append(lib)
		
		progress_list[i] = (lib, 'copied')
		write_progress(progress_list)
		
	except BaseException as e:
		if type(e) is KeyboardInterrupt:
			os.sys.exit(1)

		global was_error
		was_error = True
		print('Error on copying <%s>' % lib)
		print(e)

for lib in libs:
	copy(lib)

if copied:
	print('Copied libs: ' + ', '.join(copied))
elif not was_error:
	print('Nothing to do')
