class NoPostDefinition(Exception):
    builtin_msg = f"""\n
No post definition found!

{"_" * 10}TOP_OF_FILE{"_" * 10}
```
Publish = Bool
Date = 0000-00-00 00:00:00 +0100 or set-on-compile
Title = String
Description = String
```

Must be at the top of the file, and must be followed by a blank line.

"""

    def __str__(self):
        return self.builtin_msg


class ErrorInPostDefinition(Exception):
    builtin_msg = f"""\n
There is an error in the post description!

{"_" * 10}TOP_OF_FILE{"_" * 10}
```
Publish = Bool
Date = 0000-00-00 00:00:00 +0100 or set-on-compile
Title = String
Description = String
```

Must be at the top of the file, and must be followed by a blank line.

"""

    def __str__(self):
        return self.builtin_msg
