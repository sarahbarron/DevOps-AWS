import unittest
from aws.ec2.keypair import check_keypair_regex
from aws.ec2.keypair import create_new_key_pair
from aws.ec2.keypair import check_input_is_in_keypair_list


class TestKeyPairRegex(unittest.TestCase):
    
    def test_regex_with_invalid_character_in_keypair_name(self):
        invalid_regex = check_keypair_regex('abc&123')
        
        self.assertEqual(invalid_regex, True,
         'abc%123 should not have passed as it has an invalid character &')
       
    def test_regex_with_over_255_characters_in_keypair_name(self):

        over_255_chars = ('abcdefghijklmnopqrstuvwzxyzabcdefghi\
            jklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvw\
            xyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijkl\
            mnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzab\
            cdefghijklmnopqrstuvwxyzcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstu\
            vwxyzabcde')
        invalid_regex_over_255_chars = check_keypair_regex(over_255_chars)    
        self.assertEqual(invalid_regex_over_255_chars, True, 
            'This should not have passed the regex rules as it exceeds 255 characters')
    
    def test_regex_with_zero_characters_keypair_name(self):

        zero_characters =('')
        invalid_regex_zero_characters = check_keypair_regex(zero_characters)
        self.assertEqual(invalid_regex_zero_characters, True,
        'This should not have passed as it contains zero characters keypairs must have at least 1 character')
    def test_regex_with_valid_keypair_name(self):
        correct_regex = check_keypair_regex('ab12_AU12-Pb')
        self.assertEqual(correct_regex, False, 
        'This should have passed as it contains all valid characters')

    def test_regex_with_pem_extension(self):
        correct_regex = check_keypair_regex('ab12_AU12-Pb.pem')
        self.assertEqual(correct_regex, False, 
        'This should have passed as it contains all valid characters')


    

class TestCreateNewKeypair(unittest.TestCase):

    def test_duplicate_keypair_name_returns_none(self):
        keypair_name = create_new_key_pair('sarah_barron_key_pair')
        self.assertIsNone(keypair_name, 'This should return none as it is duplicate')
    

class TestCheckInputIsInKeypairList(unittest.TestCase):

    def test_entering_a_keypair_that_is_in_the_list_of_keypairs(self):
        response = check_input_is_in_keypair_list('sarah_barron_key_pair')
        self.assertEqual(response, 'sarah_barron_key_pair', 'This is a duplicate keypair so should return the string')


    def test_entering_keypair_that_is_not_in_the_keypair_list(self):
        response = check_input_is_in_keypair_list('abcdefg')
        self.assertEqual(response, 'DOES NOT EXIST!', 'This should return the string DOES NOT EXIST')