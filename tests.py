import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import User

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_show_add_user(self):
        """Tests that the add user form appears"""

        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- TEST: CREATE USER FORM -->", html)

    def test_user_added(self):
        """Tests that user added to db"""

        with self.client as c:
            c.post('/users/new', data={"first-name": "Tester", "last-name": "Testerino", "image-url": 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbaLhYs-hfYG1RaqOYxLbsF-wmxK3fG51xl9TKuHKHmw&s'})
            self.assertTrue(User.query.filter(User.first_name == "Tester").count() == 1)
            self.assertTrue(User.query.filter(User.last_name == "Testerino").count() == 1)
            self.assertTrue(User.query.filter(User.image_url == "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbaLhYs-hfYG1RaqOYxLbsF-wmxK3fG51xl9TKuHKHmw&s").count() == 1)

    def test_user_edit(self):
        """Tests that a user's info is edited in database"""
        with self.client as c:
            c.post(f"users/{self.user_id}/edit", data={"first-name": "Tester", "last-name": "Testerino", "image-url": 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbaLhYs-hfYG1RaqOYxLbsF-wmxK3fG51xl9TKuHKHmw&s'})
            self.assertTrue(User.query.filter(User.first_name == "Tester").count() == 1)
            self.assertTrue(User.query.filter(User.last_name == "Testerino").count() == 1)
            self.assertTrue(User.query.filter(User.image_url == "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbaLhYs-hfYG1RaqOYxLbsF-wmxK3fG51xl9TKuHKHmw&s").count() == 1)

    def test_user_delete(self):
        """Tests that a user's info is deleted from database"""

        with self.client as c:
            c.post(f"users/{self.user_id}/delete")
            self.assertTrue(User.query.filter(User.id == self.user_id).count() == 0)