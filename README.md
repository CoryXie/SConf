## What is SConf?

Working as companion to [SCons](http://www.scons.org/), **SConf** can be used to generate compile time configurations for **Kconfig** based software. It is a GUI frontend for [Kconfiglib](https://github.com/ulfalizer/Kconfiglib), written in Python with Tkinter. Users are recommended to write the configuration files with *SConfigure* as their names, in analogy to the name of *SConstruct* and *SConscript* in SCons world (although they can be named whatever you like, having a *similar* naming looks more beautiful to me). Maybe someday it could be integrated with Scons!

Note, however, **Sconf** is not bound to **SCons**, we just think it is a good example to use it as a companion to **SCons**. You can use it in anyway you like, only requiring you to follow **Kconfig** semantics to write the config options. There are `.config`, `config.h` and `config.py` files generated for you to include in either source files or **SCons** *SConstruct* file for conditional compilation.

## Why do SConf?

During some days when I was working on a small software project which was based on **SCons** to build, it worked quite well until I tried to add some compile time configurations. I had been addicted to the Kconfig based work flow, but tired on making Makefiles where Scons played very well, so I initially wanted to *homebrew* some Kconfig parser with Python then use that for this *SConf*. Doing some Google search, I quickly found [Kconfiglib](https://github.com/ulfalizer/Kconfiglib) which is Copyright (c) of *Ulf Magnusson*. This would save me a lot of time reinventing the wheel. So I started from **Kconfiglib** and renamed *kconfiglib.py* to *kconf.py* for my favor of naming in this context (hope *Ulf Magnusson* doesn't mind this renaming).

## How to use SConf?

Just copy the *sconf.py* and *kconf.py* into the root directory of source tree, then call python:

```console

    $ python sconf.py SConfigure 

```

After doing the configure actions, you may press the button to **Save Config**, which will save `.config`, `config.h` and `config.py`. You can use these generated configuration files as you wish.

Specially, when you want to use **SCons** with the **Sconf** generated `config.py`, you may need to import and use the `config.py` like this in the top level `SConstruct`:

```python

    import config 
    
    conf = config.Configuration() # Create instance of Configuration class
    
    env_options = {
        "CC"    : conf.CONFIG_CROSS_COMPILE + "gcc", # Use `conf` variable to access config options
        "CXX"   : conf.CONFIG_CROSS_COMPILE + "g++",
        "LD"    : conf.CONFIG_CROSS_COMPILE + "g++",
        "AR"    : conf.CONFIG_CROSS_COMPILE + "ar",
        "STRIP" : conf.CONFIG_CROSS_COMPILE + "strip"
    }
    
    env = Environment(**env_options)
    
    env.Append(ENV = {'PATH' : os.environ['PATH']})
    
    Export('env')
    Export('conf') # Like `env`, we export `conf` for subdir SConscripts
    
    env.SConscript('subdir1/SConscript')

    # If you do not use the Export('env') and Export('conf') above, you
    # may do the following to export the variables to specific subdirs.  

    env.SConscript('subdir2/SConscript', {'env': env, 'conf': conf})

    ...

```

Then in the other subdir `SConscript`s, you can do the following to import the `env` and `conf` then use them as normal.

```python
    
    Import('env')
    Import('conf')
    
    print conf.CONFIG_CROSS_COMPILE

```

## Special Enhancements for writting Kconfig or SConfigure files

You may want to have different *prefix* to be added before the generated options, or you may want to specify the directory to put the generated header file. To make it more flexible to accomendate various usages for different software projects, we have implemented some special enhancments to writting Kconfig or SConfigure files.

1) You can use the `KCONFIG_PREFIX` config option in your *Kconfig* or *SConfigure* files to specify prefix for the generated config options. 

```c

	config KCONFIG_PREFIX
		string
		default "_SUPER_CONFIG_"
	
	config FOO
		int "Foo Value"
		default 10

```

With the above `KCONFIG_PREFIX` the generated option for `FOO` will be `_SUPER_CONFIG_FOO`. But if you say `default ""` then the generated option for `FOO` would be just `FOO`. This is useful for projects which would want to use the same option names in both *Kconfig* files and source code files (so that is easier to grep, for example), in this case, you can set `KCONFIG_PREFIX` to `default ""` and other options with full name such as `CONFIG_FOO`.

2) You can use the `KCONFIG_HEADER_DIR` config option to specify the directory to put the generated header file. Note that this directory is relative to the base directory where you put the root *Kconfig* or *SConfigure* files.

```c

	config KCONFIG_HEADER_DIR
		string
		default "include/config"

```

With this `KCONFIG_HEADER_DIR` config option the generated `config.h` file will be in `$PROJECT_ROOT/include/config/config.h`. If you say `KCONFIG_HEADER_DIR` to be `""` or `"."` then it will generate the `config.h` as `$PROJECT_ROOT/config.h`.

Note that currently `.config` and `config.py` are always generated in the `$PROJECT_ROOT` directory where you put root *Kconfig* or *SConfigure* files.

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

Note that in the pattern `Kconfig*`, the `*` is used to make sure things such as `Kconfig.debug` in the Kernel are also copied. In other projects you may have other config file naming such as what we recommended `SConfigure`, then you should adapt.

Of course, in practice you will use **Sconf** by copying `sconf.py`/`kconf.py` into the source tree and run `sconf.py` in the source tree. This script is used for **SConf** development purpose.


## Status

Right now the following features have been implemented:

* Loads the configuration tree into the GUI.
* Double clicking on `bool` config options to toggle between `y` and `n` (with dependencies updated both in `kconf` database and in GUI).
* Double clicking on `tristate` config options to toggle between `y`, `m` and `n` (with dependencies updated both in `kconf` database and in GUI), like this : `y->m->n->y->m->n->...`
* Double clicking on `int/hex/string` config options will populate `PopupWindow` to get and update the config option values.
* Info bar to notify the current actions/status.
* Menu bar to save configuration (including `.config`, `config.h` and `config.py`) and exit.

I think most **make xconfig** style work flow is there, although we would definitely want to optimize it further.

## License

Copyright (c) 2011-2015, Ulf Magnusson ulfalizer@gmail.com

Copyright (c) 2015, Cory Xie cory.xie@gmail.com

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.