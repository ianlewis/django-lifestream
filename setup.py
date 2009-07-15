from distutils.core import setup, find_packages
 
setup(
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
    packages=find_packages(),
)
