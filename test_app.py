import app
from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['Testing'] = True




class Tester(TestCase):

    def setUp(self):
        User.query.delete()
    
    def tearDown(self):
        db.session.rollback()

    def test_route(self):
        with app.test_client() as client:
            res = client.post('/', data={"first":'Yama', "last":'Yugi', "url":""}, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertIn("<li>Yama Yugi</li>", html)

    def test_edit(self):
        with app.test_client() as client:
            res1 = client.get('/', data={"first":'Yama', "last":'Yugi', "url":"", 
                                        "edit":False, "userData":1}, follow_redirects=True)
            res2 = client.get('/', data={"first":'Jack', "last":'Yugi', "url":"", 
                                        "edit":True, "userData":1}, follow_redirects=True)
            html = res2.get_data(as_text=True)
            self.assertIn("<li>Jack Yugi</li>", html)
    
    def test_details(self):
        with app.test_client() as client:
            user = User(first_name="yamaa", last_name="yyugi", image_url="", id="1")
            db.session.add(user)
            db.session.commit()
            res = client.get('/detail/1')
            html = res.get_data(as_text=True)
            print(html)
            self.assertIn("<h1>yamaa yyugi</h1>", html)  

    def test_details(self):
        with app.test_client() as client:
            user = User(first_name="yamaa", last_name="yyugi", image_url="", id="1")
            db.session.add(user)
            db.session.commit()
            res = client.get('/delete/1', follow_redirects=True)
            html = res.get_data(as_text=True)
            print(html)
            self.assertIn("<ul>\n        \n    </ul>", html)  
    
