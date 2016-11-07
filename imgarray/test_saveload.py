
from os.path import join
from tempfile import mkdtemp
from numpy import array_equal, iinfo, finfo, NaN, ones, dtype, inf, isnan
from numpy.random.mtrand import RandomState
from pytest import raises
from . import save_array_img, load_array_img


tmpdir = mkdtemp()


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
			path = join(tmpdir, 'test-{0:s}-{1:s}.png'.format(datatype, '-'.join(str(s) for s in size)))
			data = rescale(rs.rand(*size).astype(datatype))
			save_array_img(data, path)
			data2 = load_array_img(path)
			if len(data.shape) == 1:
				data2 = data2.reshape((data2.shape[0]),)
			assert array_equal(data, data2), 'save-load failed for {0:s}'.format(datatype)


def test_formats_NOT_IMPLEMENTED():
	# todo: this test is known not to pass; it's here to test the future implementation of other image formats
	rs = RandomState(seed=123456789)
	for format in ('bmp', 'png', 'raw', 'tiff', 'gif',):
		path = join(tmpdir, 'test-format-{0:s}.{0:s}'.format(format))
		data = rescale(rs.rand(64, 48))
		save_array_img(data, path, img_format=format)
		data2 = load_array_img(path)
		assert array_equal(data, data2)


def test_zero_dim():
	rs = RandomState(seed=123456789)
	for size in ((100, 0), (0, 100), (0, 0), (0,)):
		path = join(tmpdir, 'test-zerodim-{0:s}.png'.format('-'.join(str(s) for s in size)))
		data = rs.rand(*size)
		with raises(ValueError):
			save_array_img(data, path)


def test_lossy_format():
	rs = RandomState(seed=123456789)
	path = join(tmpdir, 'test-lossy.jpg')
	data = rs.rand(64, 48)
	with raises(TypeError):
		save_array_img(data, path, img_format='jpg')


def test_special_data():
	for datatype in ('uint8', 'int16', 'int32', 'float32', 'float64',):
		if 'int' in str(datatype):
			info = iinfo(dtype(datatype))
		elif 'float' in datatype:
			info = finfo(dtype(datatype))
		extra = ()
		if 'float' in datatype:
			extra = (NaN, -inf, inf,)
		for value in (0, 1, info.min, info.max,) + extra:
			path = join(tmpdir, 'test-value-{1:}-{0:s}.png'.format(datatype, value))
			data = ones((64, 48), dtype=datatype) * value
			save_array_img(data, path)
			data2 = load_array_img(path)
			assert ((data == data2) | (isnan(data) & isnan(data2))).all()
			
	#jpg



