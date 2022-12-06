# safepython

Do you write Python code? When you execute your code, does Python throw frustrating and time-consuming errors? Try safepython! It runs your program, and if an error is thrown, it comments out the offending line and tries again (repeating as necessary).

Consider the files foo.py:
```
def foo():
    x = 0/0
    print("hello!")
```
and bar.py:
```
import foo

foo.foo()
foo.foo()
```
If you run `python bar.py`, this will throw an error, complaining about division by zero. No good! We can fix this with safepython:
```
$ ./safepython.py bar.py
Error in bar.py:3
Error in bar.py:4
Executed bar.py successfully after commenting out 2 line(s)
```
Nice! safepython commented out the offending lines until it was able to successfully execute the script. Now bar.py looks like:
```
import foo

# foo.foo()
# foo.foo()
```
But let's say you want to be more thoroughgoing, and fix the errors at the source--in foo.py, instead of bar.py. safepython lets you do that too, using the `--proactive` flag. After resetting bar.py to its original state, we run:
```
$ ./safepython.py bar.py --proactive
Error in /path/to/foo.py:2
hello!
hello!
Executed bar.py successfully after commenting out 1 line(s)
```
Now bar.py is unchanged, and foo.py looks like:
```
def foo():
#     x = 0/0
    print("hello!")
```
Now we've solved the errors by changing one line instead of two, fixed the actual problem at its root, *and* successfully executed the two print statements. Perfect!!

### Requirements

Tested with Python 3.6. And it might work with other versions too!