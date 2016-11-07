
from numpy import array_equal
from numpy.random import RandomState
from imgarray import save_array_img, load_array_img

# generate some data (most types and dimensions work) that utilizes the full range
rs = RandomState(seed=123456789)
data = (2 * rs.rand(640, 48).astype('float64') - 1) * 1.7976931348623157e+308
# save the array as an image (png is the default)
save_array_img(data, 'demo.png', img_format='png')
# load the data back from the image and check that it is the same
data2 = load_array_img('demo.png')
assert array_equal(data, data2)


