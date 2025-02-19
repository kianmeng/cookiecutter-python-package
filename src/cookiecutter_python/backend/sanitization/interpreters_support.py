import typing as t

from .input_sanitization import Sanitize

InterpretersSequence = t.Sequence[str]


# TODO Improvement: use an Enum

SUPPORTED = {
    '3.5',
    '3.6',
    '3.7',
    '3.8',
    '3.9',
    '3.10',
    '3.11',
}


@Sanitize.register_sanitizer('interpreters')
def verify_input_interpreters(interpreters: InterpretersSequence) -> None:
    user_interpreters_set = set(interpreters)
    if len(user_interpreters_set) != len(interpreters):
        raise InvalidInterpretersError("Found duplicate interpreters!")

    if not user_interpreters_set.issubset(SUPPORTED):
        # not all user requested interpreters are included in the supported ones
        raise InvalidInterpretersError(
            "Unsupported interpreter given Error!\n"
            + "Given interpreters: [{given}]\n".format(given=', '.join(interpreters))
            + "Supported interpreters: [{supported}]\n".format(supported=', '.join(SUPPORTED))
            + "Unsupported interpreters: [{unsupported}]".format(
                unsupported=', '.join(iter(unsupported_interpreters(interpreters)))
            )
        )


def unsupported_interpreters(interpreters: InterpretersSequence) -> t.Iterator[str]:
    for interpreter in interpreters:
        if interpreter not in SUPPORTED:
            yield interpreter


@Sanitize.register_exception('interpreters')
class InvalidInterpretersError(Exception):
    pass
