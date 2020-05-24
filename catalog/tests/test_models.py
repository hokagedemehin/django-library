from django.test import TestCase
from catalog.models import Author

# Create your tests here

# class YourTestClass(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         print('setUptestData: Run once to set up non-modified data for all class methods.')
#         pass

#     def setUp(self):
#         print("setUp: Run once for every test method to setup clean data")
#         pass

#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#         self.assertFalse(False)

#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         self.assertTrue(False)

#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name = 'Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label,'first name')
    # We can't get the verbose_name directly using author.first_name.verbose_name, because author.first_name is a string (not a handle to the first_name object that we can use to access its properties). Instead we need to use the author's _meta attribute to get an instance of the field and use that to query for the additional information.

    def test_date_of_death_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'Died')
    # We chose to use assertEquals(field_label,'first name') rather than assertTrue(field_label == 'first name'). The reason for this is that if the test fails the output for the former tells you what the label actually was, which makes debugging the problem just a little easier.
    
    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f"{author.last_name}, {author.first_name}"
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')

    # python manage.py test catalog.tests
    # python manage.py test catalog.tests --verbosity 2