import hashlib
import math
import re


class BaseConnvert:

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


class ConvertADFGX(BaseConnvert):

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

        return ''.join(sum(list(map(lambda x: x["tail"], mix)), []))

    def convert_from_ADFG_X(message, key, char_set='adfgx', alphabet='abcdefghiklmnopqrstuvwxyz', options={}):
        alphabet = ConvertADFGX.create_alphabet(
            key,
            alphabet=alphabet,
            options=options
        )

        _alphabet = []
        index = 0
        row = 0

        for char in alphabet:
            _alphabet.append({'char': char, 'code': char_set[row] + char_set[index]})
            index = index + 1 if index < len(char_set)-1 else 0
            row = row + 1 if index == 0 else row

        _message = [{'key': keychar, 'tail': [], 'num': index} for index, keychar in enumerate(key)]
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


class ConvertPlayfair(BaseConnvert):

    def convert_to_playfair(message, key):

        def normalize_message(message):
            message = re.sub(r'[\d\s]*', r'', message.lower().replace('j', 'i'))
            for i in range(0, len(message), 2):
                if len(message[i:i+2]) == 1:
                    break
                if message[i] == message[i+1]:
                    message = f"{message[:i+1]}x{message[i+1:]}"
            message = message + 'x' if len(message) % 2 != 0 else message
            return message

        alphabet = ConvertPlayfair.create_alphabet(
            key,
            options={'replace': ['j', 'i']}
        )
        message = normalize_message(message)
        message = [''.join(message[n:n+2]) for n in range(0, len(message), 2)]

        result = ''
        for pair in message:
            a = alphabet.index(pair[0])
            b = alphabet.index(pair[1])
            a_row, a_col = a // 5, a % 5
            b_row, b_col = b // 5, b % 5

            if a_row == b_row:
                result += alphabet[a+1] if a_col != 4 else alphabet[a-4]
                result += alphabet[b+1] if b_col != 4 else alphabet[b-4]
            elif a_col == b_col:
                result += alphabet[a+5] if a_row != 4 else alphabet[a-20]
                result += alphabet[b+5] if b_row != 4 else alphabet[b-20]
            else:
                result += f"{alphabet[a+(b_col - a_col)]}{alphabet[b+(a_col - b_col)]}"

        return result

    def convert_from_playfair(message, key):
        alphabet = ConvertPlayfair.create_alphabet(
            key,
            options={'replace': ['j', 'i']}
        )

        message = [''.join(message[n:n+2]) for n in range(0, len(message), 2)]
        print(message)
        print(alphabet)
        result = ''
        for pair in message:
            a = alphabet.index(pair[0])
            b = alphabet.index(pair[1])
            a_row, a_col = a // 5, a % 5
            b_row, b_col = b // 5, b % 5

            if a_row == b_row:
                result += alphabet[a-1] if a_col != 0 else alphabet[a+4]
                result += alphabet[b-1] if b_col != 0 else alphabet[b+4]
            elif a_col == b_col:
                result += alphabet[a-5] if a_row != 0 else alphabet[a+20]
                result += alphabet[b-5] if b_row != 0 else alphabet[b+20]
            else:
                result += f"{alphabet[a+(b_col - a_col)]}{alphabet[b+(a_col - b_col)]}"
        return result.replace('x', '')

class Salsa:
    def __init__(self,l=10):
        assert l >= 0
        self._l = l
        self._mask = 0xffffffff

    def __call__(self,key=[0]*32,nonce=[0]*8,block_counter=[0]*8):
        assert len(key) == 32
        assert len(nonce) == 8
        assert len(block_counter) == 8

        k = [self._littleendian(key[4*i:4*i+4]) for i in range(8)]
        n = [self._littleendian(nonce[4*i:4*i+4]) for i in range(2)]
        b = [self._littleendian(block_counter[4*i:4*i+4]) for i in range(2)]
        c = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]

        s = [c[0], k[0], k[1], k[2],
            k[3], c[1], n[0], n[1],
            b[0], b[1], c[2], k[4],
            k[5], k[6], k[7], c[3]]
        self._s = s[:]

        for i in range(self._l):
            self._cround()
            self._rround()

        self._s = [(self._s[i] + s[i]) & self._mask for i in range(16)]

        return self._s

    def _cround(self):
        self._qround(0, 4, 8, 12)
        self._qround(5, 9, 13, 1)
        self._qround(10, 14, 2, 6)
        self._qround(15, 3, 7, 11)

    def _rround(self):
        self._qround(0, 1, 2, 3)
        self._qround(5, 6, 7, 4)
        self._qround(10, 11, 8, 9)
        self._qround(15, 12, 13, 14)

    def _qround(self, a, b, c, d):
        self._s[b] ^= self._rotl32((self._s[a] + self._s[d]) & self._mask, 7)
        self._s[c] ^= self._rotl32((self._s[b] + self._s[a]) & self._mask, 9)
        self._s[d] ^= self._rotl32((self._s[c] + self._s[b]) & self._mask,13)
        self._s[a] ^= self._rotl32((self._s[d] + self._s[c]) & self._mask,18)

    def _rotl32(self, num, shift):
        return ( ( ( num << shift ) & self._mask) | ( num >> ( 32 - shift ) ) )

    def _littleendian(self,b):
        assert len(b) == 4
        return b[0] ^ (b[1] << 8) ^ (b[2] << 16) ^ (b[3] << 24)
