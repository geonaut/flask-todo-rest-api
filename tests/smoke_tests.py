# -*- coding: utf-8 -*-

import unittest
import app
import requests
import json
from base64 import b64encode

class ErrorTests(unittest.TestCase): 

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
        self.task = {
            'id': app.tasks[-1]['id'] + 1,
            'title': 'title',
            'description': 'description',
            'done': False
            }
        self.data = {
            "title": "title here",
            "description": "description",
            "done": False,
        }

    def tearDown(self):

        pass 

    def test_404(self):

        result = self.app.get('/missing-page') 

        self.assertEqual(result.status_code, 404)
        self.assertIn('Not found', result.data)

    def test_405(self):

        result = self.app.post('**') 

        self.assertEqual(result.status_code, 405)
        self.assertIn('The method is not allowed for the requested URL.', result.data)

    def test_403(self):

        result = self.app.get('/todo/api/v1.0/tasks') 

        self.assertEqual(result.status_code, 403)
        self.assertIn('Unauthorized access', result.data)

    def test_hello_world(self):

        result = self.app.get('/')

        self.assertIn('Hello, World!', result.data)

    def test_password(self):

        response = app.get_password('miguel')

        self.assertEqual('python', response)

    def test_password_error(self):

        response = app.get_password('test')

        self.assertEqual(None, response)

    def test_public_task(self):

        with app.app.app_context():
            response = app.make_public_task(self.task)

        self.assertIn('title', response)

    def test_get_all_tasks(self):

        response = self.app.get('/todo/api/v1.0/tasks', headers=self.auth_header)

        self.assertIn('tasks', response.data)

    def test_get_task(self):

        response = self.app.get('/todo/api/v1.0/tasks/1', headers=self.auth_header)

        self.assertIn('tasks', response.data)

    def test_get_nonexistent_task(self):

        invalidTaskId = app.tasks[-1]['id'] + 1
        response = self.app.get('/todo/api/v1.0/tasks/' + str(invalidTaskId), headers=self.auth_header)

        self.assertIn('Not found', response.data)

    def test_post_task_400(self):

        self.auth_header['title'] = "title here"

        response = self.app.post('/todo/api/v1.0/tasks', headers=self.auth_header)

        self.assertIn('Bad request', response.data)

    def test_post_task_ok(self):

        response = self.app.post('/todo/api/v1.0/tasks', headers=self.auth_header, data=json.dumps(self.data),
                       content_type='application/json')

        self.assertIn("title here", response.data)

    def test_put_task_ok(self):

        response = self.app.put('/todo/api/v1.0/tasks/1', headers=self.auth_header, data=json.dumps(self.data),
                       content_type='application/json')

        self.assertIn("title here", response.data)

    def test_put_task_404(self):
        
        response = self.app.put('/todo/api/v1.0/tasks/0', headers=self.auth_header, data=json.dumps(self.data),
                       content_type='application/json')

        self.assertIn("Not found", response.data)

    def test_put_task_400(self):
        
        response = self.app.put('/todo/api/v1.0/tasks/1', headers=self.auth_header, data=json.dumps(self.data))

        self.assertEqual(response.status_code, 400)

    def test_put_task_400_no_unicode(self):
        
        self.data["title"] = [1,2,3]
        response = self.app.put('/todo/api/v1.0/tasks/1', headers=self.auth_header, data=json.dumps(self.data),
                       content_type='application/json')

        self.assertEqual(400, response.status_code)

    def test_put_task_400_no_unicode_desc(self):
        
        self.data["description"] = [1,2,3]
        response = self.app.put('/todo/api/v1.0/tasks/1', headers=self.auth_header, data=json.dumps(self.data),
                       content_type='application/json')

        self.assertEqual(400, response.status_code)

    def test_put_task_400_no_unicode_done(self):
        
        self.data["done"] = [1,2,3]
        response = self.app.put('/todo/api/v1.0/tasks/1', headers=self.auth_header, data=json.dumps(self.data),
                       content_type='application/json')

        self.assertEqual(400, response.status_code)

    def test_delete_task_fail(self):
        
        response = self.app.delete('/todo/api/v1.0/tasks/0', headers=self.auth_header,
                       content_type='application/json')

        self.assertEqual(404, response.status_code)

    def test_delete_task(self):
        
        taskId = app.tasks[-1]['id']
        response = self.app.delete('/todo/api/v1.0/tasks/' + str(taskId), headers=self.auth_header,
                       content_type='application/json')

        self.assertIn("true", response.data)

if __name__ == "__main__":
    unittest.main()