from django.http import response
from django.test import TestCase
from users.models import User 
from .models import Task
from rest_framework.test import APITestCase
from rest_framework import status


class TaskModelTest(TestCase):
    #the method that runs before every test (for prepration data)
    def setUp(self):
        self.user = User.objects.create(phone_number="09120000000")
        self.task = Task.objects.create(
            owner=self.user, 
            title="learn tdd", 
            priority="high",
            description="Test description" 
        ) 

    def test_task_string_representation(self):
        self.assertEqual(str(self.task), "learn tdd")

    def test_task_priority(self):
        self.assertEqual(self.task.priority, "high")
        
class TaskAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(phone_number="09129999999")

        #this method is for rest_framework that simulat login whitout any token and authentication 
        self.client.force_authenticate(user=self.user)

        self.url = '/api/tasks/'
        
    def test_create_task_authorized(self):
        """
        we test that the logined user can made task
        """    
        
        data = {
            "title": "Test via api",
            "description": "Test description",
            "priority": "high",
            "status": "todo"
        }
        #POST request
        response = self.client.post(self.url, data, format='json')

        #assertations
        #1 is 201 code is created?
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        #2 is it saved in database?
        self.assertEqual(Task.objects.count(), 1)

        #3 is right the owner of the task?
        created_task = Task.objects.filter(title="Test via api").first()
        self.assertIsNotNone(created_task)
        self.assertEqual(created_task.owner, self.user)
        
        #verify response data
        self.assertEqual(response.data['title'], "Test via api")
        
    def test_create_task_unauthorized(self):
        """
        we test here the unlogined user cant made a task
        """
        #first loged out the user
        self.client.force_authenticate(user=None)
        
        data = {
            "title": "hacker task",
            "description": "Unauthorized task" 
        }
        response = self.client.post(self.url, data, format='json')
        
        #we expected 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_update_own_task(self):
        """
        we test the user can edit his own tasks
        """

        #1 make task for user
        task = Task.objects.create(owner=self.user, title='old title', priority='low')

        #2 url task
        url = f'/api/tasks/{task.id}/'

        #3 send request
        data = {'title':'new update title'}
        response = self.client.patch(url, data)

        #4 asseration
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #5 chack changing in database
        task.refresh_from_db() 
        self.assertEqual(task.title, 'new update title')
        
    def test_user_can_delete_own_task(self):
        task = Task.objects.create(owner=self.user,title="to delete", description="will be deleted")     
        url = f'/api/tasks/{task.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())
        
    def test_user_cannot_delete_other_tasks(self):
        """
        test the user can not delete the other tasks
        """    
        
        #1 creat a user
        other_user = User.objects.create(phone_number='09300000000')

        #2 make a task for this number
        other_task = Task.objects.create(owner=other_user, title='secret task')

        #3 we are loged in with our user and try to remove the delete the task of other_user
        url = f'/api/tasks/{other_task.id}/'
        response = self.client.delete(url)
        
        #4 assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_user_can_view_own_task(self):
        task = Task.objects.create(owner=self.user, title='my task', description='my description')    

        url = f'/api/tasks/{task.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'my task')
        
    def test_update_task_with_put(self):
        task = Task.objects.create(
            owner=self.user,
            title='title',
            description='description',
            status='todo'
        ) 
        
        url = f'/api/tasks/{task.id}/'
        data = {
            'title':'new title',
            'description':'new descrioption',
            'status':'in_progress',
            'priority':'low'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'new title')
        self.assertEqual(task.priority, 'low')
        
    def create_task_with_tags(self):
        data = {
            'title':'task with tags',
            'description':'Description',
            'tags':['tag1', 'tag2']
        }    
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.setatus_code, status.HTTP_201_CREATED)
        task = Task.objects.get(title='new title')
        self.assertTrue(task.tags.filter(name='tag1').exists())
        self.assertTrue(task.tags.filter(name='tag2').exists())

class TaskFilterSearchTest(APITestCase):
    
    def setUp(self):
        #1 make user and login        
        self.user = User.objects.create(phone_number='09120000000')
        self.client.force_authenticate(user=self.user)
        self.url = '/api/tasks/'

        #2 make some tasks for testing
        task1=Task.objects.create(owner=self.user, title='buy milk', status='todo', priority='low')
        task2=Task.objects.create(owner=self.user, title='gym', status='in_progress', priority='medium')
        task3=Task.objects.create(owner=self.user, title='buy beard', status='done', priority='high')
        
    def test_filter_by_status(self):
        """
        test status=todo
        """
        #send request with query
        response = self.client.get(f'{self.url}?status=todo')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_filter_by_priority(self):
        """
        priority=medium ----> return this
        """    

        response = self.client.get(f'{self.url}?priority=medium')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'gym')

    def search_by_functionality(self):
        """
        test search te word is okey
        """
        response = self.client.get(f'{self.url}?search=buy')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_create_task_validation_error(self):
        """
        test if we dont send title for task we got a 400 error
        """    

        data={
            "description":"no title",
            "priority":"low"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # we check error must be because of nothing title
        self.assertIn('title', response.data)