# Lab 5 – Issues Found and Fixed (ticket_booking_system.py)

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | Weak hash (MD5) | Bandit B324 | Security | High | 47 | MD5 is broken and unsafe for ticket hashes | Switched to `hashlib.sha256` |
| 2 | Shell command injection | Bandit B605 | Security | High | 58 | `os.system("echo ..." + filename)` runs a shell with an unsanitised filename | Replaced with `print()`; no shell needed |
| 3 | Use of `eval()` | Bandit B307 / Pylint W0123 | Security | Medium | 42 | Promo code string is executed as Python, allowing arbitrary code execution | Takes a numeric `discount_rate` (0–1), validated, and computes `price * (1 - rate)` |
| 4 | Insecure random for PIN | Bandit B311 | Security | Low | 51 | `random` is predictable, not suitable for security PINs | Used `secrets.randbelow(9000) + 1000` |
| 5 | Bare except + pass | Bandit B110 / Flake8 E722 / Pylint W0702 | Bug | Low/Medium | 26-27 | Swallows every error silently, including typos and Ctrl+C | Catch only `KeyError`; return `False`/`True` so callers know the result |
| 6 | Hard-coded secret printed | Manual review | Security | Medium | 70, 79 | Box-office key is in source code and printed to the console | Read from `BOX_OFFICE_KEY` env var; only print whether it is set |
| 7 | Mutable default argument | Pylint W0102 | Bug | Medium | 15 | `order_history=[]` is shared across all calls | Default `None`, create a new list inside the function |
| 8 | Unused import / variables | Flake8 F401, F841 / Pylint W0611, W0612 | Style | Low | 6, 31, 63 | `math`, `booking_fee`, loop var `seat` unused | Removed them |
| 9 | Comparison to None with `==` | Flake8 E711 / Pylint C0121 | Style | Low | 32 | Should use identity check | `is None` |
| 10 | Line too long, %-formatting | Flake8 E501 / Pylint C0209 | Style | Low | 19 | 82 chars, old-style formatting | f-string |
| 11 | File not opened safely | Pylint R1732, W1514 | Bug | Medium | 55-57 | File not closed on error, no encoding | `with open(..., encoding="utf-8")` |
| 12 | Shadowed global name | Pylint W0621 | Style | Low | 61 | Parameter `theater_seats` hides the global | Renamed parameter to `seats` |
| 13 | Naming, docstrings, else-after-return | Pylint C0103, C0116, R1705 | Style | Low | 15, all funcs, 34-37 | `reserveSeat` not snake_case; no docstrings; unneeded `else` | `reserve_seat`, added docstrings, simplified return |
| 14 | Code runs on import, no final newline | Pylint/Flake8 W292, C0304 | Style | Low | 82 | `main()` runs whenever module is imported | `if __name__ == "__main__": main()` + trailing newline |
