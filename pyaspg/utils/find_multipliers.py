import pandas as pd
from scipy.optimize import minimize

# REPLAY_PATH = f"./simulation_results/dataset2/scenario-hyb-90.10/uniform/uniform-secure-echo/"
# DISTRIBUTION_ASSIGNMENT_PATH = REPLAY_PATH + "../distribution_assignments.pkl"

# prosumers_df = pd.read_csv(REPLAY_PATH + "prosumers.csv")

def find_multipliers(prosumers_df):
    results = {}  # Dictionary to store results for each timestep
    
    # Loop through each unique timestep in the DataFrame
    for timestep in prosumers_df['timestep'].unique():
        # Filter data for the current timestep
        timestep_df = prosumers_df[prosumers_df['timestep'] == timestep]

        # Group by 'distributor_name' and sum 'net_power_before' for each group
        group_A_sum = timestep_df[timestep_df['distributor_name'] == timestep_df['distributor_name'].unique()[0]]['net_power_before'].sum()
        group_B_sum = timestep_df[timestep_df['distributor_name'] == timestep_df['distributor_name'].unique()[1]]['net_power_before'].sum()
        
        original_sum = group_A_sum + group_B_sum

        # Define the loss function for this timestep
        def loss_function(multipliers):
            multiplier_A, multiplier_B = multipliers
            weighted_sum = multiplier_A * group_A_sum + multiplier_B * group_B_sum
            return abs(original_sum - weighted_sum)  # Using absolute difference

        # Initial guesses for the multipliers
        initial_guess = [1, 0.5]

        # Constraints and bounds
        constraints = [
            {'type': 'ineq', 'fun': lambda x: x[0]},                  # multiplier_A >= 0
            {'type': 'ineq', 'fun': lambda x: abs(x[0] - x[1]) - 0.01}  # A != B
        ]
        bounds = [(0, None), (0, 1)]  # A >= 0, 0 <= B <= 1

        # Solve the optimization for this timestep
        result = minimize(loss_function, initial_guess, bounds=bounds, constraints=constraints)
        multiplier_A, multiplier_B = result.x

        # Calculate the weighted sum and the loss
        weighted_sum = multiplier_A * group_A_sum + multiplier_B * group_B_sum
        loss = abs(original_sum - weighted_sum)

        # Store results for this timestep
        results[timestep] = {'Multiplier_A': multiplier_A, 'Multiplier_B': multiplier_B, 'Loss': loss}
        
        # Print results for each timestep (optional)
        # print(f"Timestep {timestep}: Multiplier for Group A = {multiplier_A}, Multiplier for Group B = {multiplier_B}, Loss = {loss}")

    return results
