====================================
DDL Incubator 3, Team 7, Censusables
====================================



Build notes
===========

For starters, I (Jim) expect us (or at least the Python enthusiasts
among us) to use some combination of scikit-learn, pandas, and
matplotlib.  We'll use the requests library for calling APIs for
downloading data.

I'm a fan of `zc.buildout <http://buildout.org>`_ for managing
software. It's similar to pip, except it can do much more than just
downloading Python packages.  It also makes it easy to automate the
creation of sctipts and other tools as part of a project.  I'll
definately be using it and my buildout configuration will be available
for others to use as well.

I'm also a big fan of not mixing package installs from different
projects together.  2 tools that can help with this are `virtualenv
<https://virtualenv.pypa.io/en/latest/>`_ and buildout.

I recommend starting with virtualenv. First install it using Python
2.7, any way you can.  Then make a virtual environment::

    virtualenv-2.7 ENV

where ENV is a directory name where you want things to be installed.

For Mac and Linux, you need development tools and libraries installed.
I had to install a Fortran compiler by installing gcc with Homebrew.
I suspect this won't be an issue on Linux, assuming you have gcc
installed.  For Windows, pip and buildout will be downloading binary
distributions.

Install various interesting packages::

  ENV/bin/pip install requests
  ENV/bin/pip install numpy
  ENV/bin/pip install scipy
  ENV/bin/pip install scikit-learn
  ENV/bin/pip install pandas
  ENV/bin/pip install matplotlib

On Mac or Linux, you may run into issues when installing some of
these, especially matplotlib. (You may have issues on Windows, but I
can't really help there.) On my personal mac, which already had lots
of likely dependencies installed, I had to install gcc (for Fortran)
and freetype. (BTW, on Macs I recommend installing 3rd-party bits with
Homebrew.)

I've also provided a buildout configuration, empty initially.  I'd go
ahead and get it set up with::

  ENV/bin/python bootstrao.py
  bin/python


To get a Python prompt with the data anysis tools importable::

  ENV/bin/python
