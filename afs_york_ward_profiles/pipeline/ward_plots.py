# Description: This script contains functions to create the plots for the ward profiles.

# Importing the required libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from afs_york_ward_profiles.utils.ward_profile_utils import int_or_float


def create_gender_gap_plot(
    data_series: pd.Series,
    comparator_series: pd.Series,
    name: str,
    index: int,
    font_path: str,
    font_size: int,
    fig_size: tuple = (2.5, 2.5),
    save_path: str = None,
) -> plt.Figure:
    """Create a bar chart for the Gender gap

    Args:
        data_series (pd.Series): The series with the data for the ward
        comparator_series (pd.Series): The series with the data for the comparator
        name (str): The name of the ward
        index (int): The index of the data in the series
        font_path (str): The path to the font file
        font_size (int): The size of the font
        save_path (str, optional): The path to save the figure. Defaults to None.

    Returns:
        fig (matplotlib.figure.Figure): The figure with the plot
    """

    # Create the dataframe
    gender_df = pd.DataFrame(
        {
            "Ward": ["York", name],
            "Gender gap": [comparator_series[index], data_series[index]],
        }
    )

    # Load the font
    choice_font = fm.FontProperties(fname=font_path)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=fig_size)

    # Create the bar chart
    ax.barh(gender_df["Ward"], gender_df["Gender gap"], color="#0F294A")

    # Add text with the numbers
    for i, (ward, gap) in enumerate(zip(gender_df["Ward"], gender_df["Gender gap"])):
        if gap < 0:
            ax.text(
                gap + 0.2,
                i,
                int_or_float(gap),
                color="white",
                ha="left",
                va="center",
                fontsize=font_size,
                fontproperties=choice_font,
            )
        elif 0 < gap <= 2:
            ax.text(
                gap - 0.2,
                i,
                int_or_float(gap),
                color="white",
                ha="right",
                va="center",
                fontsize=font_size,
                fontproperties=choice_font,
            )
        else:
            ax.text(
                gap - 0.2,
                i,
                int_or_float(gap),
                color="white",
                ha="right",
                va="center",
                fontsize=font_size,
                fontproperties=choice_font,
            )

    # Remove the axis
    ax.axis("off")

    if save_path:
        # Save the figure
        fig.savefig(save_path, bbox_inches="tight", pad_inches=0, transparent=True)
    else:
        # Return the figure
        return fig


def create_breastfeeding_plot(
    data_series: pd.Series,
    comparator_series: pd.Series,
    name: str,
    index_list: list,
    font_path: str,
    font_size: int,
    fig_size: tuple = (5, 2.5),
    save_path: str = None,
) -> plt.Figure:
    """Create a bar chart for the breastfeeding data

    Args:
        data_series (pd.Series): The series with the data for the ward
        comparator_series (pd.Series): The series with the data for the comparator
        name (str): The name of the ward
        index_list (list): The list with the indexes of the data in the series
        font_path (str): The path to the font file
        font_size (int): The size of the font
        save_path (str, optional): The path to save the figure. Defaults to None.

    Returns:
        fig (matplotlib.figure.Figure): The figure with the plot
    """
    # Creating the dataframe
    type_list = ["Totally", "Partially"]
    dfs = []
    for index, type_ in zip(index_list, type_list):
        df = pd.DataFrame(
            {
                "Ward": ["York", name],
                "Breastfeeding": [comparator_series[index], data_series[index]],
                "Type": [type_] * 2,
            }
        )
        dfs.append(df)

    breastfeeding_df = pd.concat(dfs, axis=0, ignore_index=True)

    # Load the font
    choice_font = fm.FontProperties(fname=font_path)

    # Group the data by 'Ward'
    grouped_df = breastfeeding_df.groupby("Ward")

    # Create subplots for each group
    fig, axs = plt.subplots(1, len(grouped_df), figsize=fig_size, sharey=True)

    # Define the color map based on the 'Breastfeeding' column
    color_map = {"Totally": "#0F294A", "Partially": "#00A8C1"}

    # Iterate over each group and plot the bar chart
    for i, (group, data) in enumerate(grouped_df):
        ax = axs[i]
        ax.bar(data["Type"], data["Breastfeeding"], color=data["Type"].map(color_map))

        # Add percentage text to bars
        for j, value in enumerate(data["Breastfeeding"]):
            ax.text(
                j,
                value - 13,
                f"{value:.0f}%",
                ha="center",
                va="bottom",
                color="white",
                fontsize=font_size,
                fontproperties=choice_font,
            )

        # Remove the axis and titles
        ax.axis("off")

    # Adjust spacing between subplots
    plt.tight_layout()

    if save_path:
        # Save the figure
        fig.savefig(save_path, bbox_inches="tight", pad_inches=0, transparent=True)
    else:
        # Return the figure
        return fig


