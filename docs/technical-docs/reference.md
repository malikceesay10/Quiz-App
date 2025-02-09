---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
[Malik Ceesay & Yazid Heimur]

{: .no_toc }
# Reference documentation

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Main Routes

### `index()`

**Route:** `/`

**Methods:** GET

**Purpose:** Renders the application landing page with introduction text and login/register options.

**Sample Output:** HTML template displaying welcome message and authentication options.

---

### `categories()`

**Route:** `/categories`

**Methods:** GET

**Purpose:** Displays all available quiz categories with their descriptions.

**Sample Output:** Template showing categorized quiz options with progress indicators.

---

## User Management

### `get_current_user()`

**Route:** None (Helper function)

**Methods:** None

**Purpose:** Retrieves the currently logged-in user from session data for authentication checks.

**Sample Output:** User object containing username and ID, or None if no active session.

---

### `login()`

**Route:** `/login`

**Methods:** GET, POST

**Purpose:** Authenticates users by validating credentials and initializes user session.

**Sample Output:** Redirect to dashboard on success, or login form with error messages.

---

### `register()`

**Route:** `/register`

**Methods:** GET, POST

**Purpose:** Creates new user accounts after validating username availability and password requirements.

**Sample Output:** Redirect to login page or registration form with validation errors.

---

### `logout()`

**Route:** `/logout`

**Methods:** GET

**Purpose:** Terminates active user session and clears session data for secure logout.

**Sample Output:** Redirect to index page with session terminated.

---

## Quiz System

### `start_quiz()`

**Route:** `/quiz/start/<category>`

**Methods:** GET

**Purpose:** Initializes new quiz session with 5 random questions from selected category.

**Sample Output:** Quiz interface template with first question and multiple choice options.

---

### `show_question()`

**Route:** `/quiz/question/<id>`

**Methods:** GET

**Purpose:** Displays specific quiz question with multiple choice options and progress indicator.

**Sample Output:** Question template with answer choices and current quiz progress.

---

### `submit_answer()`

**Route:** `/quiz/submit`

**Methods:** POST

**Purpose:** Processes submitted answers, calculates score, and updates user statistics.

**Sample Output:** JSON response with answer correctness and updated statistics.

---

### `quiz_result()`

**Route:** `/quiz/result/<quiz_id>`

**Methods:** GET

**Purpose:** Displays detailed quiz results including score, correct/incorrect answers, and category statistics.

**Sample Output:** Result template with score breakdown and performance analytics.

---

## Question Management

### `all_questions_categories()`

**Route:** `/questions`

**Methods:** GET

**Purpose:** Lists all question categories with count and difficulty information.

**Sample Output:** Template showing categorized question overview with statistics.

---

### `show_questions_categories()`

**Route:** `/questions/<category>`

**Methods:** GET

**Purpose:** Displays all questions within selected category for individual practice.

**Sample Output:** Category-specific question list with practice options.

---

### `answer_single_question()`

**Route:** `/question/<id>`

**Methods:** GET, POST

**Purpose:** Handles individual question attempts for targeted practice sessions.

**Sample Output:** Single question interface with immediate feedback.

---

### `submit_single_answer()`

**Route:** `/question/<id>/submit`

**Methods:** POST

**Purpose:** Processes individual question responses and updates practice statistics.

**Sample Output:** JSON response with correctness.

---

## Profile Management

### `profile()`

**Route:** `/profile`

**Methods:** GET

**Purpose:** Displays user profile with account settings and comprehensive statistics.

**Sample Output:** Profile template with user data and performance metrics.

---

### `delete_account()`

**Route:** `/profile/delete`

**Methods:** POST

**Purpose:** Permanently removes user account and associated quiz history.

**Sample Output:** Redirect to index with confirmation message.

---

## Statistics Functions

### `get_user_stats()`

**Route:** None (Helper)

**Methods:** None

**Purpose:** Calculates comprehensive user statistics including average scores and category performance.

**Sample Output:** Dictionary containing quiz counts, success rates, and trending data.

---

### `get_top_categories()`

**Route:** None (Helper)

**Methods:** None

**Purpose:** Identifies user's three best-performing categories based on quiz scores.

**Sample Output:** List of top 3 categories with percentage scores.

---

## Context Processors

### `get_user_results()`

**Route:** None (Template helper)

**Methods:** None

**Purpose:** Retrieves and formats user's quiz history for template rendering.

**Sample Output:** List of quiz results with dates, scores, and categories.