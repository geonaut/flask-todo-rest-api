# -*- coding: utf-8 -*-

import unittest
import app
import json
from base64 import b64encode

class SmokeTests(unittest.TestCase): 

    @classmethod
    def setUpClass(cls):

        pass 

    @classmethod
    def tearDownClass(cls):

        pass

    def setUp(self):

        self.app = app.app.test_client()
        self.app.testing = True
        self.auth_header = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python'))
        }
        self.data = {
            "title": "title here",
            "description": "description",
            "done": False,
        }

    def tearDown(self):

        pass 

    def test_hello_world(self):

        result = self.app.get("http://localhost:5000/")

        self.assertIn('Hello, World!', result.data)

    def test_get_tasks(self):

        result = self.app.get("http://localhost:5000/todo/api/v1.0/tasks", headers=self.auth_header)

        self.assertIn('tasks', result.data)

    def test_put_task_ok(self):

        response = self.app.put('http://localhost:5000/todo/api/v1.0/tasks/1', headers=self.auth_header, data=json.dumps(self.data),
                       content_type='application/json')

        self.assertIn("title here", response.data)

if __name__ == "__main__":
    unittest.main()