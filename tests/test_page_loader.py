import tempfile
import page_loader as p


def test_name():
    assert p.name('https://ru.hexlet.io/courses') == \
        'ru-hexlet-io-courses.html'
    assert p.name('https://vk.com/username') == 'vk-com-username.html'


def test_download_path():
    with tempfile.TemporaryDirectory() as tmpdirname:
        path = p.download('https://ru.hexlet.io/courses', tmpdirname)
        assert path == tmpdirname + '/ru-hexlet-io-courses.html'


def test_download_file(requests_mock):
    requests_mock.get('http://test.com', text='data')
    with tempfile.TemporaryDirectory() as tmpdirname:
        p.download('http://test.com', tmpdirname)
        expected = open('tests/fixtures/expected.html').read()
        current = open(tmpdirname + '/test-com.html').read()
        assert expected == current
