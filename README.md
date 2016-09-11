# rarFileCracker

##About
This is a python tool which lets you bruteforce a rar file that has passwords, you only need to have a dictionary file e.i("dictionary.txt") that can be used by this program.
- Terminal Only
- Threads support (faster tries)
- Depends on your RAM, try to not put more than 20 threads per run.

##Libraries required:
- [unrar v0.3](https://pypi.python.org/pypi/unrar/0.3).

**NOTE:** you must install the libraries mentioned above.

# Demo

`# testing to start program just call start method rar = RarCrackFile('crackMeTest.rar', 10, 'dictionary.txt') rar.start() `
