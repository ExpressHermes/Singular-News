# Singular News
[![Gitter](https://badges.gitter.im/ExpressHermesOSC/Singular-News.svg)](https://gitter.im/ExpressHermesOSC/Singular-News?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

A news app powered with machine learning to provide personalized feed to the users based on their interactions on the app.

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
- In settings.py inside Indus, replace email settings with your email address and password to allow email verification. Remember to remove these when committing to github.
    ```
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER') # relpace with your email
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') # replace with email password
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
- Add a upstream link to main branch in your cloned repo
    ```
    git remote add upstream https://github.com/ExpressHermes/Singular-News.git
    ```
- Keep your cloned repo upto date by pulling from upstream (this will also avoid any merge conflicts while committing new changes)
    ```
    git pull upstream master
    ```
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

