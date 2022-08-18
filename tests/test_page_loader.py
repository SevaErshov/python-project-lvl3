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
    requests_mock.get("http://test.com/piclol.png", content=second_pic)
    expected_pic = open('tests/fixtures/expected_pic.html', 'r').read()
    with tempfile.TemporaryDirectory() as tmpdirname:
        p.download('http://test.com/picture', tmpdirname)
        current = open(tmpdirname + '/test-com-picture.html').read()
        new_dir = tmpdirname + "/test-com-picture_files"
        new_file = new_dir + "/test-com-some-beautiful-pic.png"
        new_file1 = new_dir + "/test-com-any-pics.jpeg"
        new_file2 = new_dir + "/test-com-piclol.png"
        assert exists(new_dir)
        assert exists(new_file)
        assert exists(new_file1)
        assert exists(new_file2)
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


def test_with_link(requests_mock):
    text = open('tests/fixtures/page_with_link.html').read()
    requests_mock.get('https://test.com/links', text=text)
    js = open('tests/fixtures/runtime.js', 'rb').read()
    nodepng = open('tests/fixtures/nodejs.png', 'rb').read()
    css = open('tests/fixtures/application.css', 'rb').read()
    new_page = open('tests/fixtures/courses.html').read()
    requests_mock.get('https://test.com/courses', text=new_page)
    requests_mock.get('https://test.com/assets/application.css', content=css)
    nodejs_path = 'https://test.com/assets/professions/nodejs.png'
    requests_mock.get(nodejs_path, content=nodepng)
    requests_mock.get('https://test.com/packs/js/runtime.js', content=js)
    expected = open('tests/fixtures/expected_with_link.html').read()
    with tempfile.TemporaryDirectory() as tmpdirname:
        p.download('https://test.com/links', tmpdirname)
        current = open(tmpdirname + '/test-com-links.html').read()
        new_dir = tmpdirname + '/test-com-links_files'
        new_file = new_dir + "/test-com-courses.html"
        new_file1 = new_dir + "/test-com-assets-application.css"
        new_file2 = new_dir + "/test-com-assets-professions-nodejs.png"
        new_file3 = new_dir + "/test-com-packs-js-runtime.js"
        assert exists(new_dir)
        assert exists(new_file2)
        assert exists(new_file3)
        assert exists(new_file1)
        assert exists(new_file)
        assert expected == current
