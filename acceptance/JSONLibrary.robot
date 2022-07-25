*** Settings ***
Library         JSONLibrary
Library         Collections
Library         String
Library         OperatingSystem    
Test Setup      SetUp Test
Default Tags    JSONLibrary

*** Keywords ***
SetUp Test
    ${json}=    Load JSON From File    ${CURDIR}${/}..${/}tests${/}json${/}example.json
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
    [Documentation]  Check Get Value From JSON can fail if no match is found
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

    ${res}=  Run Keyword And return status   Get Value From Json    ${json_obj}    $.bankAccounts[?(@.amount=>100)].bank
    Should Not Be True  ${res} 

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
    [Documentation]  Convert JSON To String
    ${json_str}=    Convert JSON To String    ${json_obj_input}
    Should Be String    ${json_str}

TestDumpJSONToFile
    [Documentation]    Dumps JSON to file
    Dump JSON to file    ${TEMPDIR}/sample_dump.json    ${json_obj_input}
    File Should Exist    ${TEMPDIR}/sample_dump.json