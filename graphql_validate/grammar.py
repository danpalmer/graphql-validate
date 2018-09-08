"""
Check grammar use in documentation.

Currently these checks are _very_ basic, but we should aim to expand them over
time.
"""


def check_grammar(text: str) -> [str]:
    """Return a list of human-readable issues with the given text."""
    if not text:
        yield "Empty documentation"
        return

    if text.strip() != text:
        yield "Documentation has leading/trailing whitespace."

    text = text.strip()

    if text[0] != text[0].upper():
        yield "Sentences should start with a capital letter."

    if text[-1] != ".":
        yield "Sentences should end with a full stop."
