import unittest
from aws.ec2.keypair import check_keypair_regex
from aws.ec2.keypair import check_input_is_in_keypair_list
from aws.ec2.keypair import get_key_name

class TestKeyPairRegex(unittest.TestCase):
    
    def test_regex_with_invalid_character_in_keypair_name(self):
        response = check_keypair_regex('abc&123')
        self.assertFalse(response,
         'abc%123 should not have passed as it has an invalid character &')
       
    def test_regex_with_over_255_characters_in_keypair_name(self):
        over_255_chars = ('abcdefghijklmnopqrstuvwzxyzabcdefghi\
            jklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvw\
            xyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijkl\
            mnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzab\
            cdefghijklmnopqrstuvwxyzcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstu\
            vwxyzabcde')
        response = check_keypair_regex(over_255_chars)    
        self.assertFalse(response, 
            'This should not have passed the regex rules as it exceeds 255 characters')
    
    def test_regex_with_zero_characters_keypair_name(self):
        zero_characters =('')
        response = check_keypair_regex(zero_characters)
        self.assertFalse(response,
        'This should not have passed as it contains zero characters keypairs must have at least 1 character')
    
    def test_regex_with_valid_keypair_name(self):
        response = check_keypair_regex('ab12_AU12-Pb')
        self.assertTrue(response, 
        'This should have passed as it contains all valid characters')

    def test_regex_with_pem_extension(self):
        response = check_keypair_regex('ab12_AU12-Pb.pem')
        self.assertTrue(response, 
        'This should have passed as it contains all valid characters')
  

class TestCheckInputIsInKeypairList(unittest.TestCase):

    def test_entering_a_keypair_that_is_in_the_list_of_keypairs(self):
        response = check_input_is_in_keypair_list('sarah_barron_key_pair')
        self.assertEqual(response, 
        'sarah_barron_key_pair', 'This is a duplicate keypair so should return the string')


    def test_entering_keypair_that_is_not_in_the_keypair_list(self):
        response = check_input_is_in_keypair_list('abcdefg')
        self.assertEqual(response, 'DOES NOT EXIST!', 
        'This should return the string DOES NOT EXIST')

class TestGetKeyName(unittest.TestCase):

    def test_entering_a_keyname_with_pem_extension(self):
        response = get_key_name('keyname.pem')
        self.assertEqual(response, 'keyname', 
        'This test should return the keyname with the .pem extension removed')
    
    def test_entering_a_keyname_with_no_pem_extension(self):
        response = get_key_name('keyname')
        self.assertEqual(response, 'keyname',
        'This should return only the keyname')