---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
[Malik Ceesay & Yazid Heimur]

{: .no_toc }
# Architecture

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

**Quiz Learning** is a Flask-based web application that enables users to enhance their knowledge through interactive quizzes. It features a dynamic progress tracking system, categorized questions, and visual statistics. The application combines Python backend processing with a modern frontend to deliver an engaging learning experience through immediate feedback and performance analytics.

## Codemap

Here is how the codebase of the application is organized:

```
Quiz-App/
│   add_questions.py
│   app.py
├── static/
│   ├── css/
│   │   ├── all_questions.css
│   │   ├── auth.css
│   │   ├── base.css
│   │   ├── categories.css
│   │   ├── components.css
│   │   ├── dashboard.css
│   │   ├── index.css
│   │   ├── profile.css
│   │   ├── quiz.css
│   │   └── sidebar.css
│   └── images/
│       └── quiz-logo.png
├── templates/
│   ├── all_questions.html
│   ├── categories.html
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   ├── profile.html
│   ├── question.html
│   ├── quiz_result.html
│   ├── register.html
│   └── sidebar.html
├── docs/
│   ├── team-eval/
│   └── technical-docs/
```


## Cross-Cutting Concerns  

### Authentication & Authorization

- Flask-Login handles user authentication and session management
- Users must be logged in to access quiz features and progress tracking
- All passwords are securely hashed before being stored in the database
- Route protection prevents unauthorized access to:
  - Dashboard
  - Quiz interface
  - Profile settings
  - Statistics


### Quiz Logic

The application manages **quiz generation and progress tracking** through a structured flow system.

1. **Quiz Generation:**
   - System selects **5 questions** per quiz session
   - Questions are filtered by **selected category**
   - Random selection ensures **varied learning experience**

2. **Question Processing:**
   - Each question contains:
     - Question text
     - Multiple choice options
     - Correct answer
     - Category assignment

3. **Score Calculation:**
   - System tracks **correct answers**
   - Calculates **percentage score**
   - Updates **category statistics**

4. **Progress Tracking:**
   - Stores quiz results in database
   - Updates user statistics
   - Generates performance analytics
   - Tracks category-specific progress

5. **Performance Analysis:**
   - Calculates **success rates** per category
   - Identifies **knowledge gaps**
   - Tracks **improvement over time**
   - Generates **visual statistics** 

### File Handling

- All images are stored in static/images

### Security

- Flask-Login manages secure session handling and user access control.
- All passwords are hashed before database storage.
- Route protection ensures only authenticated users can access protected features.