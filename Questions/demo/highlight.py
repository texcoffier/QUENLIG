from QUENLIG.questions import *
from QUENLIG.highlight_source import highlight_file

add(
    name="highlight",
    required=(),
    # highlight_file() will read the file, auto-detect the language,
    # and apply syntax-highlighting (this requires the pigments
    # library, the function falls-back to a plain <pre>...</pre> if
    # pygments can't be loaded):
    question=(
        """Consider this program:""" + highlight_file("hello.c") +
        """What is displayed on the standard output?"""
    ),
    tests=(
        Good(Equal("hello")),
    )
)
