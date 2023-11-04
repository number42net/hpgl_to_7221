esc = bytes.fromhex("1b")


class Converter:
    def IN(self, args):
        return esc + ".(".encode("ASCII")

    def IP(self, args):
        raise NotImplementedError("No clue how to scale yet, ignoring...")

    def SP(self, args):
        if not args.isnumeric():
            raise TypeError("Expect an integer as pen number")
        if int(args) > 63:
            raise AttributeError("Expected an integer below 64")

        args = int(args)

        return b"v" + self._covert_to_sbn(args).to_bytes()

    def _covert_to_sbn(self, number: int) -> int:
        return number | 64
