---
title: Design Decisions
nav_order: 3
---

{: .label }
[Malik Ceesay & Yazid Heimur]

{: .no_toc }
# Design Decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Database: SQLite

### Meta
- Date: November 2024
- Status: Decided

### Problem Statement
For our Quiz-App, we needed a database solution that would allow quick development iterations and easy deployment. As a learning-focused project with a moderate data volume, we didn't require enterprise-level database features but needed reliable data persistence and quick query performance for quiz sessions.

### Decision
We chose SQLite because it perfectly matches our project's scale and deployment needs. The file-based nature makes it ideal for our development process and allows us to easily package the entire application, including the database, as a single unit. This simplifies deployment and testing significantly.

### Regarded Options
- SQLite: File-based, serverless
- PostgreSQL: requires server setup
- MySQL: requires server setup

## ORM: SQLAlchemy

### Meta
- Date: November 2024
- Status: Decided

### Problem Statement
Our Quiz-App requires complex database operations, especially for quiz results and statistics calculations. We needed a solution that would make these operations maintainable and reduce the risk of SQL injection while keeping the code readable for future maintenance.

### Decision
SQLAlchemy through Flask-SQLAlchemy was chosen because it provides clear model definitions for our quiz entities and simplifies complex queries for our statistics features. It particularly helped with implementing the relationship between users, quiz results, and questions, making it easier to track user progress and calculate performance metrics.

## Authentication: Session-Based

### Meta
- Date: November 2024
- Status: Decided

### Problem Statement
Our Quiz-App needed a user authentication system that could handle multiple concurrent users while maintaining session state during quiz attempts. The solution needed to be reliable enough to prevent unauthorized access to quiz results and user profiles.

### Decision
Session-based authentication proved ideal for our use case as it maintains user state throughout quiz sessions and seamlessly handles multiple users taking quizzes simultaneously. It also provides a straightforward way to store temporary quiz progress when users are answering questions.

## Password Security: Werkzeug

### Meta
- Date: November 2024
- Status: Decided

### Problem Statement
We needed a secure way to hash and verify user passwords.

### Decision
We chose Werkzeug's security utilities for its strong security and Flask integration.

### Regarded Options
- Werkzeug: Built into Flask ecosystem, strong security
- Bcrypt: Would require additional dependency
- Plain text: Not secure, never an option

## Single Question Mode

### Meta
- Date: December 2024
- Status: Decided

### Problem Statement
During testing, we realized that users might want to practice specific questions or topics without committing to a full 5-question quiz. This was especially important for users who wanted to focus on areas where they previously struggled.

### Decision
Implementing single question mode significantly improved the learning experience by allowing users to practice specific topics more efficiently. For example, if a user performed poorly in a particular category, they can now focus on individual questions from that category without having to complete entire quizzes.

### Regarded Options
- Full quiz only: Traditional approach, but less flexible
- Single questions: More flexible, better for practice
- Mixed mode: Support both approaches

## Detailed Statistics

### Meta
- Date: December 2024
- Status: Decided

### Problem Statement
For a learning platform, basic pass/fail feedback isn't sufficient. Users needed detailed insights into their performance patterns to effectively improve their knowledge. This is crucial for maintaining user engagement and supporting actual learning progress.

### Decision
Our comprehensive statistics system provides actionable insights by showing users their strengths and weaknesses across different categories. For instance, if a user consistently scores low in a specific category, this becomes immediately apparent through the statistics dashboard, allowing them to focus their practice accordingly.

### Regarded Options
- Basic stats (just scores)
- Detailed stats with categories
- Full analytics dashboard

## Category System

### Meta
- Date: November 2024
- Status: Decided

### Problem Statement
With a growing number of quiz questions, we needed an effective way to organize content and help users focus their learning efforts. The system needed to support both structured learning paths and random practice sessions.

### Decision
The category system we implemented supports both focused learning and variety. Users can systematically work through specific topics or challenge themselves with random questions across categories. This flexibility has proven especially valuable for users with different learning preferences.

### Regarded Options
- No categories (all questions random)
- Fixed categories only
- Dynamic category system with user-created categories

## Answer History

### Meta
- Date: December 2024
- Status: Decided

### Problem Statement
A key aspect of learning is understanding mistakes and patterns in wrong answers. We needed a way to provide users with detailed feedback on their quiz attempts while keeping the data structure flexible for future features.

### Decision
We implemented a basic answer history that stores the essential informations about the quiz attempts. While we would have preferred to implement a more comprehensive analytics system with detailed answer patterns, time constraints led us to choose a simpler but still effective solution. The current implementation stores the question, user's answer, correct answer, and correctness status, providing the fundamental feedback users need while leaving room for future enhancements.

### Regarded Options
- Store only scores: Too basic, doesn't support learning from mistakes
- Store basic answer history: Our current implementation, good balance of features and development time
- Comprehensive answer details: Our preferred option, but too time-intensive to implement in the current project phase
  - Would have included detailed answer explanations