import arviz as az
from arviz_plots import combine_plots
import csv
import os
import xarray as xr


default_data = az.load_arviz_data("non_centered_eight")


def merge_chain_draw(data):
    new_data = data.copy()
    for var in new_data.data_vars:
        arr = new_data[var].values
        shape = arr.shape
        if len(shape) < 2:
            continue
        new_arr = arr.reshape(-1, *shape[2:])
        new_data[var] = (("sample",) + data[var].dims[2:], new_arr)
    return new_data

merged_data = merge_chain_draw(default_data)


invalid_data = xr.Dataset({"mu": xr.DataArray([])})


large_data = default_data.copy()
large_data = large_data.assign(draw=range(10000))

datasets = {
    "default": default_data,
    "merged_chain_draw": merged_data,
    "invalid": invalid_data,
    "large_data": large_data,
}


layouts = [
    {"plots": ["trace", "posterior"]},
    {"plots": ["posterior", "trace"]},
    {"plots": ["invalid_plot"]},
    {"plots": []},
    {},
]

valid_plots = ["trace", "posterior", "density"]



results = []

for ds_name, data in datasets.items():
    for layout in layouts:
        try:
            print(f"\nTesting dataset: {ds_name}, layout: {layout}")
        
            if "posterior" not in data:
                results.append((ds_name, str(layout), "Failed", "Missing posterior group"))
                continue
            for var in data.data_vars:
                if data[var].shape[0] == 0 or (len(data[var].shape) > 1 and data[var].shape[1] == 0):
                    results.append((ds_name, str(layout), "Failed", f"Empty dimensions for {var}"))
                    continue

            if "plots" not in layout or not layout["plots"]:
                results.append((ds_name, str(layout), "Failed", "Empty or missing plots key"))
                continue
            if not all(p in valid_plots for p in layout["plots"]):
                results.append((ds_name, str(layout), "Failed", f"Invalid plot types: {layout['plots']}"))
                continue
        
            if any(max(data[var].shape) > 10000 for var in data.data_vars):
                results.append((ds_name, str(layout), "Failed", "Dataset too large"))
                continue
            
            combine_plots(data, **layout)
            results.append((ds_name, str(layout), "Success", ""))
        except Exception as e:
            results.append((ds_name, str(layout), "Failed", str(e)))



output_file = "combine_plots_test_results.csv"
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Dataset", "Layout", "Result", "Error"])
    for row in results:
        writer.writerow(row)

print(f"\nAll test results saved to {os.path.abspath(output_file)}")