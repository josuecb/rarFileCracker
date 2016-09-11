from RarCrackFile import *

if __name__ == '__main__':
    rar = RarCrackFile('crackMeTest.rar', 10, 'dictionary.txt')
    # rar.create_threads()
    rar.start()
    # dic = DictionaryGen(4)
    # dic.write_file()
