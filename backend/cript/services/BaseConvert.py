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
