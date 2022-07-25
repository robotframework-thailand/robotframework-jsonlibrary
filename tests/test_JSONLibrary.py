# -*- coding: utf-8 -*-

__author__ = "Traitanit Huangsri"
__email__ = "traitanit.hua@ascendcorp.com"

import os
import tempfile
import pytest
from copy import deepcopy
from JSONLibrary import JSONLibrary


class TestJSONLibrary:
    test = JSONLibrary()

    @pytest.fixture(autouse=True)
    def json(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return self.test.load_json_from_file(
            os.path.join(dir_path, "json", "example.json")
        )

    def test_add_dict_element_to_json(self, json):
        json_path = "$..address"
        data_to_add = {"latitude": "13.1234", "longitude": "130.1234"}
        json_cpy = deepcopy(json)
        json_object = self.test.add_object_to_json(json_cpy, json_path, data_to_add)
        assert json_object["address"] == {**json_object["address"], **data_to_add}
        assert json_cpy == json

    def test_add_new_object_to_root(self, json):
        json_path = "$.country"
        data_to_add = "Thailand"
        json_cpy = deepcopy(json)
        json_object = self.test.add_object_to_json(json_cpy, json_path, data_to_add)
        assert json_object["country"] == "Thailand"
        assert json_cpy == json

    def test_add_list_element_to_json(self, json):
        json_path = "$..favoriteColor"
        data_to_add = "green"
        json_cpy = deepcopy(json)
        json_object = self.test.add_object_to_json(json_cpy, json_path, data_to_add)
        assert data_to_add in json_object["favoriteColor"]
        assert json_cpy, json

    def test_get_value_from_json_path(self, json):
        json_path = "$..number"
        values = self.test.get_value_from_json(json, json_path)
        expected_result = ["0123-4567-8888", "0123-4567-8910", "0123-4567-8999"]
        assert values == expected_result

    def test_get_none_from_json_path(self, json):
        json_path = "$..occupation"
        values = self.test.get_value_from_json(json, json_path)
        assert len(values) > 0
        for v in values:
            assert v is None

    def test_get_empty_list_from_json_path(self, json):
        json_path = "$..siblings"
        values = self.test.get_value_from_json(json, json_path)
        expected_result = []
        assert values, expected_result

    def test_get_value_from_json_path_not_found(self, json):
        json_path = "$..notfound"
        with pytest.raises(AssertionError):
            self.test.get_value_from_json(json, json_path, fail_on_empty=True)

        # backward-compatibility, fail_on_empty is False by default
        values = self.test.get_value_from_json(json, json_path)
        expected_result = []
        assert values == expected_result

    def test_has_value_from_json_path_passed(self, json):
        json_path = "$..isMarried"
        self.test.should_have_value_in_json(json, json_path)

    def test_has_value_from_json_path_failed(self, json):
        json_path = "$..hasSiblings"
        with pytest.raises(AssertionError):
            self.test.should_have_value_in_json(json, json_path)

    def test_has_no_value_from_json_path_passed(self, json):
        json_path = "$..hasSiblings"
        self.test.should_not_have_value_in_json(json, json_path)

    def test_has_no_value_from_json_path_failed(self, json):
        json_path = "$..isMarried"
        with pytest.raises(AssertionError):
            self.test.should_not_have_value_in_json(json, json_path)

    def test_update_value_to_json(self, json):
        json_path = "$..address.streetAddress"
        value_to_update = "Ratchadapisek Road"
        json_cpy = deepcopy(json)
        json_object = self.test.update_value_to_json(
            json_cpy, json_path, value_to_update
        )
        assert json_cpy == json
        assert value_to_update == json_object["address"]["streetAddress"]

    def test_update_value_to_json_as_index(self, json):
        json_path = "$..phoneNumbers[0].type"
        value_to_update = "mobile"
        json_cpy = deepcopy(json)
        json_object = self.test.update_value_to_json(
            json_cpy, json_path, value_to_update
        )
        assert json_cpy == json
        assert value_to_update == json_object["phoneNumbers"][0]["type"]

    def test_delete_object_from_json(self, json):
        json_path = "$..isMarried"
        json_cpy = deepcopy(json)
        json_object = self.test.delete_object_from_json(json_cpy, json_path)
        assert "isMarried" not in json_object
        assert json_cpy == json

    def test_delete_array_elements_from_json(self, json):
        json_path = "$..phoneNumbers[0]"
        json_cpy = deepcopy(json)
        json_object = self.test.delete_object_from_json(json_cpy, json_path)
        assert not any(pn["type"] == "iPhone" for pn in json_object["phoneNumbers"])
        assert json_cpy == json

    def test_delete_all_array_elements_from_json(self, json):
        json_path = "$..phoneNumbers[*]"
        json_cpy = deepcopy(json)
        json_object = self.test.delete_object_from_json(json_cpy, json_path)
        expected_result = []
        assert expected_result == json_object["phoneNumbers"]
        assert json_cpy, json

    def test_invalid_syntax_doesnt_crash(self, json):
        json_path = "$.bankAccounts[?(@.amount>=100)].bank"
        values = self.test.get_value_from_json(json, json_path)
        expected_result = ["WesternUnion", "HSBC"]
        assert values == expected_result

        json_path = "$.bankAccounts[?(@.amount=>100)].bank"
        with pytest.raises(AssertionError):
            self.test.get_value_from_json(json, json_path)

    def test_convert_json_to_string(self, json):
        json_str = self.test.convert_json_to_string(json)
        assert isinstance(json_str, str)

    def test_convert_string_to_json(self, json):
        json_obj = self.test.convert_string_to_json('{"firstName": "John"}')
        assert "firstName" in json_obj

    def test_dump_json_to_file(self, json):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = "%ssample.json" % temp_dir
            json_file = self.test.dump_json_to_file(file_path, json)
            assert os.path.exists(json_file)
