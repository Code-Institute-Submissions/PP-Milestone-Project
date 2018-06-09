from app import app, User
import unittest
from flask_login import current_user


class FlaskTestCase(unittest.TestCase):
    
    
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/dashboard', content_type='html/text')
        self.assertEqual(response.status_code, 200)
      
      
    # Login page loads correctly  
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Please Log in' in response.data)   
        
        
    # Login works correctly given correct credentials
    
    def test_correct_signup(self):
        tester = app.test_client(self)
        response = tester.post('/signup', data=dict(username="admin", 
                                                    email="admin@gmail.com", 
                                                    password="adminadmin"), 
                                                    follow_redirects = True)
        self.assertTrue(b'sign' in response.data)     
        
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="admin", password="adminadmin"), 
                                            follow_redirects = True)
        self.assertTrue(b'Please Log in' in response.data)     

    # Login works correctly given incorrect credentials    
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="admin", password="zzz"), 
                                            follow_redirects = True)
        self.assertTrue(b'Field must be between 6' in response.data)                                    
          
        
    # Logout works correctly 
    def test_logout(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="admin", password="adminadmin"), 
                                            follow_redirects = True)
        response = tester.get('/logout', follow_redirects = True)  
        self.assertTrue(b'Please Log in' in response.data) 
    
    # Ensure that main page @logout_required    
    def test_logout_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects = True)
        self.assertTrue(b'Please Log in' in response.data)    
        
    # Ensure that title & default user shows on main page
    def test_title_shows_up(self):
        tester = app.test_client(self)
        response = tester.get('/dashboard')
        self.assertTrue(b'CHARACTERISE YOUR DATASET' in response.data)
        self.assertTrue(b'Guest' in response.data)
        self.assertEqual(response.status_code, 200)
    
    # Ensure that suggested algorithm table shows on add_request page
    def test_table_shows_up(self):
        tester = app.test_client(self)
        response = tester.get('/add_algorithm', follow_redirects = True)
        self.assertTrue(b'Algorithm Name' in response.data)
        self.assertTrue(b'Users already suggested' in response.data)
        self.assertEqual(response.status_code, 200)
        
if __name__ == '__main__':
    unittest.main()