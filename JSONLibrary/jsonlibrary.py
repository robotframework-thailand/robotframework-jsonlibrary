# -*- coding: utf-8 -*-
import io
import json
import os.path
import jsonschema
from copy import deepcopy
from robot.api import logger
from robot.utils.asserts import fail
from jsonpath_ng import Index, Fields
from jsonpath_ng.ext import parse as parse_ng
from jsonpath_ng.exceptions import JsonPathParserError

__author__ = "Traitanit Huangsri"
__email__ = "traitanit.hua@gmail.com"


class JSONLibrary:
    """JSONLibrary is a robotframework testlibrary for manipulating JSON object (dictionary)

    You can get, add, update and delete your json object using JSONPath.

    == JSONPath Syntax ==
    | JSONPath | Description |
    | $        | the root object/element |
    | @        | the current object/element |
    | . or []  | child operator |
    | ..       | recursive descent. JSONPath borrows this syntax from E4X |
    | *        | wildcard. All objects/element regardless their names. |
    | []       | subscript operator. XPath uses it to iterate over element collections and for predicates.
                 In Javascript and JSON it is the native array operator. |
    | [,]      | Union operator in XPath results in a combination of node sets. JSONPath allows alternate
                 names or array indices as a set. |
    | [start:end:step] | array slice operator borrowed from ES4 |
    | ?()      | applies a filter (script) expression. |
    | ()       | script expression, using the underlying script engine. |

    == *** Known issue *** ==
    If there is a space in JSONPath expression, the module used by this library will throw an exception.
    Therefore, please avoid the space in JSONPath expression if possible.

    *Example:*
    | JSONPath | Exception? |
    | $.[?(@.id == 1)] | Y |
    | $.[?(@.id==1)] | N |
    | $.[?(@.name=='test 123')] | N |

    == Example Test Cases ==
    | *** Settings ***     |
    | Library              | JSONLibrary |
    |                      |
    | *** Test Cases ***   |
    | TestManipulatingJSON |
    | ${json_object}=      |  Load JSON From File  |  example.json  |
    | ${object_to_add}=    |  Create Dictionary    |  country=Thailand |
    | ${json_object}=      |  Add Object To Json   |  ${json_object}  |  $..address  | ${object_to_add} |
    | ${value}=            |  Get Value From Json  |  ${json_object}  |  $..country  |
    | Should Be Equal As Strings  |  ${value[0]}   | Thailand  |


    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"
    ROBOT_EXIT_ON_FAILURE = True

    @staticmethod
    def _parse(json_path):
        try:
            return parse_ng(json_path)
        except JsonPathParserError as e:
            fail(
                "Parser failed to understand syntax '{}'. error message: "
                "\n{}\n\nYou may raise an issue on https://github.com/h2non/jsonpath-ng".format(
                    json_path, e
                )
            )

    @staticmethod
    def load_json_from_file(file_name, encoding=None):
        """Load JSON from file.

        Return json as a dictionary object.

        Arguments:
            - file_name: absolute json file name
            - encoding: encoding of the file

        Return json object (list or dictionary)

        Examples:
        | ${result}=  |  Load Json From File  | /path/to/file.json |
        """
        logger.debug("Check if file exists")
        if os.path.isfile(file_name) is False:
            logger.error("JSON file: " + file_name + " not found")
            raise IOError
        with io.open(file_name, mode="r", encoding=encoding) as json_file:
            data = json.load(json_file)
        return data

    def add_object_to_json(self, json_object, json_path, object_to_add):
        """Add an dictionary or list object to json object using json_path

        Arguments:
            - json_object: json as a dictionary object.
            - json_path: jsonpath expression
            - object_to_add: dictionary or list object to add to json_object which is matched by json_path

        Return new json object.

        Examples:
        | ${dict}=  | Create Dictionary    | latitude=13.1234 | longitude=130.1234 |
        | ${json}=  |  Add Object To Json  | ${json}          | $..address         |  ${dict} |
        """
        json_path_expr = self._parse(json_path)
        json_object_cpy = deepcopy(json_object)
        object_to_add_cpy = deepcopy(object_to_add)
        rv = json_path_expr.find(json_object_cpy)
        if len(rv):
            for match in rv:
                if type(match.value) is dict:
                    match.value.update(object_to_add_cpy)
                if type(match.value) is list:
                    match.value.append(object_to_add_cpy)
        else:
            parent_json_path = ".".join(json_path.split(".")[:-1])
            child_name = json_path.split(".")[-1]
            json_path_expr = self._parse(parent_json_path)
            rv = json_path_expr.find(json_object_cpy)
            if len(rv):
                for match in rv:
                    match.value.update({child_name: object_to_add_cpy})
            else:
                fail(f"no match found for parent {parent_json_path}")

        return json_object_cpy

    def get_value_from_json(self, json_object, json_path, fail_on_empty=False):
        """Get Value From JSON using JSONPath

        Arguments:
            - json_object: json as a dictionary object.
            - json_path: jsonpath expression
            - fail_on_empty: fail the testcases if nothing is returned

        Return array of values

        Examples:
        | ${values}=  |  Get Value From Json  | ${json} |  $..phone_number |
        | ${values}=  |  Get Value From Json  | ${json} |  $..missing | fail_on_empty=${True} |
        """
        json_path_expr = self._parse(json_path)
        rv = json_path_expr.find(json_object)
        # optional: make the keyword fails if nothing was return
        if fail_on_empty is True and (rv is None or len(rv) == 0):
            fail(f"Get Value From Json keyword failed to find a value for {json_path}")
        return [match.value for match in rv]

    def update_value_to_json(self, json_object, json_path, new_value):
        """Update value to JSON using JSONPath

        Arguments:
            - json_object: json as a dictionary object.
            - json_path: jsonpath expression
            - new_value: value to update

        Return new json_object

        Examples:
        | ${json_object}=  |  Update Value To Json | ${json} |  $..address.streetAddress  |  Ratchadapisek Road |
        """
        json_path_expr = self._parse(json_path)
        json_object_cpy = deepcopy(json_object)
        for match in json_path_expr.find(json_object_cpy):
            path = match.path
            if isinstance(path, Index):
                match.context.value[match.path.index] = new_value
            elif isinstance(path, Fields):
                match.context.value[match.path.fields[0]] = new_value
        return json_object_cpy

    def delete_object_from_json(self, json_object, json_path):
        """Delete Object From JSON using json_path

        Arguments:
            - json_object: json as a dictionary object.
            - json_path: jsonpath expression

        Return new json_object

        Examples:
        | ${json_object}=  |  Delete Object From Json | ${json} |  $..address.streetAddress  |
        """
        json_path_expr = self._parse(json_path)
        json_object_cpy = deepcopy(json_object)
        for match in reversed(json_path_expr.find(json_object_cpy)):
            path = match.path
            if isinstance(path, Index):
                del match.context.value[match.path.index]
            elif isinstance(path, Fields):
                del match.context.value[match.path.fields[0]]
        return json_object_cpy

    @staticmethod
    def convert_json_to_string(json_object):
        """Convert JSON object to string

        Arguments:
            - json_object: json as a dictionary object.

        Return new json_string

        Examples:
        | ${json_str}=  |  Convert JSON To String | ${json_obj} |
        """
        return json.dumps(json_object)

    @staticmethod
    def convert_string_to_json(json_string):
        """Convert String to JSON object

        Arguments:
            - json_string: JSON string

        Return new json_object

        Examples:
        | ${json_object}=  |  Convert String to JSON | ${json_string} |
        """
        return json.loads(json_string)

    def dump_json_to_file(self, dest_file, json_object, encoding=None):
        """Dump JSON to file

        Arguments:
            - dest_file: destination file
            - json_object: json as a dictionary object.

        Export the JSON object to a file

        Examples:
        |  Dump JSON To File  | ${OUTPUT_DIR)${/}output.json | ${json} |
        """
        json_str = self.convert_json_to_string(json_object)
        with open(dest_file, "w", encoding=encoding) as json_file:
            json_file.write(json_str)
        return str(dest_file)

    def should_have_value_in_json(self, json_object, json_path):
        """Should Have Value In JSON using JSONPath

        Arguments:
            - json_object: json as a dictionary object.
            - json_path: jsonpath expression

        Fail if no value is found

        Examples:
        |  Should Have Value In Json  | ${json} |  $..id_card_number |
        """
        try:
            self.get_value_from_json(json_object, json_path, fail_on_empty=True)
        except AssertionError:
            fail(f"No value found for path {json_path}")

    def should_not_have_value_in_json(self, json_object, json_path):
        """Should Not Have Value In JSON using JSONPath

        Arguments:
            - json_object: json as a dictionary object.
            - json_path: jsonpath expression

        Fail if at least one value is found

        Examples:
        |  Should Not Have Value In Json  | ${json} |  $..id_card_number |
        """
        try:
            rv = self.get_value_from_json(json_object, json_path, fail_on_empty=True)
        except AssertionError:
            pass
        else:
            fail(f"Match found for parent {json_path}: {rv}")

    def validate_json_by_schema_file(
        self, json_object, path_to_schema, encoding=None
    ) -> None:
        """Validate json object by json schema file.
        Arguments:
            - json_object: json as a dictionary object.
            - json_path: path to file with json schema

        Fail if json object does not match the schema

        Examples:
        | Simple | Validate Json By Schema File  |  {"foo":bar}  |  ${CURDIR}${/}schema.json |
        """
        with open(path_to_schema, encoding=encoding) as f:
            self.validate_json_by_schema(json_object, json.load(f))

    @staticmethod
    def validate_json_by_schema(json_object, schema) -> None:
        """Validate json object by json schema.
        Arguments:
            - json_object: json as a dictionary object.
            - schema: schema as a dictionary object.

        Fail if json object does not match the schema

        Examples:
        | Simple | Validate Json By Schema  |  {"foo":bar}  |  {"$schema": "https://schema", "type": "object"} |
        """
        try:
            jsonschema.validate(json_object, schema)
        except jsonschema.ValidationError as e:
            fail(f"Json does not match the schema: {e.schema}")
        except jsonschema.SchemaError as e:
            fail(f"Json schema error: {e}")
