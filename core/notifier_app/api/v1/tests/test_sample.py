import pytest


@pytest.mark.django_db
class TestSample:
    def test_sample(self):
        assert True == True
