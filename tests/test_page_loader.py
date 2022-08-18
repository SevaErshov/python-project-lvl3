import tempfile
import page_loader as p
from os.path import exists


def test_name():
    assert p.name('https://ru.hexlet.io/courses') == \
        'ru-hexlet-io-courses'
    assert p.name('https://vk.com/username') == 'vk-com-username'
    assert p.name('https://anything.com/pic.html') == 'anything-com-pic'
    assert p.name('http://test.com') == 'test-com'


def test_download_path(requests_mock):
    requests_mock.get('https://ru.hexlet.io/courses', text='data')
    with tempfile.TemporaryDirectory() as tmpdirname:
        path = p.download('https://ru.hexlet.io/courses', tmpdirname)
        assert path == tmpdirname + '/ru-hexlet-io-courses.html'


def test_download_file(requests_mock):
    text = open('tests/fixtures/expected.html').read()
    requests_mock.get('http://test.com', text=text)
    with tempfile.TemporaryDirectory() as tmpdirname:
        p.download('http://test.com', tmpdirname)
        expected = open('tests/fixtures/expected.html').read()
        current = open(tmpdirname + '/test-com.html').read()
        assert expected == current


def test_download_pics(requests_mock):
    text = open('tests/fixtures/pic.html').read()
    requests_mock.get('http://test.com/picture', text=text)
    pic = open('tests/fixtures/some/beautiful/pic.png', 'rb').read()
    requests_mock.get('http://test.com/some/beautiful/pic.png', content=pic)
    second_pic = open('tests/fixtures/pics.jpg', 'rb').read()
    requests_mock.get('http://test.com/any/pics.jpeg', content=second_pic)
    expected_pic = open('tests/fixtures/expected_pic.html', 'r').read()
    with tempfile.TemporaryDirectory() as tmpdirname:
        p.download('http://test.com/picture', tmpdirname)
        current = open(tmpdirname + '/test-com-picture.html').read()
        new_dir = tmpdirname + "/test-com-picture_files"
        new_file = new_dir + "/test-com-picture-some-beautiful-pic.png"
        new_file1 = new_dir + "/test-com-picture-any-pics.png"
        assert exists(new_dir)
        assert exists(new_file)
        assert exists(new_file1)
        assert expected_pic == current


def test_bad_images(requests_mock):
    text = open('tests/fixtures/bad_images.html').read()
    requests_mock.get('https://test.com/picture', text=text)
    expected = open('tests/fixtures/bad_images.html').read()
    with tempfile.TemporaryDirectory() as tmpdirname:
        p.download('https://test.com/picture', tmpdirname)
        current = open(tmpdirname + '/test-com-picture.html').read()
        new_dir = tmpdirname + "/test-com-picture_files"
        assert not exists(new_dir)
        assert expected == current
