# Problem Set 4C
# Name: Lag-H
# Collaborators:
# Time Spent: x:xx

import itertools
import random
import string


### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    #>>> is_word(word_list, 'bat') returns
    True
    #>>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        transpose_dict = {}

        # for lower_vowel, permuted_vowel in VOWELS_LOWER, vowels_permutation:
        #     transpose_dict[lower_vowel] = permuted_vowel
        #     transpose_dict[lower_vowel.upper()] = permuted_vowel.uppper()

        for lower_vowel, upper_vowel, permuted_vowel in zip(VOWELS_LOWER, VOWELS_UPPER, vowels_permutation):
            transpose_dict[lower_vowel] = permuted_vowel
            transpose_dict[upper_vowel] = permuted_vowel.upper()

        for element in CONSONANTS_LOWER:
            transpose_dict[element] = element
        for element in CONSONANTS_UPPER:
            transpose_dict[element] = element
        return transpose_dict

    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        encrypted_message = ""
        for letter in self.message_text:
            if letter in string.ascii_letters:
                encrypted_message += transpose_dict[letter]
            else:
                encrypted_message += letter
        return encrypted_message
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        max_correct_words = 0
        decrypted_message = []
        permutation_set = itertools.permutations(VOWELS_LOWER)
        for chosen_permutation in permutation_set:
            temp_decrypted_message = ""
            word_count = 0
            transpose_dict = self.build_transpose_dict(chosen_permutation)
            reverse_transpose_dict = {}
            for vowel in VOWELS_LOWER:
                reverse_transpose_dict[transpose_dict[vowel]] = vowel
            for vowel in VOWELS_UPPER:
                reverse_transpose_dict[transpose_dict[vowel]] = vowel
            for element in CONSONANTS_LOWER:
                reverse_transpose_dict[element] = element
            for element in CONSONANTS_UPPER:
                reverse_transpose_dict[element] = element

            temp_decrypted_message = self.apply_transpose(reverse_transpose_dict)
            words = temp_decrypted_message.split()
            for word in words:
                if is_word(self.valid_words, word):
                    word_count += 1

            if word_count > max_correct_words:
                max_correct_words = word_count
                del decrypted_message[:]
                decrypted_message.append(temp_decrypted_message)
            elif word_count == max_correct_words:
                    decrypted_message.append(temp_decrypted_message)
        if max_correct_words > 1:
            return random.choice(decrypted_message)
        else:
            return self.get_message_text()


if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
    #TODO: WRITE YOUR TEST CASES HERE
