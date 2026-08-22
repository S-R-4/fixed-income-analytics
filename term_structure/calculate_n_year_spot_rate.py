#WORKS FOR PAR RATE FUNCTION
#WORKS FOR FORWARD RATE APPROACH SOLVING FOR PV
#WORKS FOR SPOT RATE APPROACH SOLVING FOR PV

def calculate_n_year_spot_rate():
    N = int(input("Enter the number of years (N): "))
    
    forward_rates = []
    first_rate = input("Enter 1YR Forward Rate 0 YEAR(s) from now (or 'NA' to input Spot Rates directly): ")
    
    if first_rate.lower() == 'na':
        spot_rates = []
        for i in range(N):
            rate = float(input(f"Enter {i+1}YR Spot Rate 0 YEAR(s) from now (as a decimal, e.g., 0.05 for 5%): "))
            spot_rates.append(rate)
    else:
        forward_rates.append(float(first_rate))
        for i in range(1, N):
            rate = float(input(f"Enter 1YR Forward Rate {i} YEAR(s) from now (as a decimal, e.g., 0.05 for 5%): "))
            forward_rates.append(rate)
        
        # Calculate spot rates from forward rates
        spot_rates = []
        product = 1
        for i in range(N):
            product *= (1 + forward_rates[i])
            spot_rate = product**(1/(i+1)) - 1
            spot_rates.append(spot_rate)
    
    for i, rate in enumerate(spot_rates):
        print(f"The {i+1}YR Spot Rate 0 YEAR(s) from now is: {rate:.6f}")
    
    PV_input = input("Enter Present Value (PV) or 'X' if unknown: ")
    PMT_input = input("Enter Payment (PMT) or 'X' if unknown: ")
    FV_input = input("Enter Future Value (FV) or 'X' if unknown: ")
    
    discount_factors = [(1 / ((1 + spot_rates[i]) ** (i+1))) for i in range(N)]
    
    if PV_input.lower() == 'x':
        PMT = float(PMT_input)
        FV = float(FV_input)
        PV = sum(PMT * df for df in discount_factors[:-1]) + (PMT + FV) * discount_factors[-1]
        print(f"The Present Value (PV) is: {PV:.6f}")
        return PV
    elif PMT_input.lower() == 'x':
        PV = float(PV_input)
        FV = float(FV_input)
        PMT = (PV - FV * discount_factors[-1]) / sum(discount_factors)
        print(f"The Payment (PMT) is: {PMT:.6f}")
        return PMT
    elif FV_input.lower() == 'x':
        PV = float(PV_input)
        PMT = float(PMT_input)
        FV = (PV - sum(PMT * df for df in discount_factors[:-1])) / discount_factors[-1] - PMT
        print(f"The Future Value (FV) is: {FV:.6f}")
        return FV
    else:
        print("Error: Please enter 'X' for exactly one unknown variable.")
        return None

# Run the function
calculate_n_year_spot_rate()
