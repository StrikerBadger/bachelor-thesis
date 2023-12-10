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
        execution_time = time.process_time_ns()
        res = PoiBin(p_is).get_pmf_xi()
        execution_time = time.process_time_ns() - execution_time
        execution_times.append(execution_time)
        results.append(list(res))
    assert all([res == results[0] for res in results]), 'Results are not consistent'
    return res, statistics.mean(execution_times)

def plot_execution_times(df):
    shot_amnts = df['shot_amnt'].unique()
    execution_times = df.groupby('shot_amnt')['execution_time_ns'].mean()
    plt.scatter(shot_amnts, execution_times)
    plt.ylim(0, 500000)
    plt.title('Mean Execution Times for the FFT Algorithm')
    plt.xlabel('Number of Shots')
    plt.ylabel('Mean Execution Time (ns)')
    plt.savefig('graphs/fft_execution_times.png')
    
if __name__ == '__main__':
    df = pd.read_csv('dataset/intersection/statsbomb_matches_shots/shots_per_match.csv')
    res = df['shot_xgs'].apply(assess_fft)
    pmfs, execution_times = res.apply(lambda x: x[0]), res.apply(lambda x: x[1])
    df.loc[:, 'poi_bin_pmf'] = pmfs
    df.loc[:, 'execution_time_ns'] = execution_times
    plot_execution_times(df)