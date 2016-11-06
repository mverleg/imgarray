
from os.path import join
from tempfile import mkdtemp
from numpy import array_equal
from numpy.random.mtrand import RandomState
from . import save_array_img, load_array_img


def test_all():
	rs = RandomState(seed=123456789)
	for datatype in ('uint8', 'int16', 'int32', 'float32', 'float64',):
		for size in ((100, 40), (5, 5), (60, 37), (13, 5000), (1, 100), (100, 1), (100,), (1,)):
			path = join(mkdtemp(), 'testmat-{0:s}-{1:s}.png'.format(datatype, '-'.join(str(s) for s in size)))
			data = rs.randn(*size).astype(datatype)
			save_array_img(data, path)
			data2 = load_array_img(path)
			if len(data.shape) == 1:
				data2 = data2.reshape((data2.shape[0]),)
			assert array_equal(data, data2), 'save-load failed for {0:s}'.format(datatype)


#todo: test NaNs
#todo: test invalid input (like (0, 0) arrays)


