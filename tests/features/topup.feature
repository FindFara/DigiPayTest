Feature: Mobile top-up purchase
  As a DigiPay user
  I want to buy direct mobile top-up
  So that I can recharge a destination phone safely

  @smoke @topup
  Scenario: User starts direct top-up purchase with valid data
    Given the user is on the top-up page
    When the user selects direct top-up
    And the user completes the top-up form with valid data
    And the user continues the top-up purchase
    Then the checkout or login step should be displayed

  @regression @topup
  Scenario: User sees validation message for invalid top-up phone number
    Given the user is on the top-up page
    When the user selects direct top-up
    And the user enters an invalid top-up phone number
    And the user continues the top-up purchase
    Then a top-up validation error should be displayed
