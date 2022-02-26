from django.test import TestCase


from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from .models import Task
from .views import GenericTaskView, GenericTaskCreateView


class AllView_Test(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="bruce_wayne", email="bruce@wayne.org", password="i_am_batman")

    def test_user_login(self):
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, 200)

    def test_user_signup(self):
        response = self.client.get("/user/signup/")
        self.assertEqual(response.status_code, 200)

    def test_homepage(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_authenticated_TaskView(self):
        request = self.factory.get("/tasks")
        request.user = self.user
        response = GenericTaskView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_CreateView(self):
        request = self.factory.get("/create-task/")
        request.user = self.user
        response = GenericTaskCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        self.client.login(username="bruce_wayne", password="i_am_batman")
        self.client.post("/create-task/",
                         {
                             "title": "Demo1",
                             "description": "Demo Task",
                             "priority": 1,
                             "completed": False,
                             "status": "PENDING",
                         },
                         )
        self.assertEqual(Task.objects.get(priority=1).description, "Demo Task")

    def test_check_priority(self):
        self.client.login(username="bruce_wayne", password="i_am_batman")
        self.client.post("/create-task/",
                         {
                             "title": "Demo1",
                             "description": "Demo Task",
                             "priority": 1,
                             "completed": False,
                             "status": "PENDING",
                         },
                         )
        self.client.post("/create-task/",
                         {
                             "title": "Demo2",
                             "description": "Demo Task 2",
                             "priority": 1,
                             "completed": False,
                             "status": "PENDING",
                         },
                         )
        self.assertEqual(Task.objects.get(priority=2).description, "Demo Task")

    def test_updateView(self):
        self.client.login(username="bruce_wayne", password="i_am_batman")
        createtask = Task.objects.create(
            title="Demo1",
            description="Demo Task",
            priority=1,
            completed=False,
            status="PENDING",
            user=self.user,
        )
        self.client.post(f"/update-task/{createtask.id}/",
                         {
                             "title": "Demo1",
                             "description": "Demo Task 2",
                             "priority": 1,
                             "completed": False,
                             "status": "PENDING",
                         },
                         )
        self.assertEqual(Task.objects.get(
            id=createtask.id).description, "Demo Task 2")


class ApiTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="bruce_wayne", email="bruce@wayne.org", password="i_am_batman")

    def test_acsessapi(self):
        self.client.login(username="bruce_wayne", password="i_am_batman")
        response = self.client.get(f"/api/task/")
        self.assertEqual(response.status_code, 200)
