"""
Models' unit tests
===================
"""

import datetime
from unittest import mock

import pytz
from django.test import TestCase

from contacts.models import Contact

TEST_DATE = datetime.datetime(2017, 4, 10, 12, 00, tzinfo=pytz.utc)


class TestContactModel(TestCase):
    """Class for Contact Model test"""

    def setUp(self):
        """ Create a Contact object to be used by the tests """
        time_mock = datetime.datetime(2017, 4, 10, 12, 00, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = time_mock
            Contact(id=111,
                    first_name='fname',
                    last_name='lname',
                    contact_url='http://day.night',
                    phone_number=1234567,
                    photo='static/images/corgey2.jpeg',
                    country='Ukraine',
                    city='Kyiv',
                    street='Mira').save()

            Contact(id=4,
                    first_name='Day',
                    last_name='Night',
                    contact_url='http://day.com',
                    phone_number='7654321',
                    photo='static/images/cat.jpg',
                    country='Russia',
                    city='Moscow',
                    street='Mira').save()

    def test__str__(self):
        """Test of the Contact.__str__() method"""
        self.maxDiff = None
        user_returned = str(Contact.objects.get(id=111))
        user_to_expect = "'id': 111, " \
                         "'first_name': 'fname', " \
                         "'last_name': 'lname', " \
                         "'contact_url': 'http://day.night', " \
                         "'phone_number': '1234567', " \
                         "'photo': <ImageFieldFile: static/images/corgey2.jpeg>, " \
                         "'country': 'Ukraine', " \
                         "'city': 'Kyiv', " \
                         "'street': 'Mira'"
        self.assertEqual(user_returned, user_to_expect)

    def test__repr__(self):
        """Test of the Contact.__repr__() method"""
        user_returned = repr(Contact.objects.get(id=111))
        user_to_expect = "Contact(id=111)"

        self.assertEqual(user_returned, user_to_expect)

    def test_get_by_id_positive(self):
        """Positive test of the Contact.get_by_id() method"""
        contact_returned = Contact.get_by_id(111)
        self.assertEqual(contact_returned.id, 111)
        self.assertEqual(contact_returned.first_name, 'fname')
        self.assertEqual(contact_returned.last_name, 'lname')
        self.assertEqual(contact_returned.contact_url, 'http://day.night')
        self.assertEqual(contact_returned.phone_number, '1234567')
        self.assertEqual(contact_returned.country, 'Ukraine')
        self.assertEqual(contact_returned.city, 'Kyiv')
        self.assertEqual(contact_returned.street, 'Mira')

    def test_get_by_id_negative(self):
        """Negative test of the Contact.get_by_id() method"""
        user_to_expect = Contact.get_by_id(999)
        self.assertIsNone(user_to_expect)

    def test_delete_by_id_positive(self):
        """ Test of the Contact.delete_by_id() method """
        self.assertTrue(Contact.delete_by_id(4))
        self.assertRaises(Contact.DoesNotExist, Contact.objects.get, pk=4)

    def test_delete_by_id_negative(self):
        """ Test of the Contact.delete_by_id() method """
        self.assertFalse(Contact.delete_by_id(41))

    def test_create_positive(self):
        """ Positive Test of the Contact.create method """

        contact_returned = Contact.create('Sergey', 'Arman', 'http://day.night', '22222222',
                                          'static/images/corgey2.jpeg',
                                          'England', 'London', 'Londonskaya')
        self.assertIsInstance(contact_returned, Contact)
        self.assertEqual(contact_returned.first_name, 'Sergey')
        self.assertEqual(contact_returned.last_name, 'Arman')
        self.assertEqual(contact_returned.contact_url, 'http://day.night')
        self.assertEqual(contact_returned.phone_number, '22222222')
        self.assertEqual(contact_returned.photo, 'static/images/corgey2.jpeg')
        self.assertEqual(contact_returned.country, 'England')
        self.assertEqual(contact_returned.city, 'London')
        self.assertEqual(contact_returned.street, 'Londonskaya')

    def test_create_negative_long_first_name(self):
        """ Negative Test of the Contact.create() method """
        user_returned = Contact.create('S' * 22, 'Arman', 'http://day.night', '22222222',
                                       'static/images/corgey2.jpeg',
                                       'England', 'London', 'Londonskaya')
        self.assertIsNone(user_returned)

    def test_to_dict(self):
        """ Test of the Contact.create() method """
        user_returned = Contact.objects.get(id=111)
        photo = Contact.objects.get(id=111).photo
        user_to_expect = {'id': 111,
                          'first_name': 'fname',
                          'last_name': 'lname',
                          'contact_url': 'http://day.night',
                          'phone_number': '1234567',
                          'photo': photo,
                          'country': 'Ukraine',
                          'city': 'Kyiv',
                          'street': 'Mira'}
        self.assertEqual(user_returned.to_dict(), user_to_expect)

    def test_update_full(self):
        """ Test of the Contact.create(args) method """
        user_to_update = Contact.objects.get(id=4)
        user_to_update.update('Sergey', 'Arman', 'http://day.night', '22222222',
                              'static/images/corgey2.jpeg',
                              'England', 'London', 'Londonskaya')
        user_to_expect = Contact(id=4,
                                 first_name='Sergey',
                                 last_name='Arman',
                                 contact_url='http://day.night',
                                 phone_number='22222222',
                                 photo='static/images/corgey2.jpg',
                                 country='England',
                                 city='London',
                                 street='Londonskaya')
        self.assertEqual(user_to_update, user_to_expect)

    def test_update_first_name_and_url(self):
        """ Test of the Contact.create(args) method """
        user_to_update = Contact.objects.get(id=4)
        user_to_expect = Contact(id=4,
                                 first_name='John',
                                 last_name='Night',
                                 contact_url='http://day.com',
                                 phone_number='22222222',
                                 photo='static/images/corgey2.jpg',
                                 country='England',
                                 city='London',
                                 street='Londonskaya')
        user_to_update.update(first_name='John', contact_url='http://day.com')
        user_to_update = Contact.objects.get(id=4)
        self.assertEqual(user_to_update, user_to_expect)

    def test_get_all_contacts(self):
        """ Test of the Contact.get_all() method """
        expected_value = Contact.objects.all()
        current_value = Contact.get_all()
        self.assertListEqual(list(current_value), list(expected_value))
