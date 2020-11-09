import os
import unittest
from unittest.mock import patch

import responses
from parameterized import parameterized

import api_client


class TestShopifyApiClient(unittest.TestCase):

    def setUp(self):
        self.client = api_client.ShopifyApiClient('test_host_shop', 'test_access_token', 'test_api_version')

    def test_api_client_creation_correct(self):
        self.assertEqual(self.client._host_shop, 'test_host_shop')
        self.assertEqual(self.client._access_token, 'test_access_token')
        self.assertEqual(self.client._api_version, 'test_api_version')
        self.assertEqual(type(self.client.available_extensions), tuple)

    def test_api_client_creation_wrong_data_type(self):
        with self.assertRaises(ValueError):
            api_client.ShopifyApiClient('test_host_shop', 'test_access_token', ['test'])

    def test__full_url_path(self):
        self.assertEqual(self.client._full_url_path('test_endpoint'),
                         'https://test_host_shop/admin/api/test_api_versiontest_endpoint')

    def test__full_url_path_wrong_data_type(self):
        with self.assertRaises(ValueError):
            self.client._full_url_path(1337)

    def test__headers_without_passing_dict(self):
        self.assertEqual(self.client._headers(), {'X-Shopify-Access-Token': 'test_access_token'})

    def test__headers_with_passing_dict(self):
        self.assertEqual(self.client._headers({'test_key': 'test_value'}),
                         {'X-Shopify-Access-Token': 'test_access_token', 'test_key': 'test_value'})

    def test__headers_wrong_data_type(self):
        with self.assertRaises(ValueError):
            self.client._full_url_path(['test_key', 'test_value'])

    @parameterized.expand([['test_key', 1337], [13.37, 'test_value']])
    def test__headers_wrong_data_type_in_dict(self, test_key, test_value):
        with self.assertRaises(ValueError):
            self.client._full_url_path({test_key: test_value})

    @parameterized.expand([['there is no link here', False],
                           ['<https://test_host_shop/admin/api/test_api_version/products.json?next_page>; rel="next"',
                            'https://test_host_shop/admin/api/test_api_version/products.json?next_page']
                           ])
    def test__get_url_from_header(self, test_header, expected):
        self.assertEqual(self.client._get_url_from_header(test_header), expected)

    def test__filter_data_from_nested_fields_for_products(self):
        json_data = {"products": [{"test_main_field_1": 1, "test_main_field_2": 2, "nested_test_1": [
            {"nested_test_1_field_1": 11, "nested_test_1_field_2": 12, "nested_test_1_field_3": 13}],
                                   "nested_test_2": [{"nested_test_2_field_1": 21}, {"nested_test_2_field_2": 22}]}]}
        self.assertEqual(self.client._filter_data_from_nested_fields_for_products(
            json_data, {"nested_test_1": ["nested_test_1_field_1", "nested_test_1_field_2"]}),
            {'products': [{'test_main_field_1': 1, 'test_main_field_2': 2,
                           'nested_test_1': [{'nested_test_1_field_1': 11, 'nested_test_1_field_2': 12}],
                           'nested_test_2': [{'nested_test_2_field_1': 21}, {'nested_test_2_field_2': 22}]}]})

    def test__filter_data_from_nested_fields_for_products_multiple_keys(self):
        json_data = {"products": [{"test_main_field_1": 1, "test_main_field_2": 2, "nested_test_1": [
            {"nested_test_1_field_1": 11, "nested_test_1_field_2": 12, "nested_test_1_field_3": 13}],
                                   "nested_test_2": [{"nested_test_2_field_1": 21}, {"nested_test_2_field_2": 22}]}]}

        self.assertEqual(self.client._filter_data_from_nested_fields_for_products(
            json_data, {"nested_test_1": ["nested_test_1_field_2"], "nested_test_2": ["nested_test_2_field_1"]}),
            {'products': [{'test_main_field_1': 1, 'test_main_field_2': 2,
                           'nested_test_1': [{'nested_test_1_field_2': 12}],
                           'nested_test_2': [{'nested_test_2_field_1': 21}]}]})

    def test__filter_data_from_nested_fields_for_products_without_products(self):
        json_data = {'not_link': 'no products'}
        with self.assertRaises(Exception):
            self.client._filter_data_from_nested_fields_for_products(json_data)

    @responses.activate
    def test_get_all_products_correct(self):
        responses.add(
            responses.GET,
            'https://test_host_shop/admin/api/test_api_version/products.json',
            json={"products": [{'test_product_1_key_1': 'test_product_1_value_1'}]},
            headers={'not_link': 'not_link'},
            status=200
        )
        self.assertEqual(self.client.get_all_products(),
                         {'products': [{'test_product_1_key_1': 'test_product_1_value_1'}]})

    @responses.activate
    def test_get_all_products_correct_after_limit(self):
        responses.add(
            responses.GET,
            'https://test_host_shop/admin/api/test_api_version/products.json?limit=250',
            json={"products": [{'test_product_1_key_1': 'test_product_1_value_1'}]},
            headers={'link': '<https://test_host_shop/admin/api/test_api_version/products.json?next_page>; rel="next"'},
            status=200
        )
        responses.add(
            responses.GET,
            'https://test_host_shop/admin/api/test_api_version/products.json?next_page',
            json={"products": [{'test_product_2_key_2': 'test_product_2_value_2'}]},
            headers={'not_link': 'not_link'},
            status=200
        )
        self.assertEqual(self.client.get_all_products(limit_result=250),
                         {'products': [{'test_product_1_key_1': 'test_product_1_value_1'},
                                       {'test_product_2_key_2': 'test_product_2_value_2'}]})

    @responses.activate
    def test_get_all_products_bad_request(self):
        responses.add(
            responses.GET,
            'https://test_host_shop/admin/api/test_api_version/products.json',
            json={'errors': 'Not Found'},
            headers={'not_link': 'not_link'},
            status=404
        )
        self.assertEqual(self.client.get_all_products(), {'errors': 'Not Found'})

    @parameterized.expand([[1.1], ['test'], [{}]])
    def test_get_all_products_wrong_data_type(self, test_limit):
        with self.assertRaises(ValueError):
            self.client.get_all_products(limit_result=test_limit)

    @responses.activate
    def test_get_all_products_select_fields_correct(self):
        responses.add(
            responses.GET,
            'https://test_host_shop/admin/api/test_api_version/products.json',
            json={"products": [{'test_product_1_key_1': 'test_product_1_value_1'}]},
            headers={'not_link': 'not_link'},
            status=200
        )
        self.assertEqual(self.client.get_all_products_select_fields(),
                         {'products': [{'test_product_1_key_1': 'test_product_1_value_1'}]})

    @responses.activate
    def test_get_all_products_select_fields_correct_after_limit(self):
        responses.add(
            responses.GET,
            'https://test_host_shop/admin/api/test_api_version/products.json?fields=',
            json={"products": [{'test_product_1_key_1': 'test_product_1_value_1'}]},
            headers={'link': '<https://test_host_shop/admin/api/test_api_version/products.json?next_page>; rel="next"'},
            status=200
        )
        responses.add(
            responses.GET,
            'https://test_host_shop/admin/api/test_api_version/products.json?next_page',
            json={"products": [{'test_product_2_key_2': 'test_product_2_value_2'}]},
            headers={'not_link': 'not_link'},
            status=200
        )
        self.assertEqual(self.client.get_all_products_select_fields(),
                         {'products': [{'test_product_1_key_1': 'test_product_1_value_1'},
                                       {'test_product_2_key_2': 'test_product_2_value_2'}]})

    @responses.activate
    def test_get_all_products_bad_request(self):
        responses.add(
            responses.GET,
            'https://test_host_shop/admin/api/test_api_version/products.json',
            json={'errors': 'Not Found'},
            headers={'not_link': 'not_link'},
            status=404
        )
        self.assertEqual(self.client.get_all_products_select_fields(), {'errors': 'Not Found'})

    @parameterized.expand([[123], [['test_1', []]]])
    def test_get_all_products_wrong_data_type(self, test_filters):
        with self.assertRaises(ValueError):
            self.client.get_all_products_select_fields(fields=test_filters)

    @responses.activate
    def test_update_product_correct(self):
        responses.add(
            responses.PUT,
            'https://test_host_shop/admin/api/test_api_version/products/123.json',
            json={"products": [{'test_product_1_key_1': 'test_product_1_value_1'}]},
            status=200
        )
        test_data_update = {"product": {"title": "test_title_update", "vendor": "test_vendor_update"}}
        self.assertEqual(self.client.update_product(123, test_data_update),
                         {'products': [{'test_product_1_key_1': 'test_product_1_value_1'}]})

    @responses.activate
    def test_update_product_correct_without_returned_object(self):
        responses.add(
            responses.PUT,
            'https://test_host_shop/admin/api/test_api_version/products/123.json',
            json={"products": [{'test_product_1_key_1': 'test_product_1_value_1'}]},
            status=200
        )
        test_data_update = {"product": {"title": "test_title_update", "vendor": "test_vendor_update"}}
        self.assertEqual(self.client.update_product(123, test_data_update, return_updated_product=False), None)

    @responses.activate
    def test_update_product_bad_request(self):
        responses.add(
            responses.PUT,
            'https://test_host_shop/admin/api/test_api_version/products/123.json',
            json={'errors': 'Not Found'},
            status=404
        )
        test_data_update = {"product": {"title": "test_title_update", "vendor": "test_vendor_update"}}
        self.assertEqual(self.client.update_product(123, test_data_update),
                         {'errors': 'Not Found'})

    @parameterized.expand(
        [[123.456, {"products": [{'test_product_1_key_1': 'test_product_1_value_1'}]}, True],
         [123, [{"products": [{'test_product_1_key_1': 'test_product_1_value_1'}]}], True],
         [123, {"products": [{'test_product_1_key_1': 'test_product_1_value_1'}]}, 123]])
    def test_update_product_wrong_data_type(self, test_product_id, test_data_to_update, test_return_updated_product):
        with self.assertRaises(ValueError):
            self.client.update_product(test_product_id, data_to_update=test_data_to_update,
                                       return_updated_product=test_return_updated_product)

    @responses.activate
    def test_saves_all_products_by_fields_check_json_format(self):
        responses.add(
            responses.GET,
            'https://test_host_shop/admin/api/test_api_version/products.json'
            '?fields=test_main_field_1,test_main_field_2,nested_test_1,nested_test_2',
            json={"products":
                      [{"test_main_field_1": 1,
                        "test_main_field_2": 2,
                        "nested_test_1": [{"nested_test_1_field_1": 11,
                                           "nested_test_1_field_2": 12,
                                           "nested_test_1_field_3": 13}],
                        "nested_test_2": [{"nested_test_2_field_1": 21},
                                          {"nested_test_2_field_2": 22}]}]},
            status=200
        )

        path_to_test_file = self.client.saves_all_products_by_fields(extension='json',
                                                                     path=os.path.abspath(os.getcwd()) + '/tests',
                                                                     fields=['test_main_field_1', 'test_main_field_2',
                                                                             'nested_test_1', 'nested_test_2'],
                                                                     nested_fields_to_return={
                                                                         "nested_test_2": ["nested_test_2_field_1"]})

        self.assertEqual(os.path.isfile(path_to_test_file), True)
        self.assertEqual(os.path.splitext(path_to_test_file)[1], '.json')
        with open(path_to_test_file, 'r') as f:
            text_test_file = f.read()
            self.assertEqual(text_test_file, '{"products": [{"test_main_field_1": 1, "test_main_field_2": 2, '
                                             '"nested_test_1": [{"nested_test_1_field_1": 11, '
                                             '"nested_test_1_field_2": 12, "nested_test_1_field_3": 13}], '
                                             '"nested_test_2": [{"nested_test_2_field_1": 21}]}]}')
        os.remove(path_to_test_file)

    @responses.activate
    def test_saves_all_products_by_fields_check_yaml_format(self):
        responses.add(
            responses.GET,
            'https://test_host_shop/admin/api/test_api_version/products.json'
            '?fields=test_main_field_1,test_main_field_2,nested_test_1,nested_test_2',
            json={"products":
                      [{"test_main_field_1": 1,
                        "test_main_field_2": 2,
                        "nested_test_1": [{"nested_test_1_field_1": 11,
                                           "nested_test_1_field_2": 12,
                                           "nested_test_1_field_3": 13}],
                        "nested_test_2": [{"nested_test_2_field_1": 21},
                                          {"nested_test_2_field_2": 22}]}]},
            status=200
        )

        path_to_test_file = self.client.saves_all_products_by_fields(extension='yaml',
                                                                     path=os.path.abspath(os.getcwd()) + '/tests',
                                                                     fields=['test_main_field_1', 'test_main_field_2',
                                                                             'nested_test_1', 'nested_test_2'],
                                                                     nested_fields_to_return={
                                                                         "nested_test_2": ["nested_test_2_field_1"]})

        self.assertEqual(os.path.isfile(path_to_test_file), True)
        self.assertEqual(os.path.splitext(path_to_test_file)[1], '.yaml')
        with open(path_to_test_file, 'r') as f:
            text_test_file = f.read()
            self.assertEqual(text_test_file, 'products:\n- nested_test_1:\n  - nested_test_1_field_1: 11\n    '
                                             'nested_test_1_field_2: 12\n    nested_test_1_field_3: 13\n  '
                                             'nested_test_2:\n  - nested_test_2_field_1: 21\n  test_main_field_1: 1\n  '
                                             'test_main_field_2: 2\n')
        os.remove(path_to_test_file)

    @parameterized.expand(
        [['this will newer be a extension', 'test_path', [], {}, AttributeError],
         ['json', 1.23, [], {}, ValueError],
         ['json', '/wrong directory', [], {}, OSError],
         ['json', os.path.abspath(os.getcwd()), 'list', {}, ValueError],
         ['json', os.path.abspath(os.getcwd()), [], 'dict', ValueError],
         ['json', os.path.abspath(os.getcwd()), ['test_1', True], {}, ValueError],
         ['json', os.path.abspath(os.getcwd()), ['test_1', 'test_2'], {'test_3': 'test_value'}, ValueError]
         ])
    def test_saves_all_products_by_fields_wrong_data_type(self, test_extension, test_path,
                                                          test_fields, test_nested_fields_to_return, error):
        with self.assertRaises(error):
            self.client.saves_all_products_by_fields(extension=test_extension, path=test_path,
                                                     fields=test_fields,
                                                     nested_fields_to_return=test_nested_fields_to_return)

    @responses.activate
    def test_update_products_from_file_json_format(self):
        responses.add(
            responses.PUT,
            url='https://test_host_shop/admin/api/test_api_version/products/1.json',
            status=200
        )
        responses.add(
            responses.PUT,
            url='https://test_host_shop/admin/api/test_api_version/products/2.json',
            status=200
        )
        self.client.update_products_from_file(
            path_to_file=os.path.join(os.getcwd() + '/tests/test_files/', 'test_json.json'))

    @patch('api_client.ShopifyApiClient.update_product')
    def test_update_products_from_file_json_format_values_to_update_per_product(self, mock_update_product):
        self.client.update_products_from_file(
            path_to_file=os.path.join(os.getcwd() + '/tests/test_files/', 'test_json.json'))
        self.assertEqual(mock_update_product.call_count, 2)
        mock_update_product.assert_called_with(2, {'product': {'id': 2, '2test_main_field_1': 1,
                                                               '2test_main_field_2': 2,
                                                               '2nested_test_1': [
                                                                   {'2nested_test_1_field_1': 11,
                                                                    '2nested_test_1_field_2': 12,
                                                                    '2nested_test_1_field_3': 13}],
                                                               '2nested_test_2': [
                                                                   {'2nested_test_2_field_1': 21}]}},
                                               return_updated_product=False)

    def test_update_products_from_file_json_format_no_id(self):
        with self.assertRaises(ValueError):
            self.client.update_products_from_file(
                path_to_file=os.path.join(os.getcwd() + '/tests/test_files/', 'test_json_no_id.json'))

    @responses.activate
    def test_update_products_from_yaml_json_format(self):
        responses.add(
            responses.PUT,
            url='https://test_host_shop/admin/api/test_api_version/products/1.json',
            status=200
        )
        responses.add(
            responses.PUT,
            url='https://test_host_shop/admin/api/test_api_version/products/2.json',
            status=200
        )
        self.client.update_products_from_file(
            path_to_file=os.path.join(os.getcwd() + '/tests/test_files/', 'test_yaml.yaml'))

    @patch('api_client.ShopifyApiClient.update_product')
    def test_update_products_from_file_yaml_format_values_to_update_per_product(self, mock_update_product):
        self.client.update_products_from_file(
            path_to_file=os.path.join(os.getcwd() + '/tests/test_files/', 'test_yaml.yaml'))
        self.assertEqual(mock_update_product.call_count, 2)
        mock_update_product.assert_called_with(2, {'product': {'id': 2, '2test_main_field_1': 1,
                                                               '2test_main_field_2': 2,
                                                               '2nested_test_1': [
                                                                   {'2nested_test_1_field_1': 11,
                                                                    '2nested_test_1_field_2': 12,
                                                                    '2nested_test_1_field_3': 13}],
                                                               '2nested_test_2': [
                                                                   {'2nested_test_2_field_1': 21}]}},
                                               return_updated_product=False)

    def test_update_products_from_yaml_json_format_no_id(self):
        with self.assertRaises(ValueError):
            self.client.update_products_from_file(
                path_to_file=os.path.join(os.getcwd() + '/tests/test_files/', 'test_yaml_no_id.yaml'))

    @parameterized.expand([[123, ValueError],
                           [os.path.join(os.getcwd(), 'there_is_no_file.json'), OSError],
                           [os.path.join(os.getcwd() + '/tests/test_files/', 'wrong_extension.js'), AttributeError]])
    def test_update_products_from_file_wrong_data_type(self, test_path_to_file, error):
        with self.assertRaises(error):
            self.client.update_products_from_file(test_path_to_file)
