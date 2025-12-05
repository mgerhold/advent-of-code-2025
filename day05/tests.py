import pytest
from main import Range, RangeContainer


@pytest.mark.parametrize(
    "start,new_range,expected",
    [
        (
            RangeContainer(),
            Range(5, 10),
            RangeContainer(Range(5, 10)),
        ),
        (
            RangeContainer(Range(5, 10)),
            Range(6, 8),
            RangeContainer(Range(5, 10)),
        ),
        (
            RangeContainer(Range(5, 10)),
            Range(3, 7),
            RangeContainer(Range(3, 10)),
        ),
        (
            RangeContainer(Range(5, 10)),
            Range(8, 12),
            RangeContainer(Range(5, 12)),
        ),
        (
            RangeContainer(Range(5, 10), Range(15, 20)),
            Range(8, 17),
            RangeContainer(Range(5, 20)),
        ),
        (
            RangeContainer(Range(5, 10), Range(15, 20)),
            Range(3, 12),
            RangeContainer(Range(3, 12), Range(15, 20)),
        ),
        (
            RangeContainer(Range(5, 10), Range(15, 20)),
            Range(3, 17),
            RangeContainer(Range(3, 20)),
        ),
        (
            RangeContainer(Range(5, 10), Range(15, 20)),
            Range(7, 22),
            RangeContainer(Range(5, 22)),
        ),
        (
            RangeContainer(Range(5, 10), Range(15, 20), Range(25, 30)),
            Range(7, 27),
            RangeContainer(Range(5, 30)),
        ),
        (
            RangeContainer(Range(5, 10), Range(15, 20), Range(25, 30)),
            Range(7, 22),
            RangeContainer(Range(5, 22), Range(25, 30)),
        ),
        (
            RangeContainer(Range(5, 10), Range(15, 20), Range(25, 30)),
            Range(3, 22),
            RangeContainer(Range(3, 22), Range(25, 30)),
        ),
        (
            RangeContainer(Range(5, 10), Range(15, 20), Range(25, 30)),
            Range(31, 35),
            RangeContainer(Range(5, 10), Range(15, 20), Range(25, 35)),
        ),
        (
            RangeContainer(Range(5, 10), Range(15, 20), Range(25, 30)),
            Range(11, 14),
            RangeContainer(Range(5, 20), Range(25, 30)),
        ),
        (
            RangeContainer(),
            Range(5, 5),
            RangeContainer(Range(5, 5)),
        ),
        (
            RangeContainer(Range(5, 5)),
            Range(6, 6),
            RangeContainer(Range(5, 6)),
        ),
        (
            RangeContainer(Range(10, 15)),
            Range(9, 9),
            RangeContainer(Range(9, 15)),
        ),
        (
            RangeContainer(Range(10, 15), Range(20, 25)),
            Range(1, 3),
            RangeContainer(Range(1, 3), Range(10, 15), Range(20, 25)),
        ),
        (
            RangeContainer(Range(10, 15), Range(20, 25)),
            Range(40, 45),
            RangeContainer(Range(10, 15), Range(20, 25), Range(40, 45)),
        ),
        (
            RangeContainer(Range(5, 10)),
            Range(12, 15),
            RangeContainer(Range(5, 10), Range(12, 15)),
        ),
        (
            RangeContainer(Range(5, 10), Range(20, 25)),
            Range(13, 17),
            RangeContainer(Range(5, 10), Range(13, 17), Range(20, 25)),
        ),
        (
            RangeContainer(Range(5, 10), Range(16, 20)),
            Range(11, 15),
            RangeContainer(Range(5, 20)),
        ),
        (
            RangeContainer(Range(10, 15), Range(20, 25), Range(30, 35)),
            Range(5, 40),
            RangeContainer(Range(5, 40)),
        ),
        (
            RangeContainer(Range(5, 10), Range(15, 20)),
            Range(11, 14),
            RangeContainer(Range(5, 20)),
        ),
        (
            RangeContainer(Range(5, 10)),
            Range(5, 10),
            RangeContainer(Range(5, 10)),
        ),
        (
            RangeContainer(Range(10, 20)),
            Range(5, 25),
            RangeContainer(Range(5, 25)),
        ),
        (
            RangeContainer(Range(10, 20)),
            Range(5, 9),
            RangeContainer(Range(5, 20)),
        ),
        (
            RangeContainer(Range(10, 20)),
            Range(21, 25),
            RangeContainer(Range(10, 25)),
        ),
        (
            RangeContainer(Range(5, 10), Range(15, 20), Range(25, 30), Range(35, 40)),
            Range(16, 29),
            RangeContainer(Range(5, 10), Range(15, 30), Range(35, 40)),
        ),
        (
            RangeContainer(Range(10, 19)),
            Range(20, 30),
            RangeContainer(Range(10, 30)),
        ),
    ],
)
def test_merge(start: RangeContainer, new_range: Range, expected: RangeContainer) -> None:
    start.merge(new_range)
    assert start == expected