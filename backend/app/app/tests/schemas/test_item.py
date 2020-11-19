import pytest
from app.schemas.item import validate_date


@pytest.mark.parametrize("date, iso_expected", [
    ("01.11.2020", "2020-11-01"),
    ("1.11.2020", "2020-11-01"),
    ("5.1.2020", "2020-01-05"),
    ("01.1.2020", "2020-01-01"),
])
def test_validate_date_returns_str(date, iso_expected):
    iso = validate_date(date)
    assert iso == iso_expected


def test_validate_date_raises_exception_if_wrong_date_format():
    with pytest.raises(ValueError):
        validate_date("05.12.20")


def test_validate_date_raises_exception_if_wrong_type():
    with pytest.raises(ValueError):
        validate_date(None)
