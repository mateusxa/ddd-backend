Feature: User login
  As a user
  I want to log in to my account
  So that I can access restricted features

Scenario: Successful login
  Given I am on the login page
  When I enter my username and password
  And I click the login button
  Then I should be redirected to the dashboard
  And I should see a welcome message
