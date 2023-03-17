import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import User, Post

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
        Post.query.delete()
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

        test_post = Post(
            title="Title_test",
            content="Content_test",
            user_id=self.user_id
        )

        db.session.add(test_post)
        db.session.commit()

        self.post_id = test_post.id

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
            #no need for new instance, could create data dictionary outside of c.post
            new_user = User(
            first_name="test2_first",
            last_name="test2_last",
            image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbaLhYs-hfYG1RaqOYxLbsF-wmxK3fG51xl9TKuHKHmw&s",
            )
            #test final redirect page instead
            c.post('/users/new', data={"first-name": new_user.first_name, "last-name": new_user.last_name, "image-url": new_user.image_url })
            self.assertTrue(User.query.filter(User.first_name == "test2_first").count() == 1)
            self.assertTrue(User.query.filter(User.last_name == "test2_last").count() == 1)
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

    def test_user_list_of_posts(self):
        """Tests that a user's posts are displayed as a list
        on user detail page"""

        with self.client as c:
            resp = c.get(f'/users/{self.user_id}')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('Title_test', html)

    def test_add_post(self):
        """Tests new post functionality."""

        with self.client as c:
            c.post(f"users/{self.user_id}/posts/new",
                          data={"title":
                                "Test post 2",
                                "content": "Test content 2"})
            self.assertTrue(Post.query.filter(Post.title == "Test post 2").count() == 1)
            self.assertTrue(Post.query.filter(Post.content == "Test content 2").count() == 1)

    def test_edit_post(self):
        """Tests that a post can be edited."""
        with self.client as c:
            c.post(f"posts/{self.post_id}/edit",
                          data={"title": "Post title edited",
                                "content": "Post content edited"})
            curr_post = Post.query.filter(Post.title == "Post title edited").first()
            self.assertTrue(curr_post.user_id == self.user_id)
            self.assertTrue(Post.query.filter(Post.content == "Post content edited").count() == 1)

    def test_delete_post(self):
        """Tests a post's delete functionality"""

        with self.client as c:
            c.post(f"posts/{self.post_id}/delete")
            self.assertTrue(Post.query.filter(Post.id == self.post_id).count() == 0)


