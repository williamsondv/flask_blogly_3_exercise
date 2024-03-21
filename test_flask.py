from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True



db.drop_all()
db.create_all()


class UserTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user and a sample post"""
        Post.query.delete()
        User.query.delete()
        

        user = User(first_name="first_name", last_name="last_name", img_url="image@image.com")
        db.session.add(user)
        db.session.commit()

        post = Post(title = "Post Title", content = "Post Content", user_id = user.id)
        db.session.add(post)
        db.session.commit()
        

       
        self.id = user.id
        self.postid = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('first_name last_name', html)
            

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>first_name last_name</h1>', html)
            self.assertIn('Post Title', html)
            

    def test_users_new(self):
        with app.test_client() as client:
            d = {"first_name": "second_user", "last_name": "second_user", "img_url": "image@image.com"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("second_user", html)

    def test_user_delete(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn('first_name last_name', html)

    def test_post_details(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.postid}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Post Content", html)

    def test_post_edit_form(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.postid}/edit")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Post Content", html)

    def test_post_edit_form(self):
        with app.test_client() as client:
            d = {"post_title": "new title", "post_content": "new content"}
            resp = client.post(f"/posts/{self.postid}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("new title", html)