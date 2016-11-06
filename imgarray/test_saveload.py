
from os.path import join
from tempfile import mkdtemp
from numpy import array_equal
from numpy.random.mtrand import RandomState
from .saveload import save_array_img, load_array_img


def test_2D():
	rs = RandomState(seed=123456789)
	for datatype in ('uint8', 'int16', 'int32', 'float32', 'float64',):
		for width, height in ((100, 40), (5, 5), (60, 37), (13, 5000),):
			path = join(mkdtemp(), 'testmat-{0:s}-{1:d}-{2:d}.png'.format(datatype, width, height))
			data = rs.randn(width, height).astype(datatype)
			save_array_img(data, path)
			data2 = load_array_img(path)
			assert array_equal(data, data2), 'save-load failed for {0:s}'.format(datatype)


#todo: test NaNs
#todo: test invalid input (like (0, 0) arrays)


