## What is SConf?

Working as companion to [SCons](http://www.scons.org/), **SConf** can be used to generate compile time configurations for Kconfig based software. It is a GUI frontend for [Kconfiglib](https://github.com/ulfalizer/Kconfiglib), written in Python with Tkinter. Users are recommended to write the configuration files with *SConfigure* as their names, in analogy to the name of *SConstruct* and *SConscript* in SCons world (although they can be named whatever you like, having a *similar* naming looks more beautiful to me). Maybe someday it could be integrated with Scons!

## Why do SConf?

During some days when I was working on a small software project which was based on **SCons** to build, it worked quite well until I tried to add some compile time configurations. I had been addicted to the Kconfig based work flow, but tired on making Makefiles where Scons played very well, so I initially wanted to *homebrew* some Kconfig parser with Python then use that for this *SConf*. Doing some Google search, I quickly found [Kconfiglib](https://github.com/ulfalizer/Kconfiglib) which is Copyright (c) of *Ulf Magnusson*. This would save me a lot of time reinventing the wheel. So I started from **Kconfiglib** and renamed *kconfiglib.py* to *kconf.py* for my favor of naming in this context (hope *Ulf Magnusson* doesn't mind this renaming).

## How to use SConf?

Just copy the *sconf.py* and *kconf.py* into the root directory of source tree, then call python:

```console

    $ python sconf.py SConfigure 

```

## How to debug SConf?

The Python script `scopy.py` can be used to copy files with specific name pattern `pat` from `src` directory tree to `dst` directory tree. For example, you can use it to copy the `Kconfig` files in the whole Linux Kernel to `SConf/linux` so that can be used to test our `sconf.py` without going to the original Linux Kernel tree. The following is the work flow that I used to debug SConf for Linux Kernel. The same procedure can be used to debug other projects. 

```console

	$ git clone https://github.com/CoryXie/SConf.git SConf
	$ cd SConf
	$ python scopy.py ../linux-4.2 ./linux Kconfig*
	$ cd linux
	$ KERNELVERSION=4.2 ARCH=arm64 SRCARCH=arm64 python ../sconf.py Kconfig
	$ cd ..; rm -rf linux # before you want to commit changes for SConf itself

```

Note that the in the pattern `Kconfig*`, the `*` is used to make sure things such as `Kconfig.debug` in the Kernel are also copied. In other projects you may have other config file naming such as what we recommended `SConfigure`, then you should adapt.

Of course, in practice you will use **Sconf** by copying `sconf.py`/`kconf.py` into the source tree and run `sconf.py` in the source tree. This script is used for **SConf** development purpose.


## Status

Right now the following features have been implemented:

* Loads the configuration tree into the GUI.
* Double clicking on `bool` config options to toggle between `y` and `n` (with dependencies updated both in `kconf` database and in GUI).
* Double clicking on `tristate` config options to toggle between `y`, `m` and `n` (with dependencies updated both in `kconf` database and in GUI), like this : `y->m->n->y->m->n->...`
* Double clicking on `int/hex/string` config options will populate `PopupWindow` to get and update the config option values.
* Info bar to notify the current actions/status.
* Menu bar buttons to save configuration (both `.config` and `config.h`) and exit.

I think we can quickly evolve it into a working **make xconfig** style work flow.

## License

Copyright (c) 2011-2015, Ulf Magnusson ulfalizer@gmail.com

Copyright (c) 2015, Cory Xie cory.xie@gmail.com

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.