import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# --- Setup ---
os.makedirs("plots", exist_ok=True)
df = pd.read_csv("results/benchmark.csv")

sns.set(style="whitegrid", font_scale=1.2)

# Metrics to compare (use actual CSV column names)
metrics = [
    "KeyGen(s)",
    "Decrypt(s)",
    "KeySize(Bytes)",
    "Memory_PyHeap_KB",
    "Memory_RSS_KB",
]


def sanitize_filename(s: str) -> str:
    return (
        s.replace(" ", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
    )


# --- Plot each metric ---
for metric in metrics:
    try:
        plt.figure(figsize=(8, 5))
        # use the newer `errorbar` parameter instead of deprecated `ci`
        ax = sns.barplot(
            data=df, x="Algo", y=metric, palette=["#2E86AB", "#E67E22"], errorbar="sd"
        )

        # Title and labels
        plt.title(f"{metric} Comparison: RSA vs Kyber512", fontsize=14, weight="bold")
        plt.ylabel(metric)
        plt.xlabel("Algorithm")

        # Calculate and display difference percentage safely
        rsa_vals = df[df["Algo"] == "RSA"][metric]
        kyber_vals = df[df["Algo"] == "Kyber512"][metric]
        rsa_mean = rsa_vals.mean() if not rsa_vals.empty else np.nan
        kyber_mean = kyber_vals.mean() if not kyber_vals.empty else np.nan

        if np.isfinite(rsa_mean) and rsa_mean != 0:
            diff = ((kyber_mean - rsa_mean) / rsa_mean) * 100
            diff_text = f"Kyber512 is {abs(diff):.2f}% {'faster' if diff < 0 else 'slower'} than RSA"
            color = "green" if diff < 0 else "red"
        else:
            diff = np.nan
            diff_text = "Insufficient data to compute difference"
            color = "black"

        # Annotate bars with values
        for p in ax.patches:
            try:
                ax.annotate(
                    f"{p.get_height():.4f}",
                    (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha="center",
                    va="bottom",
                    fontsize=10,
                )
            except Exception:
                pass

        # Show difference note on top
        try:
            ymax = np.nanmax(df[metric].values)
            y_pos = ymax * 1.05 if np.isfinite(ymax) else ax.get_ylim()[1] * 0.9
        except Exception:
            y_pos = ax.get_ylim()[1] * 0.9

        plt.text(0.5, y_pos, diff_text, color=color, ha="center", fontsize=11, weight="bold")

        plt.tight_layout()
        out_name = f"plots/{sanitize_filename(metric)}_comparison.png"
        plt.savefig(out_name)
        print(f"✅ Saved plot: {os.path.basename(out_name)} (Difference: {diff if not np.isnan(diff) else 'N/A'})")

    except Exception as e:
        print(f"⚠️ Skipped metric {metric}: {e}")


print("\n📊 All plots processed; check the 'plots/' folder for generated images.")
