import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import pearsonr

def autocorrelation_sample(sample_matrix, max_lag):
    acf_samples = []
    num_samples = sample_matrix.shape[1]
    for sample in range(num_samples):
        nad_positions = np.where(sample_matrix[:, sample] == 1)[0]
        acf = []
        total_nads = len(nad_positions)
        for lag in range(1, max_lag + 1):
            valid_pairs = 0
            total_pairs = 0
            for i in range(total_nads):
                if i + lag < total_nads:
                    total_pairs += 1
                    distance = nad_positions[i + lag] - nad_positions[i]
                    if distance == lag:
                        valid_pairs += 1
            acf.append(valid_pairs / total_pairs if total_pairs > 0 else 0)
        acf_samples.append(acf)
    return np.array(acf_samples)

def exp_decay(x, a, b):
    return a * np.exp(-b * x)

def load_sample_matrix(file_path):
    df = pd.read_excel(file_path, header=None)
    return df.to_numpy()

def process_sample_matrix(sample_matrix, max_lag=50):
    acf_samples = autocorrelation_sample(sample_matrix, max_lag)
    avg_acf = np.mean(acf_samples, axis=0)
    return avg_acf, acf_samples

def plot_acf_results(esc_avg_acf, npc_avg_acf, esc_rand_acf, npc_rand_acf, max_lag=50):
    x = np.arange(1, max_lag + 1)
    
    # Plot average ACFs
    plt.figure(figsize=(12, 7))
    plt.plot(x, esc_avg_acf, label='ESC', color='blue')
    plt.plot(x, npc_avg_acf, label='NPC', color='red')
    plt.plot(x, esc_rand_acf, label='ESC Random', color='cyan')
    plt.plot(x, npc_rand_acf, label='NPC Random', color='orange')
    plt.title('Average Autocorrelation Function (Real vs Random)')
    plt.xlabel('Lag (bins)')
    plt.ylabel('Autocorrelation')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    # Plot exponential decay fits
    plt.figure(figsize=(12, 7))
    for label, acf, color in [
        ('ESC', esc_avg_acf, 'blue'),
        ('NPC', npc_avg_acf, 'red'),
        ('ESC Random', esc_rand_acf, 'cyan'),
        ('NPC Random', npc_rand_acf, 'orange')
    ]:
        popt, _ = curve_fit(exp_decay, x, acf, maxfev=10000)
        plt.plot(x, acf, label=f'{label} ACF', color=color)
        plt.plot(x, exp_decay(x, *popt), '--', label=f'{label} Fit (a={popt[0]:.2f}, b={popt[1]:.2f})', color=color)

    plt.title('ACF with Exponential Fits (Real vs Random)')
    plt.xlabel('Lag (bins)')
    plt.ylabel('Autocorrelation')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def calculate_pearson_correlation(acf1, acf2):
    corr_coefficient, p_value = pearsonr(acf1, acf2)
    return corr_coefficient, p_value

# File paths
esc_file = "esc53_1_0_matrix.xlsx"
npc_file = "npc23_1_0_matrix.xlsx"
esc_rand_file = "ESC_53_random.xlsx"
npc_rand_file = "NPC_23_random.xlsx"

# Load data
esc_matrix = load_sample_matrix(esc_file)
npc_matrix = load_sample_matrix(npc_file)
esc_rand_matrix = load_sample_matrix(esc_rand_file)
npc_rand_matrix = load_sample_matrix(npc_rand_file)

# Process matrices
esc_avg_acf, _ = process_sample_matrix(esc_matrix)
npc_avg_acf, _ = process_sample_matrix(npc_matrix)
esc_rand_avg_acf, _ = process_sample_matrix(esc_rand_matrix)
npc_rand_avg_acf, _ = process_sample_matrix(npc_rand_matrix)

# Correlation stats
corr, pval = calculate_pearson_correlation(esc_avg_acf, npc_avg_acf)
print(f"Pearson correlation (ESC vs NPC): {corr:.3f}, p-value: {pval:.3e}")

# Plot all results
plot_acf_results(esc_avg_acf, npc_avg_acf, esc_rand_avg_acf, npc_rand_avg_acf)