def create_outcomes_plot(
    data_series: pd.Series,
    comparator_series: pd.Series,
    name: str,
    font_path: str,
    font_size: int,
    fig_size: tuple = (10, 8),
    save_path: str = None,
) -> plt.Figure:
    """Create a bar chart for the outcomes data

    Args:
        data_series (pd.Series): The series with the data for the ward
        comparator_series (pd.Series): The series with the data for the comparator
        name (str): The name of the ward
        font_path (str): The path to the font file
        font_size (int): The size of the font
        save_path (str, optional): The path to save the figure. Defaults to None.

    Returns:
        fig (matplotlib.figure.Figure): The figure with the plot
    """

    # Creating the dataframe
    outcomes_df = pd.DataFrame(
        {
            "York": comparator_series.loc[14:17],
            name: data_series.loc[14:17],
            "measure": ["ASQ 9-12", "ASQ 24-30", "Wellcomm", "Disadvantaged"],
        }
    )
    outcomes_df = outcomes_df.melt(
        id_vars="measure", var_name="Ward", value_name="Value"
    )

    # Load the font
    choice_font = fm.FontProperties(fname=font_path)

    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=fig_size, sharex=True)

    color_map = {name: "#0F294A", "York": "#00A8C1"}

    # Iterate over each measure and plot the bar chart
    for i, (measure, ax) in enumerate(
        zip(outcomes_df["measure"].unique(), axes.flatten())
    ):
        data = outcomes_df[outcomes_df["measure"] == measure]

        # Add grid on the x-axis
        ax.grid(axis="x", alpha=0.5)

        ax.barh(data["Ward"], data["Value"], color=data["Ward"].map(color_map))

        # Add text to the bars
        for ward, value in zip(data["Ward"], data["Value"]):
            if value < 6:
                ax.text(
                    value + 0.2,
                    ward,
                    ward,
                    color="#0F294A",
                    ha="left",
                    va="center",
                    fontsize=font_size,
                    fontproperties=choice_font,
                )
            else:
                ax.text(
                    value - 0.2,
                    ward,
                    ward,
                    color="white",
                    ha="right",
                    va="center",
                    fontsize=font_size,
                    fontproperties=choice_font,
                )

        # Set x-axis ticks to the nearest 2 or 5, set axis to the nearest 2 or 5 higher than the max value
        if outcomes_df["Value"].max() > 15:
            xlim = round(outcomes_df["Value"].max(), 0)
            if xlim % 5 == 0:
                xlim += 1
            else:
                xlim += 5
            ax.set_xlim(0, xlim)
            ax.xaxis.set_major_locator(plt.MultipleLocator(5))
        else:
            xlim = round(outcomes_df["Value"].max(), 0)
            if xlim % 2 == 0:
                xlim += 1
            else:
                xlim += 2
            ax.set_xlim(0, xlim)
            ax.xaxis.set_major_locator(plt.MultipleLocator(2))

        ax.set_axisbelow(True)

        # Remove y-axis
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.yaxis.set_visible(False)  # Remove y-axis

        # Remove ticks
        ax.tick_params(axis="both", which="both", length=0)

        # Adjust the layout
        plt.subplots_adjust(hspace=0)  # Remove space between facet plots

    if save_path:
        # Save the figure
        fig.savefig(save_path, bbox_inches="tight", pad_inches=0, transparent=True)
    else:
        # Return the figure
        return fig
