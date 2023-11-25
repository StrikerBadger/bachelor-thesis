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
        start = time.time()
        # Initialize the dp table
        p_k = [1] + [0]*self.n
        # Iterate over the dp table
        for i in range(self.n+1):
            for c in range(i, 0, -1):
                inc = self.p_is[i-1]*p_k[c-1]
                p_k[c-1] -= inc
                p_k[c] += inc
        print(f"DP-based Poisson Binomial PDF takes {time.time() - start} seconds")
        return p_k 
        
    # FFT-based Poisson Binomial PDF
    def fft_poibin_pdf(self):
        res = None
        fft_calculator = PoiBin(self.p_is)
        start = time.time()
        res = fft_calculator.get_pmf_xi()
        print(f"FFT-based Poisson Binomial PDF takes {time.time() - start} seconds")
        return 
    
if __name__ == '__main__':
    # Test the algorithm
    p_is = [random.random() for i in range(25)]
    poibinc = PoiBinCalculator(p_is)
    poibinc.dp_poibin_pdf()
    poibinc.fft_poibin_pdf()