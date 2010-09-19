#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    setup.py
    ~~~~~~~~
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: BSD, see LICENSE for more details.
"""

from distutils.command.build import build as _build
from setuptools import setup, find_packages
from setuptools.command.sdist import sdist as _sdist

# doing things the wrong way...
# we need the module blohg.version but we can't import the full package
# first time because the dependencies probably aren't solved yet.
import os, sys
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cwd, 'blohg'))
from version import version as __version__

cmdclass = dict()
have_babel = True

try:
    from babel.messages import frontend as babel
except ImportError:
    have_babel = False
else:
    cmdclass.update(
        compile_catalog = babel.compile_catalog,
        extract_messages = babel.extract_messages,
        init_catalog = babel.init_catalog,
        update_catalog = babel.update_catalog,
    )

class build(_build):
    def run(self):
        if have_babel:
            self.run_command('compile_catalog')
        _build.run(self)

class sdist(_sdist):
    def run(self):
        if have_babel:
            self.run_command('compile_catalog')
        _sdist.run(self)

cmdclass.update(
    build = build,
    sdist = sdist,
)

setup(
    name = 'blohg',
    version = __version__,
    license = 'BSD',
    description = 'A Mercurial-based blog engine',
    long_description = __doc__,
    author = 'Rafael Goncalves Martins',
    author_email = 'rafael@rafaelmartins.eng.br',
    url = 'http://labs.rafaelmartins.eng.br/projects/blohg',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'Flask>=0.6',
        'Flask-Babel>=0.6',
        'Flask-Themes>=0.1.2',
        'Jinja2>=2.5.2',
        'docutils>=0.7',
        'Mercurial>=1.6',
    ],
    cmdclass = cmdclass,
)
