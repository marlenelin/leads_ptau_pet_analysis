import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def plot_ptau_box(
    df,
    x_col,
    y_col,
    ylabel,
    title,
    thresholds=None,   # <-- NEW
    figsize=(8, 8)
):
    """
    thresholds: list of dicts, e.g.
    [
        {"value": 0.751, "label": "EOAD cutoff: 0.762 pg/mL", "color": "black"},
        {"value": 0.470, "label": "NCRAD cutoff: 0.470 pg/mL", "color": "blue"},
    ]
    """

    sns.set_theme(style="white", context="talk")

    fig, ax = plt.subplots(figsize=figsize)

    sns.boxplot(
        data=df,
        x=x_col,
        y=y_col,
        palette=sns.color_palette("Paired")[8:],
        width=0.5,
        linewidth=1.2,
        showfliers=False,
        ax=ax
    )

    sns.stripplot(
        data=df,
        x=x_col,
        y=y_col,
        color="black",
        alpha=0.5,
        size=3,
        jitter=0.25,
        ax=ax
    )

    ax.set_xlabel("")
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # log1p scale
    ax.set_yscale("function", functions=(np.log1p, np.expm1))

    ticks = [0, 1, 2, 3, 5, 7]
    ax.set_yticks(ticks)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: f"{v:g}"))

    # -----------------------------
    # Threshold lines (NEW)
    # -----------------------------
    if thresholds is not None:
        ymin, ymax = ax.get_ylim()

        for i, th in enumerate(thresholds):
            value = th.get("value")
            label = th.get("label", "")
            color = th.get("color", "black")

            ax.axhline(value, color=color, linestyle="--", linewidth=1)

            # stagger labels slightly to avoid overlap
            y_offset = value * (1.02 + 0.05 * i)

            ax.text(
                0.25,
                y_offset,
                label,
                color=color,
                fontsize=10
            )

    sns.despine(ax=ax)
    fig.tight_layout()

    return fig, ax