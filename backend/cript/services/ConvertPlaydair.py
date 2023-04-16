import re
from cript.services.BaseConvert import BaseConnvert


class ConvertPlayfair(BaseConnvert):

    def convert_to_playfair(message, key):

        def normalize_message(message):
            message = re.sub(
                r'[\d\s]*', r'', message.lower().replace('j', 'i'))
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
