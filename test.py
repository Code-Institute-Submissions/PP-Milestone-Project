from app import app
import unittest



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
        
    # Ensure that title shows on main page
    def test_title_shows_up(self):
        tester = app.test_client(self)
        response = tester.post('/dashboard', data=dict(username="admin", password="adminadmin"), 
                                            follow_redirects = True)
        self.assertTrue(b'CHARACTERISE YOUR DATASET' in response.data)    
    
        
if __name__ == '__main__':
    unittest.main()