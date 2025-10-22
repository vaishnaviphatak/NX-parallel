import arviz as az
from arviz_plots import combine_plots
import matplotlib.pyplot as plt


data = az.load_arviz_data("non_centered_eight")


print("Testing combine_plots with trace and posterior...")
try:
   
    plot = combine_plots(data, plots=["trace", "posterior"])
    plt.show()  
    print("Success: Combined trace and posterior plots generated.")
except Exception as e:
    print(f"Error in trace + posterior: {e}")

print("\nTesting combine_plots with trace and forest...")
try:
   
    plot = combine_plots(data, plots=["trace", "forest"])
    plt.show()  
    print("Success: Combined trace and forest plots generated.")
except Exception as e:
    print(f"Error in trace + forest: {e}")

