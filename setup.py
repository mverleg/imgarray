# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.rst', 'r') as fh:
	readme = fh.read()

setup(
	name='imgarray',
	description='Save and load numpy arrays as PNG images',
	long_description=readme,
	url='https://github.com/mverleg/imgarray',
	author='Mark V',
	maintainer='(the author)',
	author_email='mdilligaf@gmail.com',
	license='Revised BSD License (LICENSE.txt)',
	keywords=['numpy', 'png', 'pillow',],
	version='1.0',
	packages=['imgarray'],
	include_package_data=True,
	zip_safe=False,
	classifiers=[
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
	install_requires=[
		'numpy',
		'pillow',
	],
)


