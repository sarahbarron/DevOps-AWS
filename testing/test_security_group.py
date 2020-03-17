import unittest
from aws.ec2.security_group import check_for_duplicate_security_group_name
from aws.ec2.security_group import check_regex


class TestSecurityGroupForDuplicateName(unittest.TestCase):
    def test_with_a_duplicate_security_group_name(self):
        response = check_for_duplicate_security_group_name('default')
        self.assertTrue(response, 'This is a duplicate security group name so should return True')

    def test_with_a_unique_security_group_name(self):
        response = check_for_duplicate_security_group_name('xyzabc')
        self.assertFalse(response, 'This is a unique security group name so should return False')

class TestSecurityGroupNameRegex(unittest.TestCase):

    def test_with_valid_regex_for_the_security_group_name(self):
        response = check_regex('._-:/()#,@[]+=&;{}!$* a-zA-Z0-9')
        self.assertTrue(response, 
        'This is valid regex characters for a security group name so should return true')
    
    def test_with_invalid_regex_for_the_security_group_name(self):
        response = check_regex('sg-abc')
        self.assertFalse(response, 
        'This is not valid regex characters for a security group name so should return true')
    
    def test_with_an_invalid_character_in_the_security_group_name(self):
        response = check_regex('ab"123')
        self.assertFalse(response, 
        'This name includes an invalid character " so should return false')