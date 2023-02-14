import math


class ConvertADFGX:

    def convert_to_ADFGX(message, key):
        return ConvertADFGX.mix(
            ConvertADFGX.encode(
                message,
                ConvertADFGX.create_alphabet(
                    key,
                    options={'replace': ['j', 'i']}
                )),
            key
        )

    def convert_to_ADFGVX(message, key):
        return ConvertADFGX.mix(
            ConvertADFGX.encode(
                message,
                ConvertADFGX.create_alphabet(
                    key,
                    alphabet="abcdefghijklmnopqrstuvwxyz0123456789"),
                char_set='adfgvx'),
            key)

    def create_alphabet(key, alphabet='abcdefghiklmnopqrstuvwxyz', options={}):

        for char in key.lower():
            alphabet = alphabet.replace(char, '')

        if 'replace' in options:
            key = key.lower().replace(
                options['replace'][0], options['replace'][1]) if options['replace'][0] in key else key
        clear_key = ''
        for char in key.lower():
            clear_key = clear_key + char if char not in clear_key else clear_key

        return clear_key + alphabet

    def encode(message, alpabet, char_set='adfgx'):
        result = ''
        char_set = list(char_set)
        alpabet = list(alpabet)

        for char in message.lower():
            if char not in alpabet:
                continue
            index = alpabet.index(char)
            result = result + char_set[math.floor(index/len(char_set))]
            index = index - math.floor(index/len(char_set)) * len(char_set)
            result = result + char_set[index]

        return result

    def mix(message, key):
        mix = [{'key': char, "tail": []} for char in key]

        index = 0
        for char in message:
            mix[index]['tail'].append(char)
            index = index + 1 if index < len(key)-1 else 0
        mix.sort(key=lambda x: x['key'])

        print(mix)
        return ''.join(sum(list(map(lambda x: x["tail"], mix)), []))

    def convert_from_ADFG_X(message, key, set='adfgx', alphabet='abcdefghiklmnopqrstuvwxyz', options = {}):
        alphabet= ConvertADFGX.create_alphabet(
            key,
            alphabet=alphabet,
            options=options
        )

        _alphabet = []
        index = 0
        row = 0

        for char in alphabet:
            _alphabet.append({'char': char, 'code': set[row] + set[index]})
            index = index + 1 if index < len(set)-1 else 0
            row = row + 1 if index == 0 else row

        _message = [ {'key': keychar, 'tail': [], 'num': index } for index, keychar in enumerate(key)]
        _message.sort(key=lambda x: x['key'])

        long_chunk_length = len(message[0:math.ceil(len(message)/len(key))])
        long_chuncks_nums = [i for i in range(len(key) - (long_chunk_length * len(key) - len(message)))]

        pos = 0
        for chunk in _message:
            if chunk['num'] not in long_chuncks_nums:
                chunk['tail'] = message[pos:pos + long_chunk_length - 1]
            else:
                chunk['tail'] = message[pos:pos + long_chunk_length]
                pos = pos + 1
            pos = pos + long_chunk_length - 1

        _message.sort(key=lambda x: x['num'])

        result = []
        for keychar in key:
            item = filter(lambda x: x['tail'] and x['key'] == keychar, _message)
        print(_message)

        index = 0
        row = 0
        result = []
        for i in range(len(message)):
            result.append(_message[index]['tail'][row])
            index = index + 1 if index < len(key)-1 else 0
            row = row + 1 if index == 0 else row
        result = [''.join(result[n:n+2]) for n in range(0, len(result), 2)]

        string = ''
        for bigram in result:
            for char in _alphabet:
                if char['code'] == bigram:
                    string = string + char['char']
                    break
        return string
