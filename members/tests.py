from django.test import TestCase
from members.models import User
from datetime import datetime

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(match_id='a', last_update=datetime.now())
        #User.objects.create(match_id='b', last_update=datetime(2014, 1, 1, 13, 0, tzinfo=gmt1))
        User.objects.create(match_id='b', last_update=datetime(2014, 1, 1, 13, 0))
        a = User.objects.get(match_id='a')
        a.save()
        b = User.objects.get(match_id='b')
        b.save()       
        
    def test_can_update(self):
        u = User()
        self.assertEqual(u.too_soon('a'), True, 'should have been too soon to update')
        self.assertEqual(u.too_soon('b'), False, 'should not have been too soon to update')
        self.assertEqual(u.too_soon('b'), True, 'after previous update, should be too soon now')