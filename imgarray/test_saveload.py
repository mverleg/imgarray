
from os.path import join
from tempfile import mkdtemp
from numpy import array_equal, iinfo, finfo
from numpy.random.mtrand import RandomState
from . import save_array_img, load_array_img


def rescale(var):
	if 'int' in str(var.dtype):
		info = iinfo(var.dtype)
	elif 'float' in str(var.dtype):
		info = finfo(var.dtype)
	else:
		raise NotImplementedError()
	return var * info.max - info.min // 2


def test_shapes_types():
	rs = RandomState(seed=123456789)
	for datatype in ('uint8', 'int16', 'int32', 'float32', 'float64',):
		for size in ((100, 40), (5, 5), (60, 37), (13, 5000), (1, 100), (100, 1), (100,), (1,)):
			path = join(mkdtemp(), 'testmat-{0:s}-{1:s}.png'.format(datatype, '-'.join(str(s) for s in size)))
			data = rescale(rs.rand(*size).astype(datatype))
			save_array_img(data, path)
			data2 = load_array_img(path)
			if len(data.shape) == 1:
				data2 = data2.reshape((data2.shape[0]),)
			assert array_equal(data, data2), 'save-load failed for {0:s}'.format(datatype)


def test_formats():
	rs = RandomState(seed=123456789)
	for format in ('bmp', 'png', 'raw', 'tiff', 'gif',):
		path = join(mkdtemp(), 'testmat-{0:s}.{0:s}'.format(format))
		data = rescale(rs.rand(640, 480))
		save_array_img(data, path, img_format=format)
		data2 = load_array_img(path)
		assert array_equal(data, data2)


def test_special_cases():
	pass
	#zeros
	#(0, 0)
	#data *= iinfo(im.dtype).max
	#NaNs
	#jpg



