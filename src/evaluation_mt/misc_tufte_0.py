import matplotlib.pyplot as plt
import numpy as np

data = {
    "BLEURT": [0.17, 0.18, 0.185, 0.19, 0.195, 0.198, 0.201, 0.204, 0.20, 0.205, 0.21],
    "COMET_20": [0.16, 0.17, 0.175, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18],
    "chrF": [0.13, 0.14, 0.145, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15],
    "BLEU": [0.09, 0.10, 0.105, 0.11, 0.115, 0.118, 0.121, 0.124, 0.12, 0.13, 0.14]
}

data = {k:np.array(v) for k, v in data.items()}
xticks = np.array(list(range(len(data["BLEURT"]))))

plt.figure(figsize=(8, 4))

for i, (k, v) in enumerate(data.items()):
    plt.bar(
        xticks-i/5+0.3,
        v,
        width=0.2,
        label=k
    )

# plt.ylim(0.08, None)
plt.ylabel("Kendall's $\\tau$")
plt.xlabel("References count")
plt.legend(loc="lower right", ncols=2)

plt.tight_layout()
plt.savefig("/home/vilda/Downloads/figure_bad.svg")
plt.show()
plt.close()


