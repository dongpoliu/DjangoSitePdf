"""
exceptions classes
"""


class Error(Exception):
    """
    Creating user which already exist.
    """

    def __init__(self, *args, **kwargs):
        super(Error, self).__init__(*args, **kwargs)
