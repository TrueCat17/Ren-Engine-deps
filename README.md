## Preparing

For start, **if your OS is Windows**, you must download and install
[MSYS2 32-bit](https://repo.msys2.org/distrib/msys2-i686-latest.exe).  
Warning: don't use any 64-bit packages (with x86_64), only 32-bit (with i686).  
Warning: use **shell** MSYS, not MinGW\*.  
After it, you must update package database in MSYS2's PACkage MANager:  
`pacman -Syu`  
and (if needed, close MSYS and run it again) update rest:  
`pacman -Su`  
If you have some errors with PGP keys (or other problems),
see [this page](https://www.msys2.org/news/#2020-06-29-new-packagers),
fix problem and run prev 2 commands again.  
Also you must open `%msys2_dir%/home/user/.bashrc`, add `PATH="/mingw32/bin:$PATH"` and restart MSYS.

You must have installed **packages**:
`python3`, `git`, `nasm`, `autoconf`, `automake`, `libtool`, `make`, `cmake`, `gcc`, `g++`.  

Examples:
* MSYS: `pacman -S python3 git nasm autoconf automake libtool make mingw-w64-i686-cmake mingw-w64-i686-gcc`  
(not just cmake and gcc, only with i686!)
* Debian-based OS: `apt-get install python3 git nasm autoconf automake libtool make cmake gcc g++`

**If your OS is Linux**, you must also install:
* for audio subsystem: `libasound-dev libpulse-dev`
* for window subsystem: `libdbus-1-dev libudev-dev libxrandr-dev libxcursor-dev libxxf86vm-dev libgl-dev`  
(or just `xorg-dev`, but it is not only needed packages).

***

## Building

0. Make sure you have 1.5 GB of free space.


1. Open shell (MSYS for Windows) and change dir to `scripts`:
```
$ cd Ren-Engine/libs/scripts
```


2. Check programs installed and libs ready to build:
```
$ ./check.py
Ok.
```
Install programs if you forgot to do it earlier.


3. Set <start> status for all libs (in file `progress_list.txt`):
```
$ ./progress.py
```


4. Copy files (bash-scripts) for building libs:
```
$ ./copy_sh.py
```
Here you can choose platform (x32 or x64, Linux only), enable/disable optimisations that makes building slower, etc...  
For the first time, it is recommended not to use optimizations, just to check for errors.


5. Build libs:
```
$ ./build.py
# ... building prev libs ...
Build <SDL_ttf>
./conf.sh 1>conf_out.txt 2>conf_err.txt
./make.sh 1>make_out.txt 2>make_err.txt
Ok!
```


6. Copy include-files:
```
$ ./copy_incs.py
```
This step is last, because some include-files generates in previous step `build` (substep `configure`).


After building need dir (for example, `libs/win32/no_lto`) will contain built static-libs (`*.a`).  
But python not built with MinGW, so uses dynamic std-version (`py_win32` contains it, will be auto copy).

***

## Fixing problems

If there are some errors, you can fix it and restart `./build.py` again.  
Logs and Errors of building you can see at `libs/sources/%lib%` in files
* `conf_out.txt` and `conf_err.txt` for configurate,
* `make_out.txt` and `make_err.txt` for make.

You can edit to fix and run files `./conf.sh` and `./make.sh` in any lib.  
After it, don't forget to open `scripts/progress_list.txt` and to change status fixed lib to `configurated` or `maked`.  
Also you can fix `scripts/%conf-or-make%/%lib%.sh` for `copy_sh.py`, that generates `*.sh`-files from this.

Status of any lib in `scripts/progress_list.txt` can set to next values:
* `start` (need to configure - substep 1/2 of building),
* `configurated` (need to make - substep 2/2 of building),
* `maked` (built, ready to use).

***

Example for building with lto after building without lto:
```
$ ./progress.py

$ ./copy_sh.py
# choose enable lto

$ ./build.py

# not need ./copy_incs.py, because include-files are common for lto and no_lto
```
