from ticker import valid_ticker


def test_valid_ticker():
    assert valid_ticker("ABCD") is True


def test_ticker_not_string():
    assert valid_ticker(1) is False


def test_empty_string():
    assert valid_ticker("") is False


def test_ticker_too_long():
    assert valid_ticker("ABCDEG") is False


def test_special_character():
    assert valid_ticker("A1BC2") is False
