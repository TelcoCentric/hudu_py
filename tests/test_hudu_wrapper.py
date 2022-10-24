import vcr
from pytest import fixture
from dotenv import load_dotenv

load_dotenv()

from hudu_wrapper.hudu import Hudu
hudu_vcr = vcr.VCR(filter_query_parameters=['x-api-key'])

@fixture
def info_keys():
    return ['version', 'date']

@fixture
def activity_log_keys():
    return ['page']

@hudu_vcr.use_cassette('tests/vcr_cassettes/api_info.yml')
def test_info(info_keys):
    """Tests an API call to get API info"""

    h = Hudu()
    response = h.get_api_info()

    assert isinstance(response, dict)
    assert response['version'] is not None, "The version should be in the response"
    assert set(info_keys).issubset(response.keys()), "All keys should be in the response"

@hudu_vcr.use_cassette('tests/vcr_cassettes/activity_logs.yml', )
def test_activity_logs(activity_log_keys):
    """Tests an API call to activity logs"""

    h = Hudu()
    response = h.get_activity_logs(page=1)

    assert isinstance(response, dict)