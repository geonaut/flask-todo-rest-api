# -*- coding: utf-8 -*-

import unittest
import app
import requests
import json
from base64 import b64encode

# class TestFlaskApiUsingRequests(unittest.TestCase):
#     def test_hello_world(self):
#         response = requests.get('http://localhost:5000')
#         self.assertEqual(response.content,"Hello, World!")

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

    def tearDown(self):
        pass 

    def test_pagenotfound_statuscode(self):
        result = self.app.get('/missing-page') 

        self.assertEqual(result.status_code, 404) 

    def test_pagenotfound_data(self):
        result = self.app.get('/missing-page') 

        self.assertIn('Not found', result.data)

    def test_unhandledexception_statuscode(self):
        result = self.app.post('**') 

        self.assertEqual(result.status_code, 405) 

    def test_unhandledexception_data(self):
        result = self.app.post('**') 

        self.assertIn('The method is not allowed for the requested URL.', result.data)

    def test_unauthorized_statuscode(self):
        result = self.app.get('/todo/api/v1.0/tasks') 

        self.assertEqual(result.status_code, 403) 

    def test_unauthorized_data(self):
        result = self.app.get('/todo/api/v1.0/tasks') 

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
        task = {
            'id': app.tasks[-1]['id'] + 1,
            'title': 'title',
            'description': 'description',
            'done': False
            }
        with app.app.app_context():
            response = app.make_public_task(task)

        self.assertIn('title', response)

    def test_get_all_tasks(self):
        headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python'))
        }

        response = self.app.get('/todo/api/v1.0/tasks', headers=headers)

        self.assertIn('tasks', response.data)

    def test_get_task(self):
        headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python'))
        }

        response = self.app.get('/todo/api/v1.0/tasks/1', headers=headers)

        self.assertIn('tasks', response.data)

    def test_get_nonexistent_task(self):
        headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python'))
        }
        invalidTaskId = app.tasks[-1]['id'] + 1
        response = self.app.get('/todo/api/v1.0/tasks/' + str(invalidTaskId), headers=headers)

        self.assertIn('Not found', response.data)

    def test_post_task_400(self):
        headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python')),
            'title': "title here"
        }
        response = self.app.post('/todo/api/v1.0/tasks', headers=headers)

        self.assertIn('Bad request', response.data)

    def test_post_task_ok(self):
        headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python')),
        }
        data = {
            "title": "title here",
            "description": "description"
        }
        response = self.app.post('/todo/api/v1.0/tasks', headers=headers, data=json.dumps(data),
                       content_type='application/json')

        self.assertIn("title here", response.data)

    def test_put_task_ok(self):
        headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python')),
        }
        data = {
            "title": "title here",
            "description": "description"
        }
        response = self.app.put('/todo/api/v1.0/tasks/1', headers=headers, data=json.dumps(data),
                       content_type='application/json')

        self.assertIn("title here", response.data)

    def test_put_task_404(self):
        headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python')),
        }
        data = {
            "title": "title here",
            "description": "description"
        }
        response = self.app.put('/todo/api/v1.0/tasks/0', headers=headers, data=json.dumps(data),
                       content_type='application/json')

        self.assertIn("Not found", response.data)

    def test_put_task_400(self):
        headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python')),
        }
        data = {
                    "title": "title here",
                    "description": "description"
                }
        response = self.app.put('/todo/api/v1.0/tasks/1', headers=headers, data=json.dumps(data))

        self.assertEqual(response.status_code, 400)

    def test_put_task_400_no_unicode(self):
        headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python')),
        }
        # s = "Hello"
        data = {
            "title": [1,2,3],
            "description": "description here",
        }
        response = self.app.put('/todo/api/v1.0/tasks/1', headers=headers, data=json.dumps(data),
                       content_type='application/json')

        self.assertEqual(400, response.status_code)

    def test_put_task_400_no_unicode_desc(self):
        headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python')),
        }
        # s = "Hello"
        data = {
            "title": "title here",
            "description": [1,2,3]
        }
        response = self.app.put('/todo/api/v1.0/tasks/1', headers=headers, data=json.dumps(data),
                       content_type='application/json')

        self.assertEqual(400, response.status_code)

    def test_put_task_400_no_unicode_done(self):
        headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python')),
        }
        data = {
            "title": "title here",
            "description": "description here",
            "done": [1,2,3]
        }
        response = self.app.put('/todo/api/v1.0/tasks/1', headers=headers, data=json.dumps(data),
                       content_type='application/json')

        self.assertEqual(400, response.status_code)

    def test_delete_task_fail(self):
        headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python')),
        }
        response = self.app.delete('/todo/api/v1.0/tasks/0', headers=headers,
                       content_type='application/json')

        self.assertEqual(404, response.status_code)

    def test_delete_task(self):
        headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format('miguel', 'python')),
        }
        taskId = app.tasks[-1]['id']
        response = self.app.delete('/todo/api/v1.0/tasks/' + str(taskId), headers=headers,
                       content_type='application/json')

        self.assertIn("true", response.data)

if __name__ == "__main__":
    unittest.main()