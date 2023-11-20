*** Settings ***
Library         JSONLibrary
Library         Collections
Library         String
Library         OperatingSystem    
Test Setup      SetUp Test
Default Tags    JSONLibrary

*** Keywords ***
SetUp Test
    ${json}=    Load Json From File    ${CURDIR}${/}..${/}tests${/}json${/}example.json
    Set Test Variable    ${json_obj_input}    ${json}
    Set Test Variable    ${json_obj_orignal}    ${json}

*** Test Cases ***
TestAddJSONObjectByJSONPath
    [Documentation]  Adding some json object using JSONPath
    ${object_to_add}=    Create Dictionary    latitude=13.1234    longitude=130.1234
    ${json_obj1}=    Add Object To Json     ${json_obj_input}    $..address    ${object_to_add}
    Dictionary Should Contain Sub Dictionary    ${json_obj1['address']}    ${object_to_add}
    ${json_obj2}=    Add Object To Json     ${json_obj1}    $.friends    ${None}
    Dictionary Should Not Contain Key    ${json_obj1}    friends
    Dictionary Should Contain Key    ${json_obj2}    friends
    Dictionaries Should Be Equal    ${json_obj_orignal}      ${json_obj_input}

TestGetValueByJSONPath
    [Documentation]  Get some json object using JSONPath
    ${values}=     Get Value From Json    ${json_obj_input}    $..address.postalCode
    Should Be Equal As Strings    ${values[0]}    630-0192

    ${values}=     Get Value From Json    ${json_obj_input}    $..errorField
    ${size}=  Get Length  ${values}
    Should Be Equal As Integers    ${size}    0

TestErrorGetValueByJSONPath
    [Documentation]  Check Get Value From Json can fail if no match is found
    Run Keyword And Expect Error    *failed to find*    Get Value From Json    ${json_obj_input}    $..errorField  fail_on_empty=${True}

TestUpdateValueByJSONPath
    [Documentation]  Update value to json object using JSONPath
    ${json_obj}=    Update Value To Json    ${json_obj_input}    $..address.city    Bangkok
    ${updated_city}=    Get Value From Json    ${json_obj}    $..address.city
    Should Be Equal As Strings    ${updated_city[0]}    Bangkok
    Dictionaries Should Be Equal    ${json_obj_orignal}      ${json_obj_input}

TestShouldHaveValueByJSONPath
    [Documentation]  Check a value can be found in json object using JSONPath
    Should Have Value In Json    ${json_obj_input}    $..isMarried

    Run Keyword And Expect Error  *No value found*  Should Have Value In Json    ${json_obj_input}    $..hasSiblings

TestShouldNotHaveValueByJSONPath
    [Documentation]  Check a value cannot be found in json object using JSONPath
    Should Not Have Value In Json    ${json_obj_input}    $..hasSiblings

    Run Keyword And Expect Error  *Match found*  Should Not Have Value In Json    ${json_obj_input}    $..isMarried

TestInvalidSyntaxByJSONPath
    [Documentation]  Check that an invalid syntax fail the test and doesn't crash Robot
    ${value}=    Get Value From Json    ${json_obj_input}    $.bankAccounts[?(@.amount>=100)].bank
    Should Be Equal As Strings  "${value}"  "['WesternUnion', 'HSBC']"
    Run Keyword And Expect Error   Parser failed to understand syntax *
    ...     Get Value From Json    ${json_obj_input}    $.bankAccounts[?(@.amount=>100)].bank

TestDeleteObjectByJSONPath
    [Documentation]  Delete object from json object using JSONPath
    ${json_obj}=    Delete Object From Json    ${json_obj_input}    $..isMarried
    Dictionary Should Not Contain Key    ${json_obj}    isMarried
    Dictionaries Should Be Equal    ${json_obj_orignal}      ${json_obj_input}

TestDeleteArrayElementsByJSONPath
    [Documentation]  Delete array elements from json object using JSONPath
    ${json_obj1}=    Delete Object From Json    ${json_obj_input}    $..phoneNumbers[0]
    Length Should Be    ${json_obj1['phoneNumbers']}    2
    ${json_obj2}=    Delete Object From Json    ${json_obj1}    $..phoneNumbers[*]
    Length Should Be    ${json_obj1['phoneNumbers']}    2
    Length Should Be    ${json_obj2['phoneNumbers']}    0
    Dictionaries Should Be Equal    ${json_obj_orignal}      ${json_obj_input}

TestConvertJSONToString
    [Documentation]  Convert Json To String
    ${json_str}=    Convert Json To String    ${json_obj_input}
    Should Be String    ${json_str}

TestEnsureAsciiDefault
    ${data} =   Set Variable    "{'test':'ueber'}"
    ${json} =    Convert String To Json    ${data}
    ${string} =     Convert Json To String    ${json}
    Should Be Equal    ${string}   ${data}

TestEnsureAsciiFalse
    ${data} =   Set Variable    "{'test':'über'}"
    ${json} =    Convert String To Json    ${data}
    ${string} =     Convert Json To String    ${json}   ensure_ascii=False
    Should Be Equal    ${string}   ${data}

TestDumpJSONToFile
    [Documentation]    Dumps Json to file
    Dump Json to file    ${TEMPDIR}/sample_dump.json    ${json_obj_input}
    File Should Exist    ${TEMPDIR}/sample_dump.json

TestValidateJsonBySchemaFile
    [Documentation]    Validate Json by schema file
    Validate Json By Schema File    ${json_obj_input}   ${CURDIR}${/}..${/}tests${/}json${/}example_schema.json

TestValidateJsonBySchema
    [Documentation]    Validate Json by schema
    ${schema}    Load Json From File    ${CURDIR}${/}..${/}tests${/}json${/}example_schema.json
    Validate Json By Schema    ${json_obj_input}   ${schema}

TestValidateJsonBySchemaFileFail
    [Documentation]    Validate Json by schema file and fail
    ${new_json}   Delete Object From Json    ${json_obj_input}    $..phoneNumbers
    Run Keyword And Expect Error    * is a required property, Schema path: *
    ...     Validate Json By Schema File    ${new_json}   ${CURDIR}${/}..${/}tests${/}json${/}example_schema.json

TestValidateJsonBySchemaFail
    [Documentation]    Validate Json by schema and fail
    ${schema}    Load Json From File    ${CURDIR}${/}..${/}tests${/}json${/}example_schema.json
    ${new_json}   Delete Object From Json    ${json_obj_input}    $..phoneNumbers
    Run Keyword And Expect Error    * is a required property, Schema path: *
    ...     Validate Json By Schema    ${new_json}   ${schema}

TestValidateJsonByInvalidSchemaFile
    [Documentation]    Validate Json by invalid schema file
    Run Keyword And Expect Error    Json schema error: *
    ...     Validate Json By Schema File    ${json_obj_input}   ${CURDIR}${/}..${/}tests${/}json${/}broken_schema.json

TestValidateJsonByInvalidSchema
    [Documentation]    Validate Json by invalid schema
    ${schema}    Load Json From File    ${CURDIR}${/}..${/}tests${/}json${/}broken_schema.json
    Run Keyword And Expect Error    Json schema error: *
    ...     Validate Json By Schema    ${json_obj_input}   ${schema}
