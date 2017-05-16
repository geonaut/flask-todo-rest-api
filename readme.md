Simple, self-contained RESTful API for a "To Do" list, built with Flask
=======================================================================

This is a small "To Do" app, based on [Miguel Grinberg's](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask) tutorial. It allows the user to interact with a task list, using RESTful API calls. It has custom error handling, Basic authentication, PUT/GET/POST methods and the data is stored in a JSON dictionary.

I have added full unit tests, some integration tests, and I have used Docker-Compose to build a functional Docker container. The unit test coverage can be seen in the `web/cover` folder.

Setup Option 1: virtualenv
==========================

**Requirements:**

-  virtualenv

**Setup:**

-  clone this repo
-  make a virtualenv inside it e.g. `virtualenv venv`
-  activate the venv e.g. `source venv/bin/activate`
-  install the requirements `pip install -r web/requirements.txt`
-  run the app e.g. `python web/app.py`
-  app should be available at http://0.0.0.0:5000

Setup Option 2: Docker
======================

**Requirements:**

-  Docker

**Setup:**

-  clone this repo
-  from within the repo, run `docker-compose build`
-  run the app with `docker-compose up`
-  app should be available at http://0.0.0.0:5000

Using the API
=============

Requires CURL to be installed!

You can interact with the app using CURL. Examples:

```
curl http://0.0.0.0:5000 #Hello, World!
curl -i http://localhost:5000/todo/api/v1.0/tasks #Unauthorized access
curl -u miguel:python -i http://localhost:5000/todo/api/v1.0/tasks #returns all tasks, as JSON
curl -u miguel:python -i http://localhost:5000/todo/api/v1.0/tasks/1 #returns first task
curl -u miguel:python -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks #posts a new task
```

Running the tests
=================

*If you used Docker, the unit tests should have run automatically during the build. You can still run them manually, following the instructions below.*

From the webroot, with the venv activated, run:

`nosetests --with-coverage --cover-html --cover-erase --cover-package=app`

to get:
```
......................
Name     Stmts   Miss  Cover
----------------------------
app.py      66      1    98%
----------------------------------------------------------------------
Ran 22 tests in 0.502s

OK

```

This will output your code coverage report, which you can view by opening `/web/cover/index.html`


