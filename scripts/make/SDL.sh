#!/bin/bash
set -e

make -j4
cp ./build/.libs/libSDL2main.a ../000res
if [ -f ./build/.libs/SDL2.dll ] ; then
	cp ./build/.libs/SDL2.dll ../000res
else
	cp ./build/.libs/libSDL2.a ../000res
fi

# remove -lmingw32 and -Dmain=SDL_main from sdl2-config
sed -e "s/-lmingw32//" sdl2-config > sdl2-config.new
sed -e "s/-Dmain=SDL_main//" sdl2-config.new > sdl2-config
rm sdl2-config.new
chmod +x sdl2-config
