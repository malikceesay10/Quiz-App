---
title: Data Model
parent: Technical Docs
nav_order: 2
---

{: .label }
[Malik Ceesay & Yazid Heimur]

{: .no_toc }
# Data Model

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

# Data Model Documentation

This data model represents the core structure of our Quiz-App application. The model consists of three main entities that handle user management, quiz questions, and quiz results.

## User

### Attributes
- `id`: integer (primary key) - Unique identifier
- `username`: string (unique) - User's display name
- `firstname`: string - User's first name
- `lastname`: string - User's last name
- `password_hash`: string - Hashed password

### Relationships
- **User ↔ QuizResult**: 1:m relationship - Each user can have multiple quiz results
- **User ↔ Quiz**: m:n relationship - Users interact with multiple quizzes through quiz attempts

## Quiz

### Attributes
- `id`: integer (primary key) - Unique identifier
- `question`: string - The question text
- `correct_answer`: string - The correct answer
- `wrong_answer1`: string - First incorrect option
- `wrong_answer2`: string - Second incorrect option
- `wrong_answer3`: string - Third incorrect option
- `category`: string - Question category

### Relationships
- **Quiz ↔ QuizResult**: 1:m relationship - Each quiz question can appear in multiple results
- **Quiz ↔ User**: m:n relationship - Quizzes can be taken by multiple users

## QuizResult

### Attributes
- `id`: integer (primary key) - Unique identifier
- `user_id`: integer (foreign key) - Reference to User
- `score`: integer - Number of correct answers
- `category`: string - Category of the quiz taken
- `date`: datetime - When the quiz was taken
- `answers`: text - JSON string storing detailed answer information

### Relationships
- **QuizResult ↔ User**: m:1 relationship - Each result belongs to exactly one user
- **QuizResult ↔ Quiz**: m:1 relationship - Each result references one or more quiz questions
