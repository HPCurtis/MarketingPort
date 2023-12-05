"""
Plotting utility functions.
"""

from typing import Any, Dict, Optional, Tuple, Union

import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.collections import PolyCollection
from matplotlib.lines import Line2D

def plotcampaign(full_df):

    media_campaign_product = 'Pixelophone_XL'

    campaign_start = pd.Timestamp('2023-01-01')
    campaign_end = pd.Timestamp('2023-06-30')

    # Check the effect of the media campaign on the selected product's sales
    media_campaign_data = full_df[full_df['Product'] == media_campaign_product]

    # Split the data into pre, during and post campaign periods
    pre_campaign_data = media_campaign_data[media_campaign_data['Date'] < campaign_start]
    during_campaign_data = media_campaign_data[(media_campaign_data['Date'] >= campaign_start) & (media_campaign_data['Date'] <= campaign_end)]
    post_campaign_data = media_campaign_data[media_campaign_data['Date'] > campaign_end]


    # Plot the pre campaign sales with a specific color (for example, 'blue')
    plt.plot(pre_campaign_data['Date'], pre_campaign_data['Sales'], color='blue', label='Pre Campaign')

    # Plot the during campaign sales with a different color (for example, 'red')
    plt.plot(during_campaign_data['Date'], during_campaign_data['Sales'], color='red', label='During Campaign')

    # Plot the post campaign sales with the same color as pre campaign (for example, 'blue')
    plt.plot(post_campaign_data['Date'], post_campaign_data['Sales'], color='blue', label='Post Campaign')

    # Plot the joining line between pre and during campaign
    plt.plot([pre_campaign_data['Date'].iloc[-1], during_campaign_data['Date'].iloc[0]], 
            [pre_campaign_data['Sales'].iloc[-1], during_campaign_data['Sales'].iloc[0]], color='red')

    # Plot the joining line between during and post campaign
    plt.plot([during_campaign_data['Date'].iloc[-1], post_campaign_data['Date'].iloc[0]], 
            [during_campaign_data['Sales'].iloc[-1], post_campaign_data['Sales'].iloc[0]], color='red')

    plt.title('Effect of Media Campaign on Pixelophone_XL')
    plt.xlabel('Time')
    plt.ylabel('Sales')
    plt.legend(loc='upper right')  # Add a legend to distinguish the three periods
    plt.savefig('product saales.png', dpi=300) 
    plt.show()
    

def plot_xY(
x: Union[pd.DatetimeIndex, np.array],
Y: xr.DataArray,
ax: plt.Axes,
plot_hdi_kwargs: Optional[Dict[str, Any]] = None,
hdi_prob: float = 0.94,
label: Union[str, None] = None,
) -> Tuple[Line2D, PolyCollection]:
    """
    Utility function to plot HDI intervals.

    :param x:
        Pandas datetime index or numpy array of x-axis values
    :param y:
        Xarray data array of y-axis data
    :param ax:
        Matplotlib ax object
    :param plot_hdi_kwargs:
        Dictionary of keyword arguments passed to ax.plot()
    :param hdi_prob:
        The size of the HDI, default is 0.94
    :param label:
        The plot label
    """

    if plot_hdi_kwargs is None:
        plot_hdi_kwargs = {}

    (h_line,) = ax.plot(
        x,
        Y.mean(dim=["chain", "draw"]),
        ls="-",
        **plot_hdi_kwargs,
        label=f"{label}",
    )
    ax_hdi = az.plot_hdi(
        x,
        Y,
        hdi_prob=hdi_prob,
        fill_kwargs={
            "alpha": 0.25,
            "label": " ",
        },
        smooth=False,
        ax=ax,
        **plot_hdi_kwargs,
    )
    # Return handle to patch. We get a list of the childen of the axis. Filter for just
    # the PolyCollection objects. Take the last one.
    h_patch = list(
        filter(lambda x: isinstance(x, PolyCollection), ax_hdi.get_children())
    )[-1]
    return (h_line, h_patch)



   