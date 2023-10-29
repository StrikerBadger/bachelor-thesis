import numpy as np

class PoiBin():
    
    # Constructor
    def __init__(self, p_is):
        self.p_is = p_is
        self.n = len(p_is)
        
    # DP algorithm (non-optimized)
    def dp_poibin_pdf(self, k, full_dist=False):
        # Initialize the dp table
        p_k = [1] + [0]*self.n
        # Iterate over the dp table
        for i in range(self.n+1):
            for c in range(i, 0, -1):
                inc = self.p_is[i-1]*p_k[c-1]
                p_k[c-1] -= inc
                p_k[c] += inc
        return p_k if full_dist else p_k[k]
        
    # FFT-based Poisson Binomial PDF
    def fft_poibin_pdf(self, k, full_dist=False):
        # Calculate the x array
        x = np.arange(self.n+1, dtype=np.complex64)
        omega = 2*np.pi/(self.n+1)
        exps = np.exp(1j*omega*x)
        for i in range(self.n+1):
            x[i] = np.prod(np.array([1 - p + p*exps[i] for p in self.p_is]))
        # Choose to calculate one entry or full distribution
        return 1/(self.n+1)*np.fft.fft(x)
    
    
if __name__ == '__main__':
    # Test the algorithm
    p_is = np.array([1]*10)
    poibin = PoiBin(p_is)
    print(poibin.dp_poibin_pdf(10))
    print(poibin.fft_poibin_pdf(10)[0].real)