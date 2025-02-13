# Quiz Learning

Quiz Learning is an interactive learning application that allows users to enhance their knowledge through categorized quizzes while tracking their progress with visual statistics and progress bars.

In addition to code, this repository includes a Github Pages Documentation: [Quiz Learning Documentation](https://malikceesay10.github.io/Quiz-App/technical-docs/architecture.html).

## Features

- **User Registration and Login**: Secure authentication and session management.
- **Categorized Quizzes**: Choose quiz questions from various categories.
- **Progress Tracking**: Detailed statistics and analysis of learning progress.
- **Profile Management**: Users can update their personal information and passwords.
- **Visual Statistics**: Display success rates and top categories.


## Installation


1. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```

3. Add questions to the database:
    ```bash
    python add_questions.py
    ```

4. Start the application:
    ```bash
    python app.py
    ```

5. Access the application:
    Open your web browser and go to `http://127.0.0.1:5000/`

## Usage

- **Registration**: Create a new user account.
- **Login**: Log in with your username and password.
- **Start Quiz**: Choose a category and start a quiz.
- **Profile**: Manage your personal information and change your password.
- **Statistics**: Track your learning progress and analyze your results.