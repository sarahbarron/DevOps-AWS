import unittest
from aws.s3.create_bucket import check_bucket_name_regex
class TestS3BucketRegex(unittest.TestCase):

    def test_valid_regex_for_an_s3bucket_name(self):
        response = check_bucket_name_regex('abc-1.23')
        self.assertTrue(response, 
        'This is valid regex for an S3 Bucket the response should be True')
    
    def test_invalid_regex_for_an_s3bucket_name(self):
        response = check_bucket_name_regex('abc£$')
        self.assertFalse(response, 
        'This bucket name has invalid characters so should return False')
    
    def test_ip_address_does_not_pass(self):
        respsonse = check_bucket_name_regex('123.12.42.255')
        self.assertFalse(respsonse,
        'Bucket names can not be in the format of an IP address this should return false')

    def test_valid_bucket_name_characters_but_where_bucket_name_does_not_start_with_a_lowercase_letter_or_number(self):
        response = check_bucket_name_regex('-abc123')
        self.assertFalse(response,
        'Bucket names can only start with a lowercase letter or number and should return false')
    
    def test_valid_bucket_name_characters_but_where_bucket_name_does_not_end_with_a_lowercase_letter_or_number(self):
        response = check_bucket_name_regex('abc123-')
        self.assertFalse(response,
        'Bucket names can only end with a lowercase letter or number and should return false')
    
    def test_bucket_name_with_captial_letters(self):
        response = check_bucket_name_regex('Abc123')
        self.assertFalse(response,
        'Bucket names can not contain capital letters and should return false')
    
    def test_bucket_name_with_valid_characters_dot_and_dash_next_to_each_other(self):
        response = check_bucket_name_regex('abc-.123')
        self.assertFalse(response,
        'Bucket names can contain . and - characters but on beside each other so should return false')
    
    def test_bucket_name_with_underscore(self):
        response = check_bucket_name_regex('abc_123')
        self.assertFalse(response,
        'Bucket Names can not contain underscores so should return false')
    
    def test_bucket_names_that_are_less_than_three_characters(self):
        response = check_bucket_name_regex('ab')
        self.assertFalse(response,
        'Bucket names must be between 3 and 63 characters long')
    
    def test_bucket_names_that_are_longer_than_63_characters(self):
        response = check_bucket_name_regex('abcdefghijklmnopqrstuvwxyzab\
            cdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')
        self.assertFalse(response,
        'Bucket names must be between 3 and 63 characters long')
