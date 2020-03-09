import pytest

from query_builder import exceptions
from query_builder.app.utils.RangeFilterUtil import RangeFilterUtil

@pytest.mark.parametrize("arg_name,arg_value,expected",
                         [("revenue", "10000-100000", { "lte": 100000, "gte": 10000 }),
                          ("revenue", "0-100000", { "lte": 100000, "gte": 0 }),
                          ("revenue", "0-0", { "lte": 0, "gte": 0 })])
def test_parse_arg(arg_name, arg_value, expected):
    # Arrange
    util = RangeFilterUtil()

    # Act
    parsed_arg = util.parse_arg(arg_name, arg_value)

    # Assert
    assert(parsed_arg == expected)

@pytest.mark.parametrize("arg_name,arg_value",
                         [("revenue", "1"),
                          ("revenue", "abc"),
                          ("revenue", "1000-1"),
                          ("revenue", "abc-abc"),
                          ("revenue", "10-abc"),
                          ("revenue", "abc-10")])
def test_parse_arg_raises(arg_name, arg_value):
    # Arrange
    util = RangeFilterUtil()

    # Act
    with pytest.raises(exceptions.ParameterValueError):
        util.parse_arg(arg_name, arg_value)
