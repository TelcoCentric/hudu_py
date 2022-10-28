# hudu_py
 Python wrapper for Hudu API

Work in progress. If you want to contribute, feel free to.



pip install hudu-py

from hudu_py.API import Hudu

hudu = Hudu(
    api_key = HUDU_API_KEY, 
    domain = HUDU_DOMAIN, 
    api_version = HUDU_API_VERSION
)

api_info = hudu.get_api_info()