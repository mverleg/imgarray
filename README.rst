imgarray (Python)
---------------------------------------

This stores 1D and 2D numpy arrays as png images. As a method of storage, not visualization (use pillow_ for that).

Q: Why would you ever want that?

* It's somewhat, though not extremely, space-efficient.
* Saving and loading PNGs is supported by many languages, so all you need to do is port this library.
* Results look kind of funny, nothing too interesting though.
* Because you can.

Installation
---------------------------------------

This package requires `numpy` and `pillow`. They will be installed automatically if you install using pip:

.. code-block:: bash

	pip install imgarray

Usage
---------------------------------------

Usage is very simple, there are only two functions:

.. code-block:: python

	from imgarray import save_array_img, load_array_img
	data = randn((500, 500)).astype(int16)
	save_array_img(data, path)
	data2 = load_array_img(path)

You can check out the tests for more (not a lot more to be fair).

Notes
---------------------------------------

* 1D arrays will be returned as 2D arrays with one unit dimension, because all data
* It works with most numpy data types (specifically, the ones that use a number of bytes which is a power of 2)
* If you remove metadata from the PNG, the file only loads correctly if the data was float64, and you'll also get a warning.

Usage & contributions
---------------------------------------

Revised BSD License; at your own risk, you can mostly do whatever you want with this code, just don't use my name for promotion and do keep the license file.

Pull requests are welcome, especially with unit tests. Due to the great importance of this library, maintenance is not going to be high-priority.


.. _pillow: https://python-pillow.org/


