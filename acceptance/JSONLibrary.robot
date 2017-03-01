*** Settings ***
Library    JSONLibrary
Default Tags    JSONLibrary

*** Test Cases ***
Addition
    [Documentation]    Test Addition Success
    ${result}=    Add Numbers    ${-10}   ${20}    ${50}
    Should Be Equal As Integers    ${result}   ${60}

Subtraction
    [Documentation]    Test Subtraction Success
    ${result}=    Subtract Numbers    ${44}    ${21}
    Should Be Equal As Integers    ${result}    ${23}

Multiplication
    [Documentation]    Test Multiplication Success
    ${result}=    Multiply Numbers    ${11}    ${11}
    Should Be Equal As Integers    ${result}    ${121}

Division
    [Documentation]    Test Division Success
    ${result}=    Divide Numbers    ${121}    ${11}
    Should Be Equal As Integers    ${result}    ${11}

Modulo
    [Documentation]    Test Modulo Success
    ${remainder}=    Mod Numbers    ${121}    ${21}
    Should Be Equal As Integers    ${remainder}    ${16}
