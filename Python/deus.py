import sys


def ebit(rev: float, oper_ex: float, d_a: float) -> float:
    return (rev - oper_ex) - d_a


def nopat(ebit: float, tax_rate: float) -> float:
    return ebit * (1 - tax_rate)


def fcf(nopat: float, d_a: float, capex: float, nwc: float) -> float:
    return nopat + d_a - capex - nwc


def wacc(
    rev: float,
    fin_equity: float,
    perc_equity: float,
    fin_debt: float,
    perc_debt: float,
    tax: float,
) -> float:
    equity = (fin_equity / rev * 100) * perc_equity
    debt = (fin_debt / rev * 100) * perc_debt * (1 - tax)
    return equity + debt


def parse_input(prompt: str) -> float:
    try:
        return float(input(prompt))
    except ValueError:
        print("[WARNING ⚠️ ] Found corrupt number input")
        sys.exit(1)


def parse_percent(prompt: str) -> float:
    return parse_input(prompt) / 100.0


def main():
    revenue = parse_input("What's revenue? ")
    oper_ex = parse_input("What's Operating Expenses? ")
    D_A = parse_input("What's the D&A? ")
    tx_rate = parse_percent("What's the tax rate [expressed as a %]? ")
    cap_ex = parse_input("What's the CapEx? ")
    inc_nwc = parse_input("What's ^NWC? ")

    EBIT = ebit(revenue, oper_ex, D_A)
    print(f"\nEBIT = {EBIT}\n")

    NOPAT = nopat(EBIT, tx_rate)
    print(f"NOPAT = {NOPAT}\n")

    FCF = fcf(NOPAT, D_A, cap_ex, inc_nwc)
    print(f"FCF = {FCF}\n")


if __name__ == "__main__":
    main()
