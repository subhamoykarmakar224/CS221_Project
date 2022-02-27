# Node for index of index tree
class TreeNode:
    def __init__(self, prefix, offset):
        self.prefix = prefix  # Prefix
        self.file_name = list()  # File in which the posting is present
        self.offset = offset  # Offset for seek operation
