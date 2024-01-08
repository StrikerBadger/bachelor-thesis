import pandas as pd
from poibin.poibin import PoiBin
from matplotlib import pyplot as plt
import time
import statistics

def assess_fft(p_is, repeat=100):
    p_is = [float(p_i) for p_i in p_is[1:-1].split(', ')]
    execution_times = []
    results = []
    for _ in range(repeat):
        execution_time = time.perf_counter_ns()
        # Initialize the dp table
        n = len(p_is)
        p_k = [1] + [0]*n
        # Iterate over the dp table
        for i in range(n+1):
            for c in range(i, 0, -1):
                inc = p_is[i-1]*p_k[c-1]
                p_k[c-1] -= inc
                p_k[c] += inc
        res = p_k
        execution_time = time.perf_counter_ns() - execution_time
        execution_times.append(execution_time)
        results.append(list(res))
    assert all([res == results[0] for res in results]), 'Results are not consistent'
    return res, statistics.mean(execution_times)

def plot_execution_times(df):
    shot_amnts = df['shot_amnt'].unique()
    execution_times = df.groupby('shot_amnt')['execution_time_ns'].mean()
    plt.scatter(shot_amnts, execution_times)
    plt.ylim(0, 500000)
    plt.title('Mean Execution Times for the DP Algorithm')
    plt.xlabel('Number of Shots')
    plt.ylabel('Mean Execution Time (ns)')
    plt.savefig('graphs/dp_execution_times.png')
    
if __name__ == '__main__':
    df = pd.read_pickle('dataset/intersection/statsbomb_matches_shots/shots_per_match.pkl')
    res = df['shot_xgs'].apply(assess_fft)
    pmfs, execution_times = res.apply(lambda x: x[0]), res.apply(lambda x: x[1])
    df.loc[:, 'poi_bin_pmf'] = pmfs
    df.loc[:, 'execution_time_ns'] = execution_times
    df.to_csv('execution_times_dp.csv', index=False)
    plot_execution_times(df)