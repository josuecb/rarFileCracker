from threading import Thread

import time
from unrar import rarfile


class RarCrackFile:
    minThreadCounts = 0
    threadIndexList = []
    dictionaryFile = ""
    dictionarySize = 0
    threadsAllowed = False
    rarFile = ""
    passwords = []
    passwordChecks = 0
    startTime = time.time()
    currentTime = startTime
    previousTime = currentTime

    def __init__(self, rar_file_name, t_counts=0, dictionary_file="dictionary.txt"):
        print t_counts
        self.minThreadCounts = t_counts
        self.dictionaryFile = dictionary_file
        self.passwords = self.get_file_words()
        self.generate_index_list()
        self.rarFile = rar_file_name

    # setters
    def get_file_words(self):
        dic_file = open(self.dictionaryFile, 'r').read()
        dic_file = dic_file.split("\n")
        self.dictionarySize = len(dic_file)
        return dic_file

    def generate_index_list(self):
        thread_unit_size = self.dictionarySize / self.minThreadCounts
        self.get_indexes(0, thread_unit_size)

        # changes the size of threading just in case
        self.minThreadCounts = len(self.threadIndexList)
        # changing the left size i.e(max_size = 100 and last point is 98 then last point is changed to 100)
        temp = self.threadIndexList[self.minThreadCounts - 1]
        self.threadIndexList[self.minThreadCounts - 1] = (temp[0], self.dictionarySize)

    def get_indexes(self, previous_index, next_index):
        if previous_index > self.dictionarySize:
            return

        self.threadIndexList += [(previous_index, previous_index + next_index)]
        self.get_indexes(previous_index + next_index, next_index)

    # End of Setters
    def create_threads(self):
        self.threadsAllowed = True

    # Useful methods ###################################################################
    def crack_it(self, thread_index):
        # print len(self.threadIndexList)
        # print str(self.threadIndexList)
        start_index = self.threadIndexList[thread_index][0]
        end_index = self.threadIndexList[thread_index][1]

        while start_index != end_index:
            self.print_message_every(4)
            # print "Thread " + str(thread_index)
            password = self.passwords[start_index]
            self.un_rar(password)
            start_index += 1
            self.passwordChecks += 1

    def un_rar(self, password):
        try:
            rar = rarfile.RarFile(self.rarFile, 'r', pwd=password)
            if len(rar.namelist()) > 0:
                print "password found: " + password
                print rar.testrar()
                print rar.namelist()
                password_file = open('password.txt', 'a')
                password_file.write(password + '\n')
            # in case password is bad
            password_file = open('junk_passwords.txt', 'a')
            password_file.write(password + '\n')
        except Exception, e:
            # print e.message
            pass

    # creates all threads
    def start(self):
        thread_index = 0

        threads = []
        while thread_index < self.minThreadCounts:
            threads += [Thread(target=self.crack_it, args=(thread_index,))]
            thread_index += 1

        thread_index = 0

        while thread_index < self.minThreadCounts:
            threads[thread_index].start()
            thread_index += 1

    def print_message_every(self, seconds):
        if (time.time() - self.currentTime) >= seconds:
            self.currentTime = time.time()
            print "Password tries: " + str(self.passwordChecks)
            time_elapsed = time.time() - self.startTime
            print str(self.passwordChecks / time_elapsed) + "/s in " + str(time_elapsed)
