import pytest

from asm1_influent_generator.skeleton import app


def test_main(capsys):
    """Test the main function"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    with pytest.raises(SystemExit):
        app(['10'])
    captured = capsys.readouterr()
    assert 'I created 10 samples for you! I saved them into your working directory.' in captured.out
