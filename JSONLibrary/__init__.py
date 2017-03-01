# -*- coding: utf-8 -*-
from JSONLibraryKeywords import JSONLibraryKeywords
from version import VERSION

__author__ = 'Traitanit Huangsri'
__email__ = 'traitanit.hua@gmail.com'
__version__ = VERSION


class JSONLibrary(JSONLibraryKeywords):
    """JSONLibrary is a robotframework testlibrary for manipulating JSON object (dictionary)

    You can get, add, update and delete your json object using JSONPath.

    == JSONPath Syntax ==
    | JSONPath | Description |
    | $        | the root object/element |
    | @        | the current object/element |
    | . or []  | child operator |
    | ..       | recursive descent. JSONPath borrows this syntax from E4X |
    | *        | wildcard. All objects/element regardless their names. |
    | []       | subscript operator. XPath uses it to iterate over element collections and for predicates. In Javascript and JSON it is the native array operator. |
    | [,]      | Union operator in XPath results in a combination of node sets. JSONPath allows alternate names or array indices as a set. |
    | [start:end:step] | array slice operator borrowed from ES4 |
    | ?()      | applies a filter (script) expression. |
    | ()       | script expression, using the underlying script engine. |

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
