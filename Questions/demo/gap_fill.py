from QUENLIG.questions import *
from QUENLIG.gap_fill import add_gap_fill

add_gap_fill(
    name="gap",
    required=(),
    question="""Fill-in the gaps in the following program (try answering 'iostream' to get feedback):""",
    template_file="gap-hello.c",
    highlight=False,
)

add_gap_fill(
    name="gap-highlight",
    required=(),
    question="""Fill-in the gaps in the following program:""",
    template_file="gap-hello.c",
    highlight=True,
    feedback=True,  # Give feedback like "XXX should appear in the answer"
)

add_gap_fill(
    name="gap-template",
    required=(),
    question="""Fill-in the gaps in the following text:""",
    template="""This is the template text, containing <i>gaps</i> to fill-in. Here, answer "one": {{{one}}}. Here, answer "two" {{{two}}}. Notice that <b>HTML</b> is allowed as long as <tt>highlight=False</tt> is used.""",
    highlight=False,
)
