def present_value(fututure_value: float, rate: float, periods: int) -> float:
    # calc the present value of a single future cash flow
    return fututure_value / ((1 + rate) ** periods)

def net_present_value(rate: float, initial_investment: float, cash_flows: list[float]) -> float:
    # calcs net present value (NPV) for a series of cash flows
    npv = -initial_investment # initial outflow at t=0

    # discount each cash flow back to present value (starting at t=1)
    for period, cash_flow in enumerate(cash_flows, start=1):
        npv += present_value(cash_flow, rate, period)

    return npv

# an example we'll use it...
# project costs $100,000 up front
# discount rate (cost of capital): 8%
# expected cash flow over 4 yrs: $30K, 35K, 40K and 45K

discount_rate = 0.08
upfront_cost = 100000.0
projected_cash_flows = [30000.0, 35000.0, 40000.0, 45000.0]

npv_result = net_present_value(discount_rate, upfront_cost, projected_cash_flows)

print(f"Project NPV: ${npv_result:.2f}")

if npv_result > 0:
    print("Verdict: Accept project [Creates value above required return]")
else:
    print("Verdict: Reject project [Failed to meet required return]")