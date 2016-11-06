
from logging import warning
from PIL import PngImagePlugin
from PIL.Image import frombytes, open
from numpy import ndarray, frombuffer, dtype
from os.path import isfile
from math import ceil


def save_array_img(mat, path):
	"""
	Save numpy ndarray as an image.
	
	:param mat: Two-dimensional ndarray to be saved.
	:param path: The path to save the image at.
	"""
	assert isinstance(mat, ndarray)
	assert mat.size > 0, 'cannot store arrays without elements as image'
	assert len(mat.shape) == 2
	sz = mat.dtype.itemsize
	assert ((sz & (sz - 1)) == 0), 'only powers of two bytes per cell are supported'
	width = mat.shape[0]
	height = int(ceil(mat.shape[1] * sz / 4.))
	pad_len = int(width * height * 4 / sz - mat.size)
	print('>', mat.shape[0], mat.shape[1], width, height, pad_len)
	padding = b'\00' * pad_len
	meta = PngImagePlugin.PngInfo()
	meta.add_text('dtype', str(mat.dtype))
	meta.add_text('padding', str(pad_len))
	data = mat.tobytes() + padding
	img = frombytes(mode='RGBA', size=(width, height), data=data)
	img.save(path, format='png', pnginfo=meta)


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
		warning('png metadata got corrupted, cannot determine original data type, using float64')
	datatype = dtype(img.info.get('dtype', 'float64'))
	pad_len = int(img.info.get('padding', 0))
	sz = datatype.itemsize
	width = img.size[0]
	height = int(img.size[1] * 4. / sz - float(pad_len) / img.size[0])
	print('<', img.size[0], img.size[1], width, height, pad_len)
	mat = frombuffer(img.tobytes(), dtype=datatype, count=4*img.size[0]*img.size[1]-pad_len)
	print(mat.dtype, mat.shape, (width, height))
	mat = mat.reshape((width, height))
	return mat


