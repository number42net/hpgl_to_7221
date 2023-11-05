import logging
import argparse

from converter import Converter
from serial_conn import SerialConnection

logger = logging.getLogger()
conv = Converter()


def arguments():
    parser = argparse.ArgumentParser(prog="hpgl27221", description="Convert HPGL language to HP 7221 languange")
    parser.add_argument("filename")
    parser.add_argument('--serial')
    parser.add_argument('--baud')
    parser.add_argument('--bytesize', choices=[7,8], help="Bytesize")
    parser.add_argument('--parity', choices=["n", "e", "o"])
    parser.add_argument('--stopbits', choices=[1,2])
    args = parser.parse_args()

    print(args)

    if args.serial and (not args.baud or not args.bytesize or not args.parity or not args.stopbits):
        print("If a serial port is specified, the following arguments are mandatory: baud, bytesize, parity, stopbits")
        exit()
    return args


def main(file_name, serial_conn):
    with open(file_name, "r", encoding="utf-8") as file:
        source = file.readlines()

    linenumber = 0
    for line in source:
        linenumber += 1
        # Clean up
        line = line.strip(" \n\l;")

        if ";" in line:
            logger.error(f"Encountered line with multiple commands on line: {linenumber}, I can't handle that yet!")

        if not line:
            continue

        command = line[0:2]
        arguments = line[2:]
        method = getattr(conv, command, None)

        if method:
            try:
                result = method(arguments)
                if serial_conn:
                    serial_conn.write(result)
                else:
                    print(result)
            except Exception as exc:
                logger.error(f"Failed to parse line {linenumber}: {exc}")
        else:
            logger.error(f"Failed to parse line {linenumber}: Unknown command: {command}")


if __name__ == "__main__":
    args = arguments()
    if args.serial:
        serial = SerialConnection(args.serial, args.baud, args.bytesize, args.parity, args.stopbits)
    else:
        serial = None

    main(args.filename, serial)
