from converter import Converter
import logging
import argparse

logger = logging.getLogger()
conv = Converter()


def arguments():
    parser = argparse.ArgumentParser(prog="hpgl27221", description="Convert HPGL language to HP 7221 languange")
    parser.add_argument("filename", help="The name or path of a file containing HPGL commands")
    return parser.parse_args()


def main(file_name):
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
                print(result)
            except Exception as exc:
                logger.error(f"Failed to parse line {linenumber}: {exc}")
        else:
            logger.error(f"Failed to parse line {linenumber}: Unknown command: {command}")


if __name__ == "__main__":
    args = arguments()
    main(args.filename)
