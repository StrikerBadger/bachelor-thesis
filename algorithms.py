import numpy as np
from poibin.poibin import PoiBin
import time
import random

class PoiBinCalculator():
    
    # Constructor
    def __init__(self, p_is):
        self.p_is = p_is
        self.n = len(p_is)
        
    # DP algorithm (non-optimized)
    def dp_poibin_pdf(self):
        execution_time = time.process_time()
        # Initialize the dp table
        p_k = [1] + [0]*self.n
        # Iterate over the dp table
        for i in range(self.n+1):
            for c in range(i, 0, -1):
                inc = self.p_is[i-1]*p_k[c-1]
                p_k[c-1] -= inc
                p_k[c] += inc
        execution_time = time.process_time() - execution_time
        return p_k, execution_time
        
    # FFT-based Poisson Binomial PDF
    def fft_poibin_pdf(self):
        res = None
        fft_calculator = PoiBin(self.p_is)
        execution_time = time.process_time()
        res = fft_calculator.get_pmf_xi()
        execution_time = time.process_time() - execution_time
        return res, execution_time
    
    # Simulation approach
    def sim_poibin_pdf(self, n_sim=10000):
        res = None
        execution_time = time.process_time()
        res = np.zeros(self.n+1)
        for _ in range(n_sim):
            res[np.sum(np.random.uniform(size=self.n) <= self.p_is)] += 1
        res /= n_sim
        execution_time = time.process_time() - execution_time
        return res, execution_time
    
if __name__ == '__main__':
    # Test the algorithm
    p_is = [random.random() for _ in range(5)]
    poibinc = PoiBinCalculator(p_is)
    res_dp, exectime_dp = poibinc.dp_poibin_pdf()
    res_fft, exectime_fft = poibinc.fft_poibin_pdf()
    res_sim, exectime_sim = poibinc.sim_poibin_pdf()
    print('Results:')
    print('DP: ', res_dp)
    print('FFT: ', res_fft)
    print('SIM: ', res_sim)
    print('Execution times (s):')
    print('DP: ', exectime_dp)
    print('FFT: ', exectime_fft)
    print('SIM: ', exectime_sim)
    print('Sum of the probabilities:')
    print('DP: ', np.sum(res_dp))
    print('FFT: ', np.sum(res_fft))
    print('SIM: ', np.sum(res_sim))