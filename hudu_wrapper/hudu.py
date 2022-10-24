import datetime
import requests
import json
from enum import Enum
import os

class Hudu(object):

    class FieldType(Enum):
        TEXT = 'Text'
        RICHTEXT = 'RichText'
        HEADING = 'Heading'
        CHECKBOX = 'CheckBox'
        WEBSITE = 'Website'
        PASSWORD = 'Password'
        EMAIL = 'Email'
        NUMBER = 'Number'
        DATE = 'Date'
        DROPDOWN = 'Dropdown'
        EMBED = 'Embed'
        PHONE = 'Phone'
        ASSETLINK = 'AssetLink'
        ASSETTAG = 'AssetTag'

    class Field():
        def __init__(self, label: str, show_in_list: bool, required: bool, field_type: Enum, min: int = None, max: int = None, hint: str = None, options: str = None, position: int = None, expiration: bool = False, linkable_id: int = None):
            self.label = label
            self.min = min
            self.max = max
            self.show_in_list = show_in_list
            self.required = required
            self.field_type = field_type.value
            self.hint = hint
            self.options = options
            self.posistion = position
            self.expiration = expiration
            self.linkable_id = linkable_id

    ENDPOINT_ARTICLES = 'articles'
    ENDPOINT_ACTIVITY_LOGS = 'activity_logs'
    ENDPOINT_API_INFO = 'api_info'
    ENDPOINT_ASSET_LAYOUTS = 'asset_layouts'
    ENDPOINT_ASSET_PASSWORDS = 'asset_passwords'
    ENDPOINT_ASSETS = 'assets'
    ENDPOINT_CARDS_LOOKUP = 'cards/lookup'
    ENDPOINT_CARDS_JUMP = 'cards/jump'
    ENDPOINT_COMPANIES = 'companies'
    ENDPOINT_COMPANIES_JUMP = 'companies/jump'
    ENDPOINT_EXPIRATIONS = 'expirations'
    ENDPOINT_FOLDERS = 'folders'
    ENDPOINT_MAGIC_DASH = 'magic_dash'
    ENDPOINT_PROCEDURES = 'procedures'
    ENDPOINT_RELATIONS = 'relations'
    ENDPOINT_WEBSITES = 'websites'

    ENDPOINT_ARCHIVE = 'archive'
    ENDPOINT_UNARCHIVE= 'unarchive'

    def __init__(self, api_key=None, domain=None, api_version=None):

        if api_key is None: api_key = os.environ.get('HUDU_API_KEY', None)
        if domain is None: domain = os.environ.get('HUDU_DOMAIN', None)
        if api_version is None: api_version = os.environ.get('HUDU_API_VERSION', "v1")

        self.headers = {
            "x-api-key": api_key
        }
        self.domain = domain
        self.api_version = api_version

    @property
    def base_url(self):
        return f'https://{self.domain}/api/{self.api_version}'

    def __to_format(self, response):
        return response.json()

    def __get(self, url: str, params=None):
        return self.__to_format(requests.get(url, headers=self.headers, params=params))

    def __post(self, url: str, data=None):
        return self.__to_format(requests.post(url, headers=self.headers, data=data))

    def __put(self, url: str, data=None):
        return self.__to_format(requests.put(url, headers=self.headers, data=data))

    def __delete(self, url: str):
        return self.__to_format(requests.delete(url, headers=self.headers))

    ###
    # Activity logs
    ###

    def get_activity_logs(self, page: int = None, user_id: int = None, user_email: str = None, resource_id: int = None, resource_type: str = None, action_message: str = None, start_date: datetime = None, page_size:int = None):
        params = {}

        if resource_id is not None and resource_type is None:
            # REE
            resource_id = None
            message = "resource id. Must be coupled with resource_type"
        if resource_type is not None and resource_id is None:
            # ALSO REE
            resource_type = None
            message = "resource type (Asset, AssetPassword, Company, Article, etc.). Must be coupled with resource_id"
        
        if page is not None: params['page'] = page
        if user_id is not None: params['user_id'] = user_id
        if user_email is not None: params['user_email'] = user_email
        if resource_id is not None: params['resource_id'] = resource_id
        if resource_type is not None: params['resource_type'] = resource_type
        if action_message is not None: params['action_message'] = action_message
        if start_date is not None: params['start_date'] = start_date.isoformat() #Must be in ISO 8601 format
        if page_size is not None: params['page_size'] = page_size

        return self.__get(f'{self.base_url}/{Hudu.ENDPOINT_ACTIVITY_LOGS}')

    ###
    # Api info
    ###

    def get_api_info(self):
        return self.__get(f'{self.base_url}/{Hudu.ENDPOINT_API_INFO}')

    ###
    # ARTICLES
    ###
    def get_articles(self, name: str = None, company_id: int = None, page: int = None, draft: bool = None, page_size: int = None):
        params = {}

        if name is not None: params['name'] = name
        if company_id is not None: params['company_id'] = company_id
        if page is not None: params['page'] = page
        if draft is not None: params['draft'] = draft
        if page_size is not None: params['page_size'] = page_size

        return self.__get(f'{self.base_url}/{Hudu.ENDPOINT_ARTICLES}', json.dumps(params))

    def get_article(self, id):
        return self.__get(f'{self.base_url}/{Hudu.ENDPOINT_ARTICLES}/{id}')

    def create_article(self, name: str, content: str, enable_sharing: bool = None, folder_id: int = None, company_id: int = None):
        data = {
            'article': {}
        }

        data['article']['name'] = name
        data['article']['content'] = content
        if enable_sharing is not None: data['article']['enable_sharing'] = enable_sharing
        if folder_id is not None: data['article']['folder_id'] = folder_id
        if company_id is not None: data['article']['company_id'] = company_id
        
        return self.__post(f'{self.base_url}/{Hudu.ENDPOINT_ARTICLES}', json.dumps(data))
            
    def update_article(self, id: int, name: str, content: str, enable_sharing: bool = None, folder_id: int = None, company_id: int = None):
        data = {
            'article': {}
        }

        data['article']['name'] = name
        data['article']['content'] = content
        if enable_sharing is not None: data['article']['enable_sharing'] = enable_sharing
        if folder_id is not None: data['article']['folder_id'] = folder_id
        if company_id is not None: data['article']['company_id'] = company_id
        
        return self.__put(f'{self.base_url}/{Hudu.ENDPOINT_ARTICLES}/{id}', json.dumps(data))

    def remove_article(self, id):
        return self.__delete(f'{self.base_url}/{Hudu.ENDPOINT_ARTICLES}/{id}')
    
    def archive_article(self, id):
        return self.__put(f'{self.base_url}/{Hudu.ENDPOINT_ARTICLES}/{id}/{Hudu.ENDPOINT_ARCHIVE}')

    def unarchive_article(self, id):
        return self.__put(f'{self.base_url}/{Hudu.ENDPOINT_ARTICLES}/{id}/{Hudu.ENDPOINT_UNARCHIVE}')

    ###
    # Asset layouts
    ###

    def get_asset_layouts(self, name: str = None, page: int = None):
        params = {}

        if name is not None: params['name'] = name
        if page is not None: params['page'] = page

        return self.__get(f'{self.base_url}/{Hudu.ENDPOINT_ASSET_LAYOUTS}', json.dumps(params))

    def get_asset_layout(self, id):
        return self.__get(f'{self.base_url}/{Hudu.ENDPOINT_ASSET_LAYOUTS}/{id}')

    ## Fields to be list of dict
    def create_asset_layouts(self, name: str, icon: str, color: str, icon_color: str,  fields: list[dict], include_passwords: bool = None, include_photos: bool = None, include_comments: bool = None, include_files: bool = None, password_types: str = None):
        data = {
            'asset_layout': {}
        }

        data['asset_layout']['name'] = name
        data['asset_layout']['icon'] = icon
        data['asset_layout']['color'] = color
        data['asset_layout']['icon_color'] = icon_color
        if include_passwords is not None: data['asset_layout']['include_passwords'] = include_passwords
        if include_photos is not None: data['asset_layout']['include_photos'] = include_photos
        if include_comments is not None: data['asset_layout']['include_comments'] = include_comments
        if include_files is not None: data['asset_layout']['include_files'] = include_files
        if password_types is not None: data['asset_layout']['password_types'] = password_types

        data['asset_layout']['fields'] = []
        for field in fields:
            data['asset_layout']['fields'].append(field.__dict__)
        
        return self.__post(f'{self.base_url}/{Hudu.ENDPOINT_ASSET_LAYOUTS}', json.dumps(data))
            
    def update_asset_layouts(self, id: int, name: str, icon: str, color: str, icon_color: str,  fields: list[dict], include_passwords: bool = None, include_photos: bool = None, include_comments: bool = None, include_files: bool = None, password_types: str = None):
        data = {
            'asset_layout': {}
        }

        data['asset_layout']['name'] = name
        data['asset_layout']['icon'] = icon
        data['asset_layout']['color'] = color
        data['asset_layout']['icon_color'] = icon_color
        if include_passwords is not None: data['asset_layout']['include_passwords'] = include_passwords
        if include_photos is not None: data['asset_layout']['include_photos'] = include_photos
        if include_comments is not None: data['asset_layout']['include_comments'] = include_comments
        if include_files is not None: data['asset_layout']['include_files'] = include_files
        if password_types is not None: data['asset_layout']['password_types'] = password_types

        data['asset_layout']['fields'] = []
        for field in fields:
            data['asset_layout']['fields'].append(field.__dict__)
        
        return self.__put(f'{self.base_url}/{Hudu.ENDPOINT_ASSET_LAYOUTS}/{id}', json.dumps(data))

    ###
    # Asset passwords
    ###

    ###
    # Assets
    ###

    def get_assets(self, company_id: int = None, id: int = None, name: str = None, primary_serial: int = str, asset_layout_id: int = None, page: int = None, archived: bool = False, page_size: int = 25):
        params = {}

        if company_id is not None and id is None and name is None and primary_serial is None and asset_layout_id is None:
            return self.get_company_assets(company_id=company_id, page=page, archived=archived, page_size=page_size)

        if company_id is not None: params['company_id'] = company_id
        if id is not None: params['id'] = id
        if name is not None: params['name'] = name
        if primary_serial is not None: params['primary_serial'] = primary_serial
        if asset_layout_id is not None: params['asset_layout_id'] = asset_layout_id
        if page is not None: params['page'] = page
        if archived is not None: params['archived'] = archived
        if page_size is not None: params['page_size'] = page_size

        return self.__get(f'{self.base_url}/{Hudu.ENDPOINT_ASSETS}', json.dumps(params))

    def get_company_assets(self, company_id: int = None, page: int = None, archived: bool = False, page_size: int = 25):
        params = {}

        if company_id is not None: params['company_id'] = company_id
        if page is not None: params['page'] = page
        if archived is not None: params['archived'] = archived
        if page_size is not None: params['page_size'] = page_size

        return self.__get(f'{self.base_url}/{Hudu.ENDPOINT_COMPANIES}/{company_id}/{Hudu.ENDPOINT_ASSETS}', json.dumps(params))

    def get_company_asset(self, company_id: int, id: int):
        return self.__get(f'{self.base_url}/{Hudu.ENDPOINT_COMPANIES}/{company_id}/{Hudu.ENDPOINT_ASSETS}/{id}')

    def create_asset(self, company_id: int, asset_layout_id: int,  name: str, primary_serial:str = None, primary_mail: str = None, primary_model: str = None, primary_manufacturer: str = None, custom_fields: dict = None):
        data = {
            'asset': {}
        }
        
        data['asset']['asset_layout_id'] = asset_layout_id
        data['asset']['name'] = name        
        if primary_serial is not None: data['asset']['primary_serial'] = primary_serial
        if primary_mail is not None: data['asset']['primary_mail'] = primary_mail
        if primary_model is not None: data['asset']['primary_model'] = primary_model
        if primary_manufacturer is not None: data['asset']['primary_manufacturer'] = primary_manufacturer
        if custom_fields is not None: data['asset']['custom_fields'] = custom_fields
        
        return self.__post(f'{self.base_url}/{Hudu.ENDPOINT_COMPANIES}/{company_id}/{Hudu.ENDPOINT_ASSETS}', json.dumps(data))
            
    def update_asset(self, id: int, company_id: int, asset_layout_id: int,  name: str, primary_serial:str = None, primary_mail: str = None, primary_model: str = None, primary_manufacturer: str = None, custom_fields: dict = None):
        data = {
            'asset': {}
        }

        data['asset']['asset_layout_id'] = asset_layout_id
        data['asset']['name'] = name        
        if primary_serial is not None: data['asset']['primary_serial'] = primary_serial
        if primary_mail is not None: data['asset']['primary_mail'] = primary_mail
        if primary_model is not None: data['asset']['primary_model'] = primary_model
        if primary_manufacturer is not None: data['asset']['primary_manufacturer'] = primary_manufacturer
        if custom_fields is not None: data['asset']['custom_fields'] = custom_fields
        
        return self.__put(f'{self.base_url}/{Hudu.ENDPOINT_COMPANIES}/{company_id}/{Hudu.ENDPOINT_ASSETS}{id}', json.dumps(data))

    def remove_asset(self, id: int, company_id: int):
        return self.__delete(f'{self.base_url}{Hudu.ENDPOINT_COMPANIES}/{company_id}/{Hudu.ENDPOINT_ASSETS}/{id}')
    
    def archive_asset(self, id: int, company_id: int):
        return self.__put(f'{self.base_url}/{Hudu.ENDPOINT_COMPANIES}/{company_id}/{Hudu.ENDPOINT_ASSETS}/{id}/{Hudu.ENDPOINT_ARCHIVE}')

    def unarchive_assets(self, id: int, company_id: int):
        return self.__put(f'{self.base_url}/{Hudu.ENDPOINT_COMPANIES}/{company_id}/{Hudu.ENDPOINT_ASSETS}/{id}/{Hudu.ENDPOINT_UNARCHIVE}')

    ###
    # Cards
    ###

    ###
    # Companies
    ###

    ###
    # Expirations
    ###

    ###
    # Folders
    ###

    ###
    # Magic dash
    ###

    ###
    # Procedures
    ###

    ###
    # Relations
    ###

    ###
    # Websites
    ###

