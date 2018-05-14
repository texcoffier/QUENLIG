from QUENLIG.questions import *
from QUENLIG.mcq import add_mcq

add_mcq(
    name="basic",
    required=(),
    question="""Please tick the right boxes:""",
    # answers is a list of tuples (<string>, <boolean>[, <string>]).
    # The first item is the text displayed next to the tickbox. The
    # boolean states whether the box should be ticked. The 3rd
    # element, if present, is a feedback given to the user in case of
    # incorrect answer.
    answers=(
        ("You should tick this one.", True),
        ("You should also tick this one.", True),
        ("This one shouldn't be ticked.", False),
    ),
    shuffle=True,  # Reorder the items randomly
    indices=("This is the first hint",
             "This is the second hint"
             )
)

add_mcq(
    name="feedback",
    required=(),
    question="""Please tick the right boxes (try ticking none or all boxes to get feedback):""",
    answers=(
        ("You should tick this one.", True, "It seems you didn't tick this answer, but you should have."),
        ("You should also tick this one.", True, "Again, you should have ticked this answer."),
        ("This one shouldn't be ticked.", False, "It seems you ticked this answer, but you shouldn't have."),
    ),
)
