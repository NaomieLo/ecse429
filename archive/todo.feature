
############################## STORY 1 ##############################

Feature: Retrieve Todos
  As a user, I want to retrieve a list of todos so that I can see all my tasks.

  Background:
    Given the API is responsive
    And the database contains several todos

  # Normal Flow
  Scenario Outline: Successfully retrieve all todos
    When the user retrieves all todos
    Then the status code 200 will be received
    And the response contains a list of todos
    And the todo with title "<todo_name>" is included in the list

    Examples:
      | todo_name           |
      | Grocery Shopping    |
      | Complete Homework   |
      | Pay Bills           |

  # Alternate Flow
  Scenario: Retrieve todos when there are no todos available
    Given the database is empty
    When the user retrieves all todos
    Then the status code 200 will be received
    And the response contains an empty list

  # Error Flow
  Scenario: Fail to retrieve todos due to server error
    Given the API is down
    When the user retrieves all todos
    Then the status code 500 will be received
    And an error message "Internal Server Error" will be displayed

############################ END STORY 1 ############################

############################## STORY 2 ##############################

Feature: Update Todo
  As a user, I want to update an existing todo so that I can correct or change its details.

  Background:
    Given the API is responsive
    And there is an existing todo with title "Old Title" and description "Old Description"

  # Normal Flow
  Scenario Outline: Successfully update a todo's title and description
    When the todo with id "<todo_id>" is updated with title "<new_title>" and description "<new_description>"
    Then the status code 200 will be received
    And the todo with id "<todo_id>" has title "<new_title>" and description "<new_description>"

    Examples:
      | todo_id | new_title         | new_description          |
      | 1       | Updated Title 1   | Updated Description 1    |
      | 2       | New Grocery List  | Buy fruits and vegetables |
      | 3       | Updated Homework  | Complete the science project |

  # Alternate Flow
  Scenario: Update a todo with only a new title
    When the todo with id "1" is updated with title "Updated Title Only"
    Then the status code 200 will be received
    And the todo with id "1" has title "Updated Title Only" and retains its original description

  # Error Flow
  Scenario: Fail to update a non-existent todo
    When the user attempts to update a todo with id "9999" with title "Non-Existent"
    Then the status code 404 will be received
    And an error message "Todo not found" will be displayed


############################ END STORY 2 ############################

############################## STORY 3 ##############################

Feature: Delete Todo
  As a user, I want to delete an existing todo so that I can remove tasks I no longer need.

  Background:
    Given the API is responsive
    And there is an existing todo with title "Temporary Todo" in the database

  # Normal Flow
  Scenario: Successfully delete a todo by ID
    When the user deletes the todo with id "1"
    Then the status code 204 will be received
    And the todo with id "1" should no longer exist in the database

  # Alternate Flow
  Scenario: Delete a todo that is already marked as completed
    Given the todo with id "2" is marked as completed
    When the user deletes the completed todo with id "2"
    Then the status code 204 will be received
    And the completed todo with id "2" should no longer exist in the database

  # Error Flow
  Scenario: Fail to delete a non-existent todo
    When the user attempts to delete a todo with id "9999"
    Then the status code 404 will be received
    And an error message "Todo not found" will be displayed


############################ END STORY 3 ############################

############################## STORY 4 ##############################

Feature: Retrieve Categories for a Todo
  As a user, I want to retrieve all categories linked to a specific todo so that I can see how my tasks are categorized.

  Background:
    Given the API is responsive
    And there is an existing todo with title "Test Todo" linked to categories "Work" and "Personal"

  # Normal Flow
  Scenario: Successfully retrieve all categories for a todo
    When the user retrieves categories for the todo with id "1"
    Then the status code 200 will be received
    And the response contains categories "Work" and "Personal"

  # Alternate Flow
  Scenario: Retrieve categories when a todo is not linked to any category
    Given the todo with id "2" is not linked to any category
    When the user retrieves categories for the todo with id "2"
    Then the status code 200 will be received
    And the response contains an empty list

  # Error Flow
  Scenario: Fail to retrieve categories for a non-existent todo
    When the user attempts to retrieve categories for a todo with id "9999"
    Then the status code 404 will be received
    And an error message "Todo not found" will be displayed


############################ END STORY 4 ############################

############################## STORY 5 ##############################

Feature: Link Task to Todo
  As a user, I want to link a new task to an existing todo so that I can associate detailed steps or actions with my todos.

  Background:
    Given the API is responsive
    And there is an existing todo with title "Test Todo" and description "Test description"

  # Normal Flow
  Scenario: Successfully link a new task to a todo
    When a new task with title "New Task" and description "Task description" is created for the todo with id "1"
    Then the status code 201 will be received
    And the task with title "New Task" should be linked to the todo with id "1"

  # Alternate Flow
  Scenario: Link multiple tasks to the same todo
    When the user creates tasks with titles "Task 1" and "Task 2" for the todo with id "1"
    Then the status code 201 will be received for each task
    And both tasks should be linked to the todo with id "1"

  # Error Flow
  Scenario: Fail to link a task to a non-existent todo
    When the user attempts to create a task with title "Orphan Task" for a todo with id "9999"
    Then the status code 404 will be received
    And an error message "Todo not found" will be displayed


############################ END STORY 5 ############################