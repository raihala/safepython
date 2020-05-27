import argparse
import os
import shutil
import sys
import traceback


def comment_line(filename, lineno):
    with open(filename, 'r') as f_in:
        lines = f_in.readlines()
    with open(f"{filename}+", 'w') as f_out:
        for line in lines[:lineno-1]:
            f_out.write(line)
        f_out.write(f"# {lines[lineno-1]}")
        for line in lines[lineno:]:
            f_out.write(line)

    os.replace(f"{filename}+", filename)


def execfile(filename, globals=None, locals=None):
    # see https://stackoverflow.com/a/41658338
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filename,
        "__name__": "__main__",
    })
    with open(filename, 'rb') as file:
        exec(compile(file.read(), filename, 'exec'), globals, locals)


def wrap(filename, lines_commented=0):
    try:
        execfile(filename)
    except:
        tb = sys.exc_info()[2]
        stack = traceback.extract_tb(tb)
        frame = stack[2]  # gotta get the right stack frame

        offending_filename = frame.filename
        offending_lineno = frame.lineno
        print(f"Error occurred in file {offending_filename} at line {offending_lineno}. Commenting out offending line")

        # comment out the offending line and try again
        comment_line(offending_filename, offending_lineno)
        wrap(filename, lines_commented+1)
    else:
        print(f"Executed {filename} successfully after commenting out {lines_commented} lines!")


def main(argv=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Python file to wrap')
    args = parser.parse_args(argv[1:])

    # <<;;;
    shutil.copy2(args.filename, f"{args.filename}.bak")

    wrap(args.filename)


if __name__ == "__main__":
    sys.exit(main(sys.argv))