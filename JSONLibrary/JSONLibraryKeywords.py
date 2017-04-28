# -*- coding: utf-8 -*-
from robot.api import logger
from robot.api.deco import keyword
from version import VERSION
import os.path
import json
from jsonpath_rw import Index, Fields
from jsonpath_rw_ext import parse

__author__ = 'Traitanit Huangsri'
__email__ = 'traitanit.hua@gmail.com'
__version__ = VERSION


class JSONLibraryKeywords(object):
    ROBOT_EXIT_ON_FAILURE = True

    @keyword('Load JSON From File')
    def load_json_from_file(self, file_name):
        """Load JSON from file.

        Return json as a dictionary object.

        Arguments:
            - file_name: absolute json file name

        Return json object (list or dictionary)

        Examples:
        | ${result}=  |  Load Json From File  | /path/to/file.json |
        """
        logger.debug("Check if file exists")
        if os.path.isfile(file_name) is False:
            logger.error("JSON file: " + file_name + " not found")
            raise IOError
        with open(file_name) as json_file:
            data = json.load(json_file)
        return data

    @keyword('Add Object To Json')
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
        for match in json_path_expr.find(json_object):
            if type(match.value) is dict:
                match.value.update(object_to_add)
            if type(match.value) is list:
                match.value.append(object_to_add)

        return json_object

    @keyword('Get Value From Json')
    def get_value_from_json(self, json_object, json_path):
        """Get Value From JSON using JSONPath

        Arguments:
            - json_object: json as a dictionary object.
            - json_path: jsonpath expression

        Return array of values

        Examples:
        | ${values}=  |  Get Value From Jsonpath  | ${json} |  $..phone_number |
        """
        json_path_expr = parse(json_path)
        return [match.value for match in json_path_expr.find(json_object)]

    @keyword('Update Value To Json')
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

    @keyword('Delete Object From Json')
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
        for match in json_path_expr.find(json_object):
            path = match.path
            if isinstance(path, Index):
                del(match.context.value[match.path.index])
            elif isinstance(path, Fields):
                del(match.context.value[match.path.fields[0]])
        return json_object

    @keyword('Convert JSON To String')
    def convert_json_to_string(self, json_object):
        """Convert JSON object to string

        Arguments:
            - json_object: json as a dictionary object.

        Return new json_string

        Examples:
        | ${json_str}=  |  Convert JSON To String | ${json_obj} |
        """
        return json.dumps(json_object)

