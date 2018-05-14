from QUENLIG.questions import Contain, Comment, Good, Bad, add


def add_mcq(question, answers, shuffle=False, **kwargs):
    """Convenience wrapper around add() to add a multiple-choice question.

    ``question`` is the text of the question.

    ``answers`` is a list of options, each option being a tuple:
    - Text describing the option,
    - True/False to say whether this option should be ticked (True) or
      not (False),
    - Optionaly, a comment.

    ``shuffle`` is a Boolean saying whether answers should be shuffled.

    Other arguments are forwarded to ``add``.

    Example:

    add_mcq(
        question="Tick the right answers:",
        answers=(
            ("Tick this one", True),
            ("Don't tick this one", False),
            ("Don't tick this one either", False, "Hey, I told you not to tick ..."),
        )
    )

    """
    tests = []
    i = 0
    for a in answers:
        i += 1
        ans = "A" + str(i)
        if a[1]:
            this_test = ~ Contain(ans)
            before = "<i>"
            after = "</i>"
        else:
            this_test = Contain(ans)
            before = "<strike><i>"
            after = "</i></strike>"
        if len(a) > 2:
            this_test = Comment(this_test, before + a[0] + after +
                                "<br />" + a[2] + "<br />")
        question += "{{{" + ans + "}}}" + a[0] + "\n"
        tests.append(Bad(this_test))
    tests.append(Good())  # Always True: accept question if no Bad() rejected it.
    if shuffle:
        question += "{{{ shuffle}}}"
    add(question=question, tests=tests, function_name='add_mcq', **kwargs)
