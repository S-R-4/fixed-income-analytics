def solve_implied_forward():
    A = int(input("Enter the number of years for Spot_Rate_A (A): "))
    Spot_Rate_A = input("Enter Spot_Rate_A (or 'X' to solve for it): ")
    B = int(input("Enter the number of years for Spot_Rate_B (B): "))
    Spot_Rate_B = input("Enter Spot_Rate_B (or 'X' to solve for it): ")
    IFR_A_BA = input(f"Enter the {B-A} year Implied Forward Rate {A} years from now (or 'X' to solve for it): ")
    
    # Convert inputs to float or keep as unknown variable
    Spot_Rate_A = None if Spot_Rate_A.lower() == 'x' else float(Spot_Rate_A)
    Spot_Rate_B = None if Spot_Rate_B.lower() == 'x' else float(Spot_Rate_B)
    IFR_A_BA = None if IFR_A_BA.lower() == 'x' else float(IFR_A_BA)

    if Spot_Rate_B is None:  # Solve for Spot_Rate_B
        Spot_Rate_B = ((1 + Spot_Rate_A) ** A * (1 + IFR_A_BA) ** (B - A)) ** (1 / B) - 1
        print(f"The {B}-year Spot Rate (Z_B) is: {Spot_Rate_B:.6f}")
    
    elif Spot_Rate_A is None:  # Solve for Spot_Rate_A
        Spot_Rate_A = ((1 + Spot_Rate_B) ** B / (1 + IFR_A_BA) ** (B - A)) ** (1 / A) - 1
        print(f"The {A}-year Spot Rate (Z_A) is: {Spot_Rate_A:.6f}")
    
    elif IFR_A_BA is None:  # Solve for IFR_A_BA
        IFR_A_BA = ((1 + Spot_Rate_B) ** B / (1 + Spot_Rate_A) ** A) ** (1 / (B - A)) - 1
        print(f"The {B-A}-year Implied Forward Rate {A} year(s) from now is: {IFR_A_BA:.6f}")

    else:
        print("No variable to solve for.")

# Run the function
solve_implied_forward()
