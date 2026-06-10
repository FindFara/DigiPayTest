Feature: Login
  As a DigiPay user
  I want to authenticate with my mobile number
  So that I can access wallet and payment services

  @smoke @login
  Scenario: User reaches OTP step with a valid phone number
    Given the user is on the login page
    When the user submits a valid phone number
    Then the OTP step should be displayed

  @regression @login
  Scenario: User sees validation message for invalid phone number
    Given the user is on the login page
    When the user submits an invalid phone number
    Then a login validation error should be displayed
