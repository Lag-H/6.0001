def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    assert isinstance(sequence, str), "Passed in object is not a string."
    permutations = []
    permutaion_helper(sequence, "", permutations)

    return permutations


def permutaion_helper(sequence, chosen, permutations):
    if (len(sequence) == 0):
        # print(chosen)
        if chosen not in permutations:
            permutations.append(chosen)
    else:
        for i in range(len(sequence)):
            chosen += sequence[i]
            # print(chosen)
            sequence_iter = sequence[1:] if (i == 0) else (sequence[:i] + sequence[i + 1:])
            # print("seq_iter = " + sequence_iter)
            permutaion_helper(sequence_iter, chosen, permutations)

            sequence_iter += sequence[i]
            chosen = chosen[:-1]


if __name__ == '__main__':
    # EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))

#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a
#    sequence of length n)
#     i2 = '123'
#     print('Input 2: ', i2)
#     print("Output 2: ", get_permutations(i2))
#
#     i2 = 'qwe'
#     print('Input 3: ', i2)
#     print("Output 3: ", get_permutations(i2))
#
#     i2 = '1'
#     print('Input 4: ', i2)
#     print("Output 4: ", get_permutations(i2))
#
#     i2 = '89'
#     print('Input 5: ', i2)
#     print("Output 5: ", get_permutations(i2))
#
#     i2 = ''
#     print('Input 6: ', i2)
#     print("Output 6: ", get_permutations(i2))
#
#     i2 = [123]
#     print('Input 7: ', i2)
#     print("Output 7: ", get_permutations(i2))

