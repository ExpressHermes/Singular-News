# Indus-News
A news app powered with machine learning to provide personalized feed to the users based on their interactions on the app.

:warning: The ML part has not been committed because my teammate does not wish to share his algorithm :warning:

#### Uncommitted files list
 * Database scheduling script
 * Feed preparation modules

 # Installation

 ## Prerequsites
 - Python 
 - Django
 - PostgreSQL

 ## How to set up locally
- Fork and clone repo on your machine.
    ```
    git clone https://github.com/ExpressHermes/Singular-News.git
    ```

- Create a virtual environment. Activate it. Make sure it is in the same directory as the cloned repo.

    ```
    # for linux users
    python -m venv <env-name>
    source venv/bin/activate 
    ```
- Install all requirements.
    ```
    pip install -r requirements.txt
    ```
- Inside the project folder, create migrations for the apps `users` and `feeds`
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
- Run the project
    ```
    python manage.py runserver
    ```

# Contribution Guidelines
- Fork and star the repo.
- Create your feature branch
    ```
    git checkout -b <feature-name>
    ```
- Commit all the changes
    ```
    git commit -am "Meaningful commit message"
    ```
- Push the changes for review
    ```
    git push origin <branch-name>
    ```
