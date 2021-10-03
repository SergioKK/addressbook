from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.utils import DataError
from django.db import models


class Contact(models.Model):
    first_name = models.CharField(blank=False, max_length=20)
    last_name = models.CharField(blank=False, max_length=20)
    contact_url = models.URLField(max_length=200, validators=[URLValidator])
    phone_number = models.CharField(max_length=63, db_index=True)
    photo = models.ImageField(null=True, blank=True)
    country = models.CharField(blank=True, max_length=50)
    city = models.CharField(blank=True, max_length=40)
    street = models.CharField(blank=True, max_length=50)

    def __str__(self):
        """
        Magic method is redefined to show all information about CustomUser.
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user password, user updated_at, user created_at,
                 user role, user is_active
        """
        return str(self.to_dict())[1:-1]

    def __repr__(self):
        """
        This magic method is redefined to show class and id of CustomUser object.
        :return: class, id
        """
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        """
        :return: user id, user first_name, user last_name, user contact_url, phone_number, user photo
        :Example:
        | {
        |   'id': 8,
        |   'first_name': 'fn',
        |   'middle_name': 'mn',
        |   'contact_url': 'http://ln.com',
        |   'phone_number': 1509393504,
        |   'photo': '<ImageFieldFile: static/images/corgey2.jpeg>'
        |   'country': 'AAA',
        |   'city': 'Kyiv',
        |   'street': 'Shabska',
        | }
        """

        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'contact_url': self.contact_url,
            'phone_number': self.phone_number,
            'photo': self.photo,
            'country': self.country,
            'city': self.city,
            'street': self.street
        }

    @staticmethod
    def create(first_name, last_name, contact_url, phone_number, photo, country, city, street):
        """
        :param photo: photo of a user
        :type photo: file
        :param phone_number: phone number og a user
        :type phone_number: str
        :param first_name: first name of a user
        :type first_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param contact_url: url of a user
        :type contact_url: str
        :param country:
        :type country: str
        :param city:
        :type city: str
        :param street:
        :type street: str
        :return: a new user object which is also written into the DB
        """
        data = {}
        data['first_name'] = first_name if first_name else ''
        data['last_name'] = last_name if last_name else ''
        data['contact_url'] = contact_url
        data['phone_number'] = phone_number
        data['photo'] = photo
        data['country'] = country
        data['city'] = city
        data['street'] = street
        user = Contact(**data)
        try:
            URLValidator(user.contact_url)
            user.save()
            return user
        except (ValidationError, DataError, AssertionError):
            pass

    def update(self,
               first_name=None,
               last_name=None,
               contact_url=None,
               phone_number=None,
               photo=None,
               country=None,
               city=None,
               street=None):
        """
        Updates user profile in the database with the specified parameters.\n
        :param first_name: first name of a user
        :type first_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param photo: photo of a user
        :type photo: file
        :param phone_number: phone number og a user
        :type phone_number: str
        :param contact_url: email of a user
        :type contact_url: str
        :param country:
        :type country: str
        :param city:
        :type city: str
        :param street:
        :type street: str
        :return: None
        """

        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if contact_url:
            self.url = contact_url
        if phone_number:
            self.phone_number = phone_number
        if photo:
            self.photo = photo
        if country:
            self.country = country
        if city:
            self.city = city
        if street:
            self.street = street
        self.save()

    @staticmethod
    def delete_by_id(contact_id):
        """
        :param contact_id: an id of a contact to be deleted
        :type contact_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """

        try:
            user = Contact.objects.get(id=contact_id)
            user.delete()
            return True
        except Contact.DoesNotExist:
            pass
        return False

    @staticmethod
    def get_by_id(contact_id):
        """
        :param author_id: SERIAL: the id of a Author to be found in the DB
        :return: author object or None if a user with such ID does not exist
        """
        try:
            user = Contact.objects.get(id=contact_id)
            return user
        except Contact.DoesNotExist:
            pass

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all users
        """
        all_users = Contact.objects.all()
        return all_users
