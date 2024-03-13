"""This module contains the function to create a Ward deep dive image."""

# Import necessary libraries
from PIL import Image, ImageDraw
import os
import tempfile
import numpy as np

# Import the required functions
from afs_york_ward_profiles.utils.ward_profile_utils import (
    int_or_float,
    percentage_0,
    child_or_children,
    text_york,
    generate_colour_image,
    get_font,
    pivot_text,
)
from afs_york_ward_profiles.pipeline.ward_plots import (
    create_breastfeeding_plot,
    create_gender_gap_plot,
    create_outcomes_plot,
)

# Set the font path
font_path = "afs_york_ward_profiles/app_utils/font/"
font_path_plots = "afs_york_ward_profiles/app_utils/font/Averta-Bold.ttf"


def create_ward_profile(
    template_image: Image, data_series: list, comparator_series: list, name: str
) -> Image:
    """Function to create a Ward deep dive image.

    Args:
        template_image (Image): The template image to be used as a base for the ward profiles.
        data_series (list): The data to be used to create the ward profiles.
        comparator_series (list): The data to be used to compare the ward profiles.
        name (str): The name of the ward.

    Returns:
        Image: The modified image.
    """
    # Create a copy of the template image
    ward_image = template_image.copy()

    # Adding the ward name to the image
    if "&" in name:
        # Split the name into two lines
        title_name = name.split("& ")
        title_name[0] = title_name[0] + "&"
    else:
        title_name = [name]

    if len(title_name) >= 1:
        ward_image = pivot_text(
            image=ward_image,
            xy_start=[325, 0],
            angle=90,
            text=title_name[-1],
            font=get_font("Bold", 130, font_path),
            fill="#0F294A",
            anchor="la",
            paddingx=-10,
            paddingy=20,
        )
    if len(title_name) == 2:
        ward_image = pivot_text(
            image=ward_image,
            xy_start=[162, 0],
            angle=90,
            text=title_name[0],
            font=get_font("Bold", 130, font_path),
            fill="#0F294A",
            anchor="la",
            paddingx=-10,
            paddingy=20,
        )

    draw = ImageDraw.Draw(ward_image)

    # Adding Numbers to the image
    draw.text(
        (485, 77.5),
        int_or_float(data_series[0]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )
    draw.text(
        (855, 77.5),
        int_or_float(data_series[1]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )
    draw.text(
        (1275, 77.5),
        int_or_float(data_series[2]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )
    draw.text(
        (1650, 77.5),
        int_or_float(data_series[3]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )
    draw.text(
        (550, 490),
        int_or_float(data_series[6]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )
    draw.text(
        (1325, 455),
        percentage_0(data_series[8]),
        font=get_font("Bold", 46, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (480, 680),
        int_or_float(round(data_series[11], 1)),
        font=get_font("Bold", 46, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (670, 680),
        percentage_0(data_series[12]),
        font=get_font("Bold", 46, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (680, 830),
        percentage_0(data_series[13]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )

    # Adding text to the image
    # Ward text
    if "&" in name:
        text_name = name.replace("& ", "&\n")
    else:
        text_name = name

    text_list = [
        f"children in\n{text_name}",
        "children took up a\nHealthy Start Voucher",
        "children have 2\nyear old funding",
        "children in the\nSocial Care data",
        "children\nreferred to GP",
    ]
    text_list_wo_children = [
        f"{data_series[4].astype(str)} average IMD decile\nacross LSOAs*",
        "of children are in income deprivation",
        "Community Needs Score***",
        "overweight in\nReception",
        "of residents agree their local area is a good place for children\nand young people to grow up****",
        f"Gender gap** for\n{text_name}",
        "Gender gap for York",
    ]
    text_list = [
        child_or_children(data_series[i], text_list[i]) for i in range(len(text_list))
    ]
    text_list = text_list + text_list_wo_children
    draw.text(
        (500, 77.5),
        text_list[0],
        font=get_font("Regular", 23, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (870, 77.5),
        text_list[1],
        font=get_font("Regular", 23, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (1290, 77.5),
        text_list[2],
        font=get_font("Regular", 23, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (1665, 77.5),
        text_list[3],
        font=get_font("Regular", 23, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (355, 325),
        text_list[5],
        font=get_font("Bold", 23, font_path),
        fill="#0F294A",
        anchor="lm",
        align="center",
    )
    draw.text(
        (880, 250),
        text_name,
        font=get_font("Bold", 23, font_path),
        fill="#0F294A",
        anchor="rm",
        align="center",
    )
    draw.text(
        (1305, 250),
        percentage_0(data_series[5]),
        font=get_font("Bold", 38, font_path),
        fill="#0F294A",
        anchor="mm",
    )
    draw.text(
        (1390, 250),
        text_list[6],
        font=get_font("Regular", 23, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (565, 490),
        text_list[4],
        font=get_font("Regular", 20, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (355, 720),
        text_list[7],
        font=get_font("Regular", 20, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (800, 680),
        text_list[8],
        font=get_font("Regular", 20, font_path),
        fill="#0F294A",
        anchor="lm",
        align="center",
    )
    draw.text(
        (350, 900),
        text_list[9],
        font=get_font("Regular", 20, font_path),
        fill="#0F294A",
        anchor="lm",
        align="center",
    )
    draw.text(
        (980, 455),
        text_list[10],
        font=get_font("Bold", 20, font_path),
        fill="#0F294A",
        anchor="rm",
        align="center",
    )

    # Comparator text
    draw.text(
        (520, 145),
        text_york(comparator_series[0]),
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="mm",
    )
    draw.text(
        (935, 145),
        text_york(comparator_series[1]),
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="mm",
    )
    draw.text(
        (1330, 145),
        text_york(comparator_series[2]),
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="mm",
    )
    draw.text(
        (1705, 145),
        text_york(comparator_series[3]),
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="mm",
    )
    draw.text(
        (880, 330),
        "York",
        font=get_font("Bold", 23, font_path),
        fill="#0F294A",
        anchor="rm",
    )
    draw.text(
        (1305, 330),
        percentage_0(comparator_series[5]),
        font=get_font("Bold", 38, font_path),
        fill="#0F294A",
        anchor="mm",
    )
    draw.text(
        (1390, 330),
        "of children are in income deprivation",
        font=get_font("Regular", 23, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (520, 575),
        text_york(comparator_series[6]),
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="mm",
    )
    draw.text(
        (1345, 535),
        f"low birth weight\nvs {percentage_0(comparator_series[8])} on average for\nYork wards",
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="mm",
        align="center",
    )
    draw.text(
        (720, 725),
        f"vs {percentage_0(comparator_series[12])} for York",
        font=get_font("Regular", 16, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (980, 550),
        text_list[11],
        font=get_font("Bold", 20, font_path),
        fill="#0F294A",
        anchor="rm",
        align="center",
    )

    text_at_bottom = [
        f"*vs {int_or_float(comparator_series[4])} on average across York LSOAs",
        f"** Number of male children - number of female children with WellComm\nRed/Amber or ASQ emerging",
        f"*** vs {int_or_float(comparator_series[11])} for all of York. Comprises of active and engaged community\nscore, civic assets score and connectedness score",
        f"**** vs {percentage_0(comparator_series[13])} for all of York.",
    ]
    # Combined text_at_bottom to one string
    text_at_bottom = "\n".join(text_at_bottom)
    draw.text(
        (330, 950),
        text_at_bottom,
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="la",
    )
    draw.text(
        (1895, 930),
        "Children 0-5",
        font=get_font("Bold", 130, font_path),
        fill="#0F294A",
        anchor="ra",
    )

    # Adding images to the image
    # Add IMD image
    if ~np.isnan(data_series[4]):
        imd_value = round(data_series[4])
        imd_image = Image.open(
            f"afs_york_ward_profiles/app_utils/images/imd/imd_{imd_value}.png"
        )
        ward_image.alpha_composite(imd_image, (410, 210))
    # Add income deprivation image for Ward
    if ~np.isnan(data_series[5]):
        people_value = int(round(data_series[5], -1) / 10)
        people_image = Image.open(
            f"afs_york_ward_profiles/app_utils/images/people_percentage/people_{people_value}.png"
        )
        ward_image.alpha_composite(people_image, (900, 220))
    # Add income deprivation image for comparator
    if ~np.isnan(comparator_series[5]):
        comparator_people_value = int(round(comparator_series[5], -1) / 10)
        comparator_people_image = Image.open(
            f"afs_york_ward_profiles/app_utils/images/people_percentage/people_{comparator_people_value}.png"
        )
        ward_image.alpha_composite(comparator_people_image, (900, 300))

    # Add square colours
    light_blue = generate_colour_image("#00A8C1", (15, 15))
    dark_blue = generate_colour_image("#0F294A", (15, 15))
    ward_image.paste(light_blue, (1540, 430))
    ward_image.paste(dark_blue, (1540, 410))
    # Text for the Breastfeeding image
    draw.text(
        (1570, 417),
        "Totally breastfeeding",
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (1570, 437),
        "Totally/partially breastfeeding",
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (1600, 590),
        text_name,
        font=get_font("Bold", 15, font_path),
        fill="#0F294A",
        anchor="mm",
        align="center",
    )
    draw.text(
        (1765, 590),
        "York",
        font=get_font("Bold", 15, font_path),
        fill="#0F294A",
        anchor="mm",
        align="center",
    )
    # Add bar charts
    image_dir = tempfile.TemporaryDirectory()
    # Add gender bar chart
    if np.isnan(data_series[7]) and np.isnan(comparator_series[7]):
        draw.text(
            (1100, 500),
            "Ward and York\ndata unavailable",
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )
    elif np.isnan(data_series[7]):
        draw.text(
            (1100, 500),
            "Ward data\nunavailable",
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )
    elif np.isnan(comparator_series[7]):
        draw.text(
            (1100, 500),
            "York data\nunavailable",
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )
    else:
        with open(os.path.join(image_dir.name, f"gender.png"), "w") as gender_file:
            create_gender_gap_plot(
                data_series=data_series,
                comparator_series=comparator_series,
                name=name,
                index=7,
                font_path=font_path_plots,
                font_size=18,
                save_path=gender_file.name,
            )

        gender_image = Image.open(os.path.join(image_dir.name, f"gender.png"))
        ward_image.alpha_composite(gender_image, (990, 410))

    # Add breastfeeding bar chart
    if any(np.isnan(x) for x in data_series[9:11]) and any(
        np.isnan(x) for x in comparator_series[9:11]
    ):
        draw.text(
            (1670, 530),
            "Ward and York\ndata unavailable",
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )
    elif any(np.isnan(x) for x in data_series[9:11]):
        draw.text(
            (1670, 530),
            "Ward data\nunavailable",
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )
    elif any(np.isnan(x) for x in comparator_series[9:11]):
        draw.text(
            (1670, 530),
            "York data\nunavailable",
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )
    else:
        with open(
            os.path.join(image_dir.name, f"breastfeeding.png"), "w"
        ) as breastfeeding_file:
            create_breastfeeding_plot(
                data_series=data_series,
                comparator_series=comparator_series,
                name=name,
                index_list=[9, 10],
                font_path=font_path_plots,
                font_size=16,
                fig_size=(3.5, 1.5),
                save_path=breastfeeding_file.name,
            )
        breastfeeding_image = Image.open(
            os.path.join(image_dir.name, f"breastfeeding.png")
        )
        ward_image.alpha_composite(breastfeeding_image, (1525, 450))

    # Add outcomes bar chart
    if any(np.isnan(x) for x in data_series[14:18]) and any(
        np.isnan(x) for x in comparator_series[14:18]
    ):
        draw.text(
            (1520, 795),
            "Ward and York\ndata unavailable",
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )
    elif any(np.isnan(x) for x in data_series[14:18]):
        draw.text(
            (1520, 795),
            "Ward data\nunavailable",
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )
    elif any(np.isnan(x) for x in comparator_series[14:18]):
        draw.text(
            (1520, 795),
            "York data\nunavailable",
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )
    else:
        with open(os.path.join(image_dir.name, f"outcomes.png"), "w") as outcomes_file:
            create_outcomes_plot(
                data_series=data_series,
                comparator_series=comparator_series,
                name=name,
                font_path=font_path_plots,
                font_size=12,
                fig_size=(8, 3),
                save_path=outcomes_file.name,
            )
        outcomes_image = Image.open(os.path.join(image_dir.name, f"outcomes.png"))
        ward_image.alpha_composite(outcomes_image, (1270, 670))
    # Close the temporary directory
    image_dir.cleanup()

    # Adding outcomes text
    outcomes_text = [
        "ASQ 9-12 C&L emerging",
        "ASQ 24-30 C&L emerging",
        "WellComm (Red/Amber)",
        "Not meeting expectations\n(disadvantaged)",
    ]
    for i, text in enumerate(outcomes_text):
        draw.text(
            (1120, 695 + i * 58),
            text,
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )

    return ward_image
