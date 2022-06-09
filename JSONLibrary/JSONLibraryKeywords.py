# -*- coding: utf-8 -*-
import io
import json
import os.path
from robot.api import logger
from robot.api.deco import keyword
from robot.utils.asserts import assert_true, fail
from jsonpath_ng import Index, Fields
from jsonpath_ng.ext import parse as parse_ng
from jsonpath_ng.exceptions import JsonPathParserError
from .version import VERSION

__author__ = 'Traitanit Huangsri'
__email__ = 'traitanit.hua@gmail.com'
__version__ = VERSION

def parse(json_path):
    try:
        _rv=parse_ng(json_path)
    except JsonPathParserError as e:
        fail("Parser failed to undestand syntax '{}'. error message: \n{}\n\nYou may raise an issue on https://github.com/h2non/jsonpath-ng".format(json_path,e))
    # let other exceptions crash robot
    return _rv


class JSONLibraryKeywords(object):
    ROBOT_EXIT_ON_FAILURE = True

    @keyword("Load JSON From File")
    def load_json_from_file(self, file_name, encoding=None):
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
        with io.open(file_name,mode='r',encoding=encoding) as json_file:
            data = json.load(json_file)
        return data

    @keyword("Add Object To Json")
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
        json_path_expr = parse(json_path)
        rv=json_path_expr.find(json_object)
        if len(rv):
            for match in rv:
                if type(match.value) is dict:
                    match.value.update(object_to_add)
                if type(match.value) is list:
                    match.value.append(object_to_add)
        else:
            parent_json_path='.'.join(json_path.split('.')[:-1])
            child_name=json_path.split('.')[-1]
            json_path_expr = parse(parent_json_path)
            rv=json_path_expr.find(json_object)
            if len(rv):
                for match in rv:
                    match.value.update({child_name:object_to_add})
            else:
                fail(f"no match found for parent {parent_json_path}")

        return json_object

    @keyword("Get Value From Json")
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
        json_path_expr = parse(json_path)
        rv=json_path_expr.find(json_object)
        # optional: make the keyword fails if nothing was return
        if fail_on_empty is True and (rv is None or len(rv)==0):
            fail(f"Get Value From Json keyword failed to find a value for {json_path}")
        return [match.value for match in rv]

    @keyword("Update Value To Json")
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
        json_path_expr = parse(json_path)
        for match in json_path_expr.find(json_object):
            path = match.path
            if isinstance(path, Index):
                match.context.value[match.path.index] = new_value
            elif isinstance(path, Fields):
                match.context.value[match.path.fields[0]] = new_value
        return json_object

    @keyword("Delete Object From Json")
    def delete_object_from_json(self, json_object, json_path):
        """Delete Object From JSON using json_path

        Arguments:
            - json_object: json as a dictionary object.
            - json_path: jsonpath expression

        Return new json_object

        Examples:
        | ${json_object}=  |  Delete Object From Json | ${json} |  $..address.streetAddress  |
        """
        json_path_expr = parse(json_path)
        for match in reversed(json_path_expr.find(json_object)):
            path = match.path
            if isinstance(path, Index):
                del(match.context.value[match.path.index])
            elif isinstance(path, Fields):
                del(match.context.value[match.path.fields[0]])
        return json_object

    @keyword("Convert JSON To String")
    def convert_json_to_string(self, json_object):
        """Convert JSON object to string

        Arguments:
            - json_object: json as a dictionary object.

        Return new json_string

        Examples:
        | ${json_str}=  |  Convert JSON To String | ${json_obj} |
        """
        return json.dumps(json_object)

    @keyword("Convert String To JSON")
    def convert_string_to_json(self, json_string):
        """Convert String to JSON object

        Arguments:
            - json_string: JSON string

        Return new json_object

        Examples:
        | ${json_object}=  |  Convert String to JSON | ${json_string} |
        """
        return json.loads(json_string)

    @keyword("Dump JSON To File")
    def dump_json_to_file(self, dest_file, json_object, encoding=None):
        """Dump JSON to file

        Arguments:
            - dest_file: destination file
            - json_object: json as a dictionary object.

        Export the JSON object to a file

        Examples:
        |  Dump JSON To File  | ${OUTPUTID)${/}output.json | ${json} |
        """
        json_str = self.convert_json_to_string(json_object)
        with open(dest_file, "w", encoding=encoding) as json_file:
            json_file.write(json_str)
        return str(dest_file)

    @keyword("Should Have Value In Json")
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


    @keyword("Should Not Have Value In Json")
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
            rv=self.get_value_from_json(json_object, json_path, fail_on_empty=True)
        except AssertionError:
            pass
        else:
            fail(f"Match found for parent {json_path}: {rv}")

