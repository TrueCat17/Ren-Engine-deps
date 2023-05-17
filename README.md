## Preparing

For start, **if your OS is Windows**, you must download and install
[Cygwin](https://cygwin.com).  
* For new Windows use x86_64 installer.
* For old or/and 32-bit system (win7-x32, for example) use old unsupported (archived) x86 installer
with archived repo (see [Cygwin install page](https://cygwin.com/install.html)).

**Warning**: `setup-x86.exe` requires an option `--allow-unsupported-windows` for start on old Windows.  
You can:
* specify this from `cmd`,
* make `Shortcut` and add this option in the end of the path (after space, of course).

***

## Installing libraries

You must have installed **packages**:
`python3`, `git`, `nasm`, `autoconf`, `automake`, `libtool`, `make`, `cmake`, `gcc`, `g++`.

Example for Debian:  
`apt-get install python3 git nasm autoconf automake libtool make cmake gcc g++`

**If your OS is Linux**, you must also install:
* for audio subsystem: `libasound2-dev libpulse-dev`
* for window subsystem: `libdbus-1-dev libudev-dev libxrandr-dev libxcursor-dev libxxf86vm-dev libgl-dev`  
(or just `xorg-dev`, but it is not only needed packages).

**If your OS is Windows**:
* additionally install `mingw64-i686-gcc-core`,
* select common `automake` - with unspecifed version,
* make sure that you have `i686-pc-cygwin-g++` (compiler for 32-bit) after installing.

***

## Building

0. Make sure you have 1.5 GB of free space.


1. Open shell and change dir to `scripts`:
```
$ cd Ren-Engine/libs/scripts
```
Note: `C:/` in Cygwin is `/cygdrive/c/`.


2. Check that the programs are installed and the libraries are ready to be built:
```
$ ./check.py
Ok.
```
Install programs if you forgot to do it earlier.


3. Set <start> status for all libs (in file `progress_list.txt`):
```
$ ./progress.py
```


4. Copy files (bash-scripts) to building libs:
```
$ ./copy_sh.py
```
Here you can choose platform (x32 or x64), enable/disable optimisations that makes building slower, etc...  
Some options available only for Linux.  
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


5. Copy include-files:
```
$ ./copy_incs.py
```
This step is last, because some include-files generates in previous step `build` (substep `configure`).


After building need dir (for example, `libs/win32/no_lto`) will contain built static-libs (`*.a`).

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
```
Not need `./copy_incs.py`, because include-files are common for `lto` and `no_lto`.
