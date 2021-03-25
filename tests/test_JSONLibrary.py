# -*- coding: utf-8 -*-

__author__ = 'Traitanit Huangsri'
__email__ = 'traitanit.hua@ascendcorp.com'

from JSONLibrary import JSONLibrary
import unittest
import os


class JSONLibraryTest(unittest.TestCase):
    test = JSONLibrary()
    json = None

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.json = self.test.load_json_from_file(os.path.join(dir_path, 'json', 'example.json'))

    def test_add_object_to_json(self):
        json_path = '$..address'
        data_to_add = {'latitude': '13.1234', 'longitude': '130.1234'}
        json_object = self.test.add_object_to_json(self.json, json_path, data_to_add)
        self.assertDictContainsSubset(data_to_add, json_object['address'])

    def test_add_new_object_to_root(self):
        json_path = '$'
        data_to_add = {'country': 'Thailand'}
        json_object = self.test.add_object_to_json(self.json, json_path, data_to_add)
        self.assertEqual(json_object['country'], 'Thailand')

    def test_add_new_list_to_json(self):
        json_path = '$..favoriteColor'
        data_to_add = 'green'
        json_object = self.test.add_object_to_json(self.json, json_path, data_to_add)
        self.assertIn(data_to_add, json_object['favoriteColor'])

    def test_get_value_from_json_path(self):
        json_path = '$..number'
        values = self.test.get_value_from_json(self.json, json_path)
        expected_result = ['0123-4567-8888', '0123-4567-8910']
        self.assertListEqual(values, expected_result)

    def test_get_value_from_json_path_not_found(self):
        json_path = '$..notfound'
        values = self.test.get_value_from_json(self.json, json_path)
        expected_result = []
        self.assertListEqual(values, expected_result)

    def test_update_value_to_json(self):
        json_path = '$..address.streetAddress'
        value_to_update = 'Ratchadapisek Road'
        json_object = self.test.update_value_to_json(self.json, json_path, value_to_update)
        self.assertEqual(value_to_update, json_object['address']['streetAddress'])

    def test_update_value_to_json_as_index(self):
        json_path = '$..phoneNumbers[0].type'
        value_to_update = 'mobile'
        json_object = self.test.update_value_to_json(self.json, json_path, value_to_update)
        self.assertEqual(value_to_update, json_object['phoneNumbers'][0]['type'])

    def test_delete_object_from_json(self):
        json_path = '$..isMarried'
        json_object = self.test.delete_object_from_json(self.json, json_path)
        self.assertFalse('isMarried' in json_object)

    def test_convert_json_to_string(self):
        json_str = self.test.convert_json_to_string(self.json)
        self.assertTrue(isinstance(json_str, str))

    def test_convert_string_to_json(self):
        json_obj = self.test.convert_string_to_json('{"firstName": "John"}')
        self.assertTrue("firstName" in json_obj)
        
    def test_dump_json_to_file(self):
        if os.name == 'nt':
            tmp_path = os.getenv('TMP', 'c:\\Temp\\')
        else:
            tmp_path = os.getenv('TMP', '/tmp/')
        file_path = '%ssample.json' % (tmp_path)
        json_file = self.test.dump_json_to_file(file_path, self.json)
        self.assertTrue(os.path.exists(json_file))
        

    def tearDown(self):
        pass
