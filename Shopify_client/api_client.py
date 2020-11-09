import json
import os
import re
from datetime import date

import requests
import yaml


class ShopifyApiClient:
    _AVAILABLE_EXTENSIONS = ('json', 'yaml',)
    """
    Class responsible for handling Shopify api
    :param __AVAILABLE_EXTENSIONS: File formats which class can support 
    """

    def __init__(self,
                 host_shop: str,
                 access_token: str,
                 api_version: str):
        """
        :param host_shop: Domain for shop
        :param access_token: Authenticate token
        :param api_version: Version of api
        """
        if any(
                not isinstance(x, str)
                for x in [host_shop, access_token, api_version]
        ):
            raise ValueError("All arguments must be strings")

        self._host_shop = host_shop
        self._access_token = access_token
        self._api_version = api_version

    @property
    def available_extensions(self):
        return self._AVAILABLE_EXTENSIONS

    def _full_url_path(self, endpoint: str) -> str:
        """
        Returns: full url path with host_shop api version and specific endpoint
        :param endpoint: Rest of the url after api version
            EXAMPLE: /admin/api/2020-07/products.json
                endpoint = products.json
        """
        if not isinstance(endpoint, str):
            raise ValueError("endpoint must be string")

        return 'https://' + self._host_shop + "/admin/api/" + self._api_version + endpoint

    def _headers(self, custom_headers: dict = {}) -> dict:
        """
        Returns: headers for request THIS METHOD WILL ALWAYS ADD Access-Token to HEADERS
        :param custom_headers: Custom headers to send in request
        """
        if not isinstance(custom_headers, dict):
            raise ValueError("custom_headers must be dictionary")
        if any(not isinstance(key, str) and not isinstance(value, str) for key, value in custom_headers.items()):
            raise ValueError("Key and value in dictionary must be strings")

        return {**{'X-Shopify-Access-Token': self._access_token}, **custom_headers}

    def _get_url_from_header(self, header) -> str:
        """
        Returns: Link from header
        """
        if header:
            url = re.findall('<(.*?)>; rel="next"', header)
            return url[0] if url else False
        return False

    def _filter_data_from_nested_fields_for_products(self, data: dict, nested_fields: dict) -> dict:
        """
        Returns: Filtered data
        :param data: Data to filter
        :param nested_fields: Fields to return
        """
        if not data.get('products'):
            raise Exception(f"There was a problem with request: {data}")

        for product_index in range(len(data["products"])):
            for key, value in nested_fields.items():
                data["products"][product_index][key] = [
                    {key: value_test
                     for key, value_test in data["products"][0][key][0].items() if
                     key in value}]
        return data

    def get_all_products(self, limit_result: int = 250) -> dict:
        """
        Returns: All products in JSON format
        :param limit_result: The maximum number of results per request
        """
        if not isinstance(limit_result, int):
            raise ValueError("filters must be list")

        endpoint = f"/products.json?limit={limit_result}"
        url = self._full_url_path(endpoint)
        headers = self._headers()

        data_to_return_in_json = {'products': []}
        while url:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data_to_return_in_json['products'] += response.json()['products']
                url = self._get_url_from_header(response.headers.get('link'))
            else:
                data_to_return_in_json = response.json()
                break

        return data_to_return_in_json

    def get_all_products_select_fields(self, fields: list = []) -> dict:
        """
        Returns: All products filtered by fields
        :param fields: Fields to return from products
        """
        if not isinstance(fields, list):
            raise ValueError("filters must be list")
        if any(not isinstance(field, str) for field in fields):
            raise ValueError("fields in filters must be strings")

        endpoint = "/products.json?fields=" + ','.join(fields)
        url = self._full_url_path(endpoint)
        headers = self._headers()

        data_to_return_in_json = {'products': []}
        while url:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data_to_return_in_json['products'] += response.json().get('products')
                url = self._get_url_from_header(response.headers.get('link'))
            else:
                data_to_return_in_json = response.json()
                break

        return data_to_return_in_json

    def update_product(self, product_id: int, data_to_update: dict, return_updated_product: bool = True):
        """
        Updates product by given data
        :param product_id: Product ID for update
        :param data_to_update: Data to update
        :param return_updated_product: if True function will return updated product as dictionary
        """
        if not isinstance(product_id, int):
            raise ValueError("product_id must be integer")
        if not isinstance(data_to_update, dict):
            raise ValueError("data_to_update must be dict")
        if not isinstance(return_updated_product, bool):
            raise ValueError("return_updated_product must be bool")

        url = self._full_url_path(f"/products/{product_id}.json")
        headers = self._headers({"Content-Type": "application/json"})
        data = json.dumps(data_to_update)

        response = requests.put(url, headers=headers, data=data)

        if return_updated_product:
            return response.json()

    def saves_all_products_by_fields(self,
                                     extension: str,
                                     fields: list = [],
                                     nested_fields_to_return: dict = {},
                                     path: str = os.path.abspath(os.getcwd())) -> str:
        """
        Saves all products in file
        Returns: Path to file
        :param extension: Type of format file
        :param fields: Fields to return from products
        :param nested_fields_to_return: Nested fields to return from file
        :param path: Path where result will be saved DEFAULT = path to script
        """
        if extension not in self._AVAILABLE_EXTENSIONS:
            raise AttributeError(f"extension not supported, AVAILABLE EXTENSIONS = {self._AVAILABLE_EXTENSIONS}")
        if not isinstance(path, str):
            raise ValueError("path must be string")
        if not os.path.isdir(path):
            raise OSError(f"There is no directory: {path}")
        if not isinstance(nested_fields_to_return, dict):
            raise ValueError("nested_fields_to_return must be dict")
        if any(key not in fields for key in nested_fields_to_return.keys()):
            raise ValueError("Nested field must be in fields")
        if any(not isinstance(item, list) for item in nested_fields_to_return.values()):
            raise ValueError("Value in nested_fields_to_return must be list")

        data_of_all_products = self.get_all_products_select_fields(fields)
        filtered_data = self._filter_data_from_nested_fields_for_products(data_of_all_products, nested_fields_to_return)
        path_to_file = os.path.join(path, f'All_products_{date.today().strftime("%d_%m_%Y")}' + "." + extension)
        with open(path_to_file, 'w') as f:
            if extension == "json":
                json.dump(filtered_data, f)
            elif extension == "yaml":
                yaml.dump(filtered_data, f)

        return path_to_file

    def update_products_from_file(self, path_to_file):
        """
        Updates products by given file
        :param path_to_file: Path to file with data
        """
        if not isinstance(path_to_file, str):
            raise ValueError("path_to_file must be string")
        if not os.path.isfile(path_to_file):
            raise OSError(f"There is no file: {path_to_file}")

        extension = os.path.splitext(path_to_file)[1][1:]
        if extension not in self._AVAILABLE_EXTENSIONS:
            raise AttributeError(f"Wrong file format, AVAILABLE EXTENSIONS = {self._AVAILABLE_EXTENSIONS}")

        with open(path_to_file, 'r') as f:
            if extension == "yaml":
                data_all_products_json = yaml.safe_load(f)
            elif extension == "json":
                data_all_products_json = json.load(f)

            if any(product.get('id') is None for product in data_all_products_json['products']):
                raise ValueError("There is missing id for product in the file")

            for product in data_all_products_json['products']:
                self.update_product(product["id"], {"product": product}, return_updated_product=False)

# ASYNC VERSION
# def update_products_from_file(self, path_to_file):
#     """
#     Updates products by given file
#     :param path_to_file: Path to file with data
#     """
#     if not isinstance(path_to_file, str):
#         raise ValueError("path_to_file must be string")
#     if not os.path.isfile(path_to_file):
#         raise OSError(f"There is no file: {path_to_file}")
#
#     async def update_single_product(url, headers, data):
#         async with aiohttp.ClientSession(headers=headers) as session:
#             async with session.put(url, data=data) as response:
#                 time.sleep(1)
#                 return response
#
#     loop = asyncio.get_event_loop()
#     coroutines = [update_single_product(
#         url=self._full_url_path(f"/products/{product['id']}.json"),
#         headers=self._headers(
#             {"Content-Type": "application/json"}),
#         data=json.dumps({"product": product})
#     ) for product in data_all_products_json['products']]
#
#     results = loop.run_until_complete(asyncio.gather(*coroutines))
