import unittest
from flask_testing import TestCase
from app import app, db, User
from flask_login import current_user


class BaseTestCase(TestCase):
    ## base test case
    
    def create_app(self):
        app.config.from_object('app.TestConfig')
        return app
        
    def setUp(self):
        db.create_all()
        db.session.add(User(username="tester", email="tester@gmail.com", password="testertester"))
        db.session.commit()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    
    ## url tests
    def test_index(self):
        response = self.client.get('/dashboard', content_type='html/text')
        self.assertEqual(response.status_code, 200)
      
      
    
    
        
class UsersViewsTests(BaseTestCase):
    
    # Login page loads correctly  
    def test_login_page_loads(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Please Log in' in response.data)   
        
        
    # Login works correctly given correct credentials
    def test_correct_login(self):
        response = self.client.post('/login', data=dict(username="tester", password="testertester"), 
                                            follow_redirects = True)
        self.assertEqual(response.status_code, 200)
                          
      
    # Login works correctly given incorrect credentials    
    def test_incorrect_login(self):
        response = self.client.post('/login', data=dict(username="admin", password="zzz"), 
                                            follow_redirects = True)
        self.assertTrue(b'Field must be between 6' in response.data)                                    
          
        
    # Logout works correctly 
    def test_logout(self):
        response = self.client.post('/login', data=dict(username="admin", password="adminadmin"), 
                                            follow_redirects = True)
        response = self.client.get('/logout', follow_redirects = True)  
        self.assertTrue(b'Please Log in' in response.data) 
    
    # Ensure that main page @logout_required    
    def test_logout_requires_login(self):
        response = self.client.get('/logout', follow_redirects = True)
        self.assertTrue(b'Please Log in' in response.data)    
        
    # Ensure that title shows on main page
    def test_title_shows_up(self):
        response = self.client.post('/dashboard', data=dict(username="admin", password="adminadmin"), 
                                            follow_redirects = True)
        self.assertTrue(b'CHARACTERISE YOUR DATASET' in response.data)    
    
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    unittest.main()