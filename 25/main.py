from aoc import DEBUG, read_input

DECIMAL_DIGITS = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
SNAFU_DIGITS = ["0", "1", "2", "=", "-"]


def snafu_to_decimal(snafu: str) -> int:
    return sum(DECIMAL_DIGITS[d] * 5**pow for pow, d in enumerate(snafu[::-1]))


def decimal_to_snafu(decimal: int) -> str:
    snafu = ""
    while decimal:
        mod = decimal % 5
        snafu += SNAFU_DIGITS[mod]
        if mod > 2:
            decimal += mod
        decimal //= 5
    return snafu[::-1] or "0"


if DEBUG:
    for decimal, snafu in (
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "1="),
        (4, "1-"),
        (5, "10"),
        (6, "11"),
        (7, "12"),
        (8, "2="),
        (9, "2-"),
        (10, "20"),
        (15, "1=0"),
        (20, "1-0"),
        (2022, "1=11-2"),
        (12345, "1-0---0"),
        (314159265, "1121-1110-1=0"),
    ):
        assert snafu_to_decimal(snafu) == decimal
        assert decimal_to_snafu(decimal) == snafu


s = sum(snafu_to_decimal(x) for x in read_input().splitlines())
print("Part 1:", decimal_to_snafu(s))
