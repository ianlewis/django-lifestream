#!/usr/bin/env python

from setuptools import setup, find_packages
 
setup (
    name='django-lifestream',
    version='0.1',
    description='A lifestream application for Django.',
    author='Ian Lewis',
    author_email='IanMLewis@gmail.com',
    url='http://code.google.com/p/django-lifestream-2/',
    license='MIT License',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Environment :: Plugins',
      'Framework :: Django',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires = [
        'Django>=1.1',
        'BeautifulSoup==3.2.0',
        'dateutils==0.4.1',
        'feedparser>=5.0',
    ],
    packages=find_packages(),
    test_suite='tests.main',
)
