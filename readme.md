Simple, self-contained RESTful API for a "To Do" list, built with Flask
=======================================================================

This is a small "To Do" app, based on [Miguel Grinberg's](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask) tutorial. It allows the user to interact with a task list, using RESTful API calls. It has custom error handling, Basic authentication, PUT/GET/POST methods and the data is stored in a JSON dictionary.

I have added full unit tests, some integration tests, and I have used Docker-Compose to build a functional Docker container. The unit test coverage can be seen in the `web/cover` folder.

Setup
=====

Requirements:

-  