# funkcja startująca przed każdym testem
import pytest


@pytest.fixture(autouse=True)
def no_request(monkeypatch):
    monkeypatch.delattr('requests.sessions.Session.request')


@pytest.fixture
def backend(tmpdir):
    temp_file = tmpdir.join('test.txt')
    temp_file.write('')
    return temp_file
