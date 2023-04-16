
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
