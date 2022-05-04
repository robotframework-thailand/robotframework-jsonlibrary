*** Settings ***
Library         JSONLibrary
Library         Collections
Library         String
Library         OperatingSystem    
Test Setup      SetUp Test
Default Tags    JSONLibrary

*** Keywords ***
SetUp Test
    ${json_obj}=    Load JSON From File    ${CURDIR}${/}..${/}tests${/}json${/}example.json
    Set Test Variable    ${json_obj}    ${json_obj}

*** Test Cases ***
TestAddJSONObjectByJSONPath
    [Documentation]  Adding some json object using JSONPath
    ${object_to_add}=    Create Dictionary    latitude=13.1234    longitude=130.1234
    ${json_obj}=    Add Object To Json     ${json_obj}    $..address    ${object_to_add}
    Dictionary Should Contain Sub Dictionary    ${json_obj['address']}    ${object_to_add}

    ${json_obj}=    Add Object To Json     ${json_obj}    $.friends    ${None}
    Dictionary Should Contain Key    ${json_obj}    friends

TestGetValueByJSONPath
    [Documentation]  Get some json object using JSONPath
    ${values}=     Get Value From Json    ${json_obj}    $..address.postalCode
    Should Be Equal As Strings    ${values[0]}    630-0192

TestErrorGetValueByJSONPath
    [Documentation]  Check Get Value From JSON can fail if no match is found
    Run Keyword And Expect Error    *failed to find*    Get Value From Json    ${json_obj}    $..errorField

TestUpdateValueByJSONPath
    [Documentation]  Update value to json object using JSONPath
    ${json_obj}=    Update Value To Json    ${json_obj}    $..address.city    Bangkok
    ${updated_city}=    Get Value From Json    ${json_obj}    $..address.city
    Should Be Equal As Strings    ${updated_city[0]}    Bangkok

TestDeleteObjectByJSONPath
    [Documentation]  Delete object from json object using JSONPath
    ${json_obj}=    Delete Object From Json    ${json_obj}    $..isMarried
    Dictionary Should Not Contain Key    ${json_obj}    isMarried

TestDeleteArrayElementsByJSONPath
    [Documentation]  Delete array elements from json object using JSONPath
    ${json_obj}=    Delete Object From Json    ${json_obj}    $..phoneNumbers[0]
    Length Should Be    ${json_obj['phoneNumbers']}    2
    ${json_obj}=    Delete Object From Json    ${json_obj}    $..phoneNumbers[*]
    Length Should Be    ${json_obj['phoneNumbers']}    0

TestConvertJSONToString
    [Documentation]  Convert JSON To String
    ${json_str}=    Convert JSON To String    ${json_obj}
    Should Be String    ${json_str}

TestDumpJSONToFile
    [Documentation]    Dumps JSON to file
    Dump JSON to file    ${TEMPDIR}/sample_dump.json    ${json_obj}
    File Should Exist    ${TEMPDIR}/sample_dump.json