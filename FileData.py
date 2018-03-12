WRITE = 'w'
READ = 'r'
READWRITE = 'r+'
APPEND = 'a'


class FileData:
    def __init__(self, file):
        self.file = file

    def append_file(self, line):
        writer = open(self.file, mode=APPEND)
        writer.write('\n' + line)

    def write_file(self, line):
        writer = open(self.file, mode=WRITE)
        writer.write('\n' + line)

    def overwrite_file(self, line):
        writer = open(self.file, mode=READWRITE)
        writer.write('\n' + line)

    def read_file(self):
        reader = open(self.file, mode=READ)
        data = reader.read()
        return data

    def list_file_lines(self):
        reader = open(self.file, mode=READ)
        data = reader.readlines()
        return data
