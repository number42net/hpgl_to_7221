esc = bytes.fromhex("1b")

class Converter:
    def IN(self, args: str) -> bytes:
        # Initialize
        # Manual page 95
        return esc + ".(".encode("ASCII")

    def IP(self, args: str) -> bytes:
        # Manual pages 95, 100
        if not args:
            return b""
        
        raise NotImplementedError("No clue how to scale yet, ignoring...")

    def SP(self, args) -> bytes:
        # Select Pen
        # Manual page 94
        return b"v" + self._covert_to_sbn(args).to_bytes()

    def PU(self, args: str) -> bytes:
        # Pen Up
        # Manual page 110
        coordinates = self._combine_pairs(args.split(","))
        
        output = b"p"
        for coordinate in coordinates:
            output += self._convert_to_mbp(*coordinate)
        
        output += b"}"

        return output
    def PD(self, args: str) -> bytes:
        # Pen Down
        # Manual page 106
        coordinates = self._combine_pairs(args.split(","))
        
        output = b"q"
        for coordinate in coordinates:
            output += self._convert_to_mbp(*coordinate)
        
        output += b"}"

        return output


    def _combine_pairs(self, args: list) -> list:
        if not (len(args) % 2) == 0:
            raise AttributeError("Expected pairs of xy coordinates")

        output = []
        for i in range(0, len(args), 2):
            output.append((args[i], args[i + 1]))

        return output

    def _covert_to_sbn(self, number: int) -> int:
        # Manual page 87
        if not number.isnumeric():
            raise TypeError("Expect an integer")
        if int(number) > 63:
            raise AttributeError("Expected an integer below 64")
        
        number = int(number)

        # SBN is a 7 bit integer and the most significant bit is always a 1
        return number | 64

    def _convert_to_mbn(self, number: int) -> bytes:
        # Manual page 87
        # Ported from: https://github.com/Toranktto/bsd-plotutils/blob/master/libplot/drivers/hp7221/subr.c

        if not number.isnumeric():
            raise TypeError("Expect an integer")
        if int(number) > 32767:
            raise AttributeError("Expected an integer below 32768")
        
        number = int(number)

        output = b''

        chr = (number >> 12) & 0o7
        chr |= 0o140
        output += chr.to_bytes()
        
        chr = (number >> 6) & 0o77
        if chr < 32:
            chr += 64
        output += chr.to_bytes()
        
        chr = number & 0o77
        if chr < 32:
            chr += 64
        output += chr.to_bytes()
        
        return output

    def _convert_to_mbp(self, x: int, y: int) -> bytes:
        # Manual page 88
        # Ported from: https://github.com/Toranktto/bsd-plotutils/blob/master/libplot/drivers/hp7221/subr.c

        if not x.isnumeric() and y.x.isnumeric():
            raise TypeError("Expect an integer")
        if int(x) > 32767 and int(y) > 32767:
            raise AttributeError("Expected an integer below 32768")

        x = int(x)
        y = int(y)
        output = b""

        chr = (x >> 10) & 0o17
        chr |= 0o140
        output += chr.to_bytes()

        chr = (x >> 4) & 0o77
        if chr < 32:
            chr += 64
        output += chr.to_bytes()

        chr = (y >> 12) & 0o3
        chr |= (x << 2) & 0o71
        if chr < 32:
            chr += 64
        output += chr.to_bytes()

        chr = (y >> 6) & 0o77
        if chr < 32:
            chr += 64
        output += chr.to_bytes()

        chr = (y)&0o77
        if (chr < 32):
            chr += 64
        output += chr.to_bytes()

        return output

