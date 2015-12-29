## What is SConf?

Working as companion to [SCons](http://www.scons.org/), **SConf** can be used to generate compile time configurations for Kconfig based software. It is a GUI frontend for [Kconfiglib](https://github.com/ulfalizer/Kconfiglib), written in Python with Tkinter. Users are recommended to write the configuration files with *SConfigure* as their names, in analogy to the name of *SConstruct* and *SConscript* in SCons world (although they can be named whatever you like, having a *similar* naming looks more beautiful to me). Maybe someday it could be integrated with Scons!

## Why do SConf?

During some days when I was working on a small software project which was based on **SCons** to build, it worked quite well until I tried to add some compile time configurations. I had been addicted to the Kconfig based work flow, but tired on making Makefiles where Scons played very well, so I initially wanted to *homebrew* some Kconfig parser with Python then use that for this *SConf*. Doing some Google search, I quickly found [Kconfiglib](https://github.com/ulfalizer/Kconfiglib) which is Copyright (c) of *Ulf Magnusson*. This would save me a lot of time reinventing the wheel. So I started from **Kconfiglib** and renamed *kconfiglib.py* to *kconf.py* for my favor of naming in this context (hope *Ulf Magnusson* doesn't mind this renaming).

## How to use SConf?

Just copy the *sconf.py* and *kconf.py* into the root directory of source tree, then call python:

```console

    $ python sconf.py SConfigure 

```

## Status

Right now it barely loads the configuration tree into the GUI and can perform some config option changes but I think we can quickly evolve it into a working **make xconfig** style work flow.

## License

Copyright (c) 2011-2015, Ulf Magnusson ulfalizer@gmail.com

Copyright (c) 2015, Cory Xie cory.xie@gmail.com

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.