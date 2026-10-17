

MAX_VALUE = 1_000_000_000_000_000_000
MIN_VALUE = -1_000_000_000_000_000_000
MOD = 998_244_353

def _sanity():
    assert 10**17 <= MAX_VALUE <= 10**19, f"MAX_VALUE suspicious: {MAX_VALUE}"
    assert -10**19 <= MIN_VALUE <= -10**17, f"MIN_VALUE suspicious: {MIN_VALUE}"
    assert MOD in (998_244_353, 1_000_000_007)
_sanity()