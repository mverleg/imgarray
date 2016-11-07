
from logging import warning
from PIL import PngImagePlugin
from PIL.Image import frombytes, open
from numpy import ndarray, frombuffer, dtype
from os.path import isfile
from math import ceil


META_DESCRIPTION = 'This image encodes {0:s} {1:d}x{2:d} array data.'
META_SOFTWARE = 'Saved/loadable with "imgarray" at "github.com/mverleg/imgarray".'


def save_array_img(mat, path, img_format='png'):
	"""
	Save numpy ndarray as an image.
	
	:param mat: Two-dimensional ndarray to be saved.
	:param path: The path to save the image at.
	"""
	assert isinstance(mat, ndarray)
	if mat.size <= 0:
		raise ValueError('Cannot store arrays without elements as image')
	if len(mat.shape) == 1:
		mat = mat.reshape((mat.shape[0], 1))
	assert len(mat.shape) == 2
	if img_format not in {'bmp', 'png', 'raw', 'tiff', 'gif',}:
		raise TypeError('only lossless image formats that have metadata are supported, '
			'otherwise data gets corrupted (in ways that do not approximate the original data)')
	assert img_format == 'png', 'only png is implemented (metadata not yet implemented for others)'  # todo
	sz = mat.dtype.itemsize
	assert ((sz & (sz - 1)) == 0), 'only powers of two bytes per cell are supported'
	img_width = mat.shape[0]
	img_height = int(ceil(mat.shape[1] * sz / 4.))
	meta = PngImagePlugin.PngInfo()
	meta.add_text('Description', META_DESCRIPTION.format(str(mat.dtype), *mat.shape))
	meta.add_text('Software', META_SOFTWARE)
	meta.add_text('dtype', str(mat.dtype))
	padding = b''
	if sz < 4:
		pad_len = int(img_width * img_height * 4 - mat.size * sz)
		padding = b'\00' * pad_len
		meta.add_text('padding', str(pad_len))
	data = mat.tobytes() + padding
	img = frombytes(mode='RGBA', size=(img_width, img_height), data=data)
	img.save(path, format=img_format, pnginfo=meta)


def load_array_img(path, is_int=False):
	"""
	Load an image-encoded numpy ndarray.
	
	:param path: The path the image is saved at.
	:param is_int: Whether the data are integers (otherwise floats).
	:return: The two-dimensional numpy array encoded by the image.
	"""
	if not isfile(path):
		raise IOError('image array file "{0:s}" not found'.format(path))
	img = open(path)
	if 'dtype' not in img.info:
		warning('png metadata missing or corrupted, cannot determine original data type, using float64')
	datatype = dtype(img.info.get('dtype', 'float64'))
	sz = datatype.itemsize
	if 'padding' not in img.info and sz < 4:
		raise IOError('png metadata missing or corrupted, making assumptions about the shape of the data, this may lead to errors')
	pad_len = int(img.info.get('padding', 0))
	mat_width = img.size[0]
	mat_height = int((img.size[1] * 4 - pad_len / mat_width) / sz)
	mat = frombuffer(img.tobytes(), dtype=datatype, count=mat_width * mat_height)
	mat = mat.reshape((mat_width, mat_height))
	return mat


