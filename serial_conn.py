import serial


class SerialConnection:
    def __init__(
        self, port: str, baudrate: int, bytesize: int, parity: str, stopbits: int
    ):
        if parity == "n":
            parity = serial.PARITY_NONE
        if parity == "e":
            parity = serial.PARITY_EVEN
        if parity == "o":
            parity = serial.PARITY_ODD

        if bytesize == 7:
            bytesize = serial.SEVENBITS
        if bytesize == 8:
            bytesize = serial.EIGHTBITS

        if stopbits == 1:
            stopbits = serial.STOPBITS_ONE
        if stopbits == 2:
            stopbits = serial.STOPBITS_TWO

        self.conn = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
        )

    def write(self, data: bytes):
        self.conn.write(data)
