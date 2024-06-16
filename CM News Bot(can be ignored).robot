*** Settings ***
Documentation       Template robot main suite.
Library    RPA.Browser.Selenium        auto_close=${False}
Library    String
Library    Collections
Library    occurence.py

*** Variables ***
${URL}        https://www.latimes.com

*** Tasks ***
Open Chrome and access LATimes
    Open Chrome and access LATimes    lakers

*** Keywords ***
Open Chrome and access LATimes
    [Arguments]    ${searchphrase}

    Log    Open Chrome and access LATimes started
    Open Available Browser   ${URL}
    Maximize Browser Window
    #Sleep   10
    Wait Until Element Is Visible    css:button[data-element="search-button"]    10 seconds
    Click Element    css:button[data-element="search-button"]
    Input Text When Element Is Visible    css:input[data-element="search-form-input"]    ${searchphrase}
    Click Element    css:button[data-element="search-submit-button"]
    Wait Until Element Is Visible    css:select[name="s"]
    Select From List By Value    css:select[name="s"]    1
    Sleep    1
    Wait Until Page Contains Element    css:div[class="promo-wrapper"]
    ${articles}=    Get WebElements    css:div[class="promo-wrapper"]
    ${count}=     Get length    ${articles}
    Log    Articles found on page: ${count}
    Create List     $(titles)
    FOR    ${article}    IN    @{articles}
        ${title_element}=    Get WebElement    css:h3.promo-title > a    ${article}
        ${title}=    Get Text    ${title_element}
        Log    Title: ${title}
        ${title_count}=    Count search phrases in text    ${title}    ${searchphrase}
        Log    Search phrases in title: ${title_count}

        ${description_element}=    Get WebElement    css:p.promo-description    ${article}
        ${description}=    Get Text    ${description_element}
        Log    Description: ${description}
        ${description_count}=    Count search phrases in text    ${description}    ${searchphrase}
        Log    Search phrases in description: ${description_count}

        ${date_element}=     Get WebElement    css:p[class="promo-timestamp"]    ${article}
        ${date}=    Get Text    ${date_element}
        Log    Date: ${date}

        ${picture_element}=    Get WebElement    css:img    ${article}
        ${picture_source}=    Get Element Attribute    ${picture_element}    src
        ${picture_name}=    Get FileName From URL    ${picture_source}
        Log    Picture: ${picture_name}
    END
    #\    ${title}=    Get Text    xpath=//div[@class="promo-wrapper"][${index}]//h3[@class="promo-title"]/a




Get FileName From URL
    [Arguments]    ${URL}
    ${strings}=    Split String    ${URL}    %2F
    ${filename}=    Get From List    ${strings}    -1
    [Return]    ${filename}

Count search phrases in text
    [Arguments]    ${text}    ${searchphrase}
    ${times}=   0
    #${times}=    Count Occurrences    ${text}    ${searchphrase}
    [Return]    ${times}
#Get data from search


#Write data to excel