import argparse
import os
import shutil
import sys
import traceback


def reset_sys_modules(original_sys_modules):
    added_modules = []
    altered_modules = []
    for key, value in sys.modules.items():
        if key not in original_sys_modules:
            added_modules.append(key)
        elif value is not original_sys_modules[key]:
            altered_modules.append(key)

    for key in added_modules:
        del sys.modules[key]
    for key in altered_modules:
        raise NotImplementedError("Don't know how to handle altered modules yet")


def comment_line(filename, lineno):
    backup_filename = f"{filename}.bak"
    if not os.path.isfile(backup_filename):
        shutil.copy2(filename, backup_filename)

    with open(filename, 'r') as f_in:
        lines = f_in.readlines()

    tmp_filename = f"{filename}+"
    with open(tmp_filename, 'w') as f_out:
        f_out.writelines(lines[:lineno-1])
        f_out.write(f"# {lines[lineno-1]}")
        f_out.writelines(lines[lineno:])

    os.replace(tmp_filename, filename)


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


def wrap(filename, proactive=False, lines_commented=0):
    original_sys_modules = dict(sys.modules)  # will reset after exec
    try:
        execfile(filename)
    except:
        tb = sys.exc_info()[2]
        stack = traceback.extract_tb(tb)

        # frame 0 is execfile() call, frame 1 is exec() call,
        # frame 2 is source of error in the wrapped file, and
        # the last frame (-1) is the ultimate source of the error
        if proactive:
            frame = stack[-1]
        else:
            frame = stack[2]

        offending_filename = frame.filename
        offending_lineno = frame.lineno

        print(f"Error in {offending_filename}:{offending_lineno}")

        # comment out the offending line, reset the
        # loaded modules, and try again
        comment_line(offending_filename, offending_lineno)
        reset_sys_modules(original_sys_modules)
        wrap(filename, proactive, lines_commented+1)
    else:
        print(f"Executed {filename} successfully after commenting out {lines_commented} line(s)")


def main(argv=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Python file to wrap')
    parser.add_argument(
        '--proactive', action='store_true',
        help='Doggedly pursue exceptions to their ultimate source, and fix them there'
    )
    args = parser.parse_args(argv[1:])

    sys.argv[0] = args.filename
    wrap(args.filename, proactive=args.proactive)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
