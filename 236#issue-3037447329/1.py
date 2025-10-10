def plot1(data, sample_dims=None):
    print(f"Plot1 using sample_dims={sample_dims}")

def plot2(data, sample_dims=None):
    print(f"Plot2 using sample_dims={sample_dims}")

def combine_plots(data, sample_dims=None):
    plot1(data, sample_dims=sample_dims)
    plot2(data, sample_dims=sample_dims)

combine_plots(data=[1,2,3], sample_dims=5)
