import os


def get_file_size(file):
    """take a file object and return the size of it in bytes"""
    # os.SEEK_END == 2
    # seek() return the new absolute position
    file_length = file.seek(0, os.SEEK_END)

    # also can use tell() to get current position
    # file_length = file.tell()

    # seek back to start position of stream,
    # otherwise save() will write a 0 byte file
    # os.SEEK_END == 0
    file.seek(0, os.SEEK_SET)
    return file_length