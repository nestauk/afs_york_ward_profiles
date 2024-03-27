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
    data_unavailable,
)
from afs_york_ward_profiles.pipeline.ward_plots import (
    create_gender_gap_plot,
    create_hospital_maternity_plot,
    create_breastfeeding_plot,
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

    ### Lists of text to add to the image

    # Ward text
    if "&" in name:
        text_name = name.replace("& ", "&\n")
    else:
        text_name = name

    text_list = [
        f"children in\n{text_name}",
        "children took up\na Healthy Start\nVoucher",
        "children have\n2 year old\nfunding",
        "children are\neligible for FSM",
        "children in the\nSocial Care\ndata",
        "children have\nan EHCP",
        "children have\nan S23",
        "children referred\nto GP***",
    ]
    text_list_wo_children = [
        "of children are in\nincome deprivation",
        f"Gender gap* for\n{text_name}",
        "Gender gap for\nYork",
        f"{data_series[12]} average IMD decile\nacross LSOAs**",
        "overweight in\nReception",
        "of residents agree their local area is a good place for children\nand young people to grow up****",
    ]
    text_list = [
        child_or_children(data_series[i], text_list[i]) for i in range(len(text_list))
    ]
    text_list = text_list + text_list_wo_children

    ### Adding Information by box

    ## (1) Number of children
    # Number
    draw.text(
        (450, 77.5),
        int_or_float(data_series[0]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )
    # Text
    draw.text(
        (465, 77.5),
        text_list[0],
        font=get_font("Regular", 21, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    # Comparator text
    draw.text(
        (475, 145),
        text_york(comparator_series[0], split=True),
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="mm",
        align="center",
    )

    # (2) Number of children with Healthy Start Voucher
    # Number
    draw.text(
        (750, 77.5),
        int_or_float(data_series[1]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )
    # Text
    draw.text(
        (765, 77.5),
        text_list[1],
        font=get_font("Regular", 21, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    # Comparator text
    draw.text(
        (790, 145),
        text_york(comparator_series[1], split=True),
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="mm",
        align="center",
    )

    # (3) Number of children with 2 year old funding
    # Number
    draw.text(
        (1080, 77.5),
        int_or_float(data_series[2]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )

    # Text
    draw.text(
        (1095, 77.5),
        text_list[2],
        font=get_font("Regular", 21, font_path),
        fill="#0F294A",
        anchor="lm",
    )

    # Comparator text
    draw.text(
        (1105, 145),
        text_york(comparator_series[2], split=True),
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="mm",
        align="center",
    )

    # (4) Number of children eligible for FSM
    # Number
    draw.text(
        (1370, 77.5),
        int_or_float(data_series[3]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )

    # Text
    draw.text(
        (1395, 77.5),
        text_list[3],
        font=get_font("Regular", 21, font_path),
        fill="#0F294A",
        anchor="lm",
    )

    # Comparator text
    draw.text(
        (1420, 145),
        text_york(comparator_series[3], split=True),
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="mm",
        align="center",
    )

    # (5) Number of children in Social Care data
    # Number
    draw.text(
        (1700, 77.5),
        int_or_float(data_series[4]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )

    # Text
    draw.text(
        (1715, 77.5),
        text_list[4],
        font=get_font("Regular", 21, font_path),
        fill="#0F294A",
        anchor="lm",
    )

    # Comparator text
    draw.text(
        (1735, 145),
        text_york(comparator_series[4], split=True),
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="mm",
        align="center",
    )

    # (6) Number of children with an EHCP
    # Number
    draw.text(
        (450, 255),
        int_or_float(data_series[5]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )

    # Text
    draw.text(
        (465, 255),
        text_list[5],
        font=get_font("Regular", 21, font_path),
        fill="#0F294A",
        anchor="lm",
        align="center",
    )

    # Comparator text
    draw.text(
        (480, 325),
        text_york(comparator_series[5], split=True),
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="mm",
        align="center",
    )

    # (7) Number of children with an S23
    # Number
    draw.text(
        (750, 255),
        int_or_float(data_series[6]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )

    # Text
    draw.text(
        (765, 255),
        text_list[6],
        font=get_font("Regular", 21, font_path),
        fill="#0F294A",
        anchor="lm",
        align="center",
    )

    # Comparator text
    draw.text(
        (790, 325),
        text_york(comparator_series[6], split=True),
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="mm",
        align="center",
    )

    # (8) Children income deprivation
    # Number
    draw.text(
        (1555, 250),
        percentage_0(data_series[7]),
        font=get_font("Bold", 38, font_path),
        fill="#0F294A",
        anchor="mm",
    )
    draw.text(
        (1555, 330),
        percentage_0(comparator_series[7]),
        font=get_font("Bold", 38, font_path),
        fill="#0F294A",
        anchor="mm",
    )
    # Text
    draw.text(
        (1130, 250),
        text_name,
        font=get_font("Bold", 21, font_path),
        fill="#0F294A",
        anchor="rm",
        align="center",
    )
    draw.text(
        (1130, 330),
        "York",
        font=get_font("Bold", 23, font_path),
        fill="#0F294A",
        anchor="rm",
    )
    draw.text(
        (1630, 290),
        text_list[8],
        font=get_font("Regular", 23, font_path),
        fill="#0F294A",
        anchor="lm",
    )

    # Add income deprivation image for Ward
    if ~np.isnan(data_series[7]):
        people_value = int(round(data_series[7], -1) / 10)
        people_image = Image.open(
            f"afs_york_ward_profiles/app_utils/images/people_percentage/people_{people_value}.png"
        )
        ward_image.alpha_composite(people_image, (1150, 220))
    # Add income deprivation image for comparator
    if ~np.isnan(comparator_series[7]):
        comparator_people_value = int(round(comparator_series[7], -1) / 10)
        comparator_people_image = Image.open(
            f"afs_york_ward_profiles/app_utils/images/people_percentage/people_{comparator_people_value}.png"
        )
        ward_image.alpha_composite(comparator_people_image, (1150, 300))

    # (9) Gender gap
    # Text
    draw.text(
        (500, 455),
        text_list[9],
        font=get_font("Bold", 20, font_path),
        fill="#0F294A",
        anchor="rm",
        align="center",
    )
    draw.text(
        (500, 550),
        text_list[10],
        font=get_font("Bold", 20, font_path),
        fill="#0F294A",
        anchor="rm",
        align="center",
    )

    # (10) Teenage pregnancy, birth weight, and smoking
    # Add square colours
    light_blue = generate_colour_image("#97D9E3", (15, 15))
    medium_blue = generate_colour_image("#00A8C1", (15, 15))
    dark_blue = generate_colour_image("#0F294A", (15, 15))
    ward_image.paste(light_blue, (875, 430))
    ward_image.paste(medium_blue, (980, 410))
    ward_image.paste(dark_blue, (760, 410))
    # Text for the Breastfeeding image
    draw.text(
        (790, 417),
        "Teenage pregnancy",
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (1010, 417),
        "Low birth weight",
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (905, 437),
        "Mother smoking",
        font=get_font("Regular", 18, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    draw.text(
        (855, 590),
        text_name,
        font=get_font("Bold", 15, font_path),
        fill="#0F294A",
        anchor="mm",
        align="center",
    )
    draw.text(
        (1065, 590),
        "York",
        font=get_font("Bold", 15, font_path),
        fill="#0F294A",
        anchor="mm",
        align="center",
    )
    # (11) Average IMD decile
    # Text
    draw.text(
        (1450, 555),
        text_list[11],
        font=get_font("Bold", 20, font_path),
        fill="#0F294A",
        anchor="rm",
        align="center",
    )
    # Add IMD image
    if ~np.isnan(data_series[12]):
        imd_value = round(data_series[12])
        imd_image = Image.open(
            f"afs_york_ward_profiles/app_utils/images/imd/imd_{imd_value}.png"
        )
        ward_image.alpha_composite(imd_image, (1275, 430))

    # (12) Breastfeeding
    # Add square colours
    ward_image.paste(medium_blue, (1540, 430))
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

    # (13) Referral to GP
    # Number
    draw.text(
        (490, 680),
        int_or_float(round(data_series[15], 1)),
        font=get_font("Bold", 46, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    # Text
    draw.text(
        (445, 730),
        text_list[7],
        font=get_font("Regular", 20, font_path),
        fill="#0F294A",
        anchor="lm",
        align="center",
    )

    # (14) Overweight in reception
    # Number
    draw.text(
        (670, 680),
        percentage_0(data_series[16]),
        font=get_font("Bold", 46, font_path),
        fill="#0F294A",
        anchor="lm",
    )

    # Text
    draw.text(
        (800, 680),
        text_list[12],
        font=get_font("Regular", 20, font_path),
        fill="#0F294A",
        anchor="lm",
        align="center",
    )

    draw.text(
        (720, 735),
        f"vs {percentage_0(comparator_series[16])} for York",
        font=get_font("Regular", 16, font_path),
        fill="#0F294A",
        anchor="lm",
    )
    # (15) Local area good for children
    # Number
    draw.text(
        (680, 830),
        percentage_0(data_series[17]),
        font=get_font("Bold", 65, font_path),
        fill="#0F294A",
        anchor="rm",
    )
    # Text
    draw.text(
        (340, 900),
        text_list[13],
        font=get_font("Regular", 20, font_path),
        fill="#0F294A",
        anchor="lm",
        align="center",
    )

    # (16-20) Outcomes
    # Adding outcomes text
    outcomes_text = [
        "ASQ 9-12 C&L emerging",
        "ASQ 24-30 C&L emerging",
        "WellComm (Red/Amber)",
        "EYFSP emerging",
        "Not meeting expectations\n(disadvantaged)",
    ]
    for i, text in enumerate(outcomes_text):
        draw.text(
            (1100, 690 + i * 47),
            text,
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )

    # Adding images to the image
    # Add bar charts
    image_dir = tempfile.TemporaryDirectory()
    # Add gender bar chart
    gender_value = data_unavailable(
        draw=draw,
        data_series=data_series,
        comparator_series=comparator_series,
        font_path=font_path,
        index=(7, 8),
        coordinates=(600, 500),
    )
    if gender_value:
        with open(os.path.join(image_dir.name, f"gender.png"), "w") as gender_file:
            create_gender_gap_plot(
                data_series=data_series,
                comparator_series=comparator_series,
                name=name,
                index=8,
                font_path=font_path_plots,
                font_size=18,
                save_path=gender_file.name,
            )

        gender_image = Image.open(os.path.join(image_dir.name, f"gender.png"))
        ward_image.alpha_composite(gender_image, (510, 410))

    # Add maternity bar chart
    maternity_value = data_unavailable(
        draw=draw,
        data_series=data_series,
        comparator_series=comparator_series,
        font_path=font_path,
        index=(9, 12),
        coordinates=(950, 500),
    )

    if maternity_value:
        with open(
            os.path.join(image_dir.name, f"maternity.png"), "w"
        ) as maternity_file:
            create_hospital_maternity_plot(
                data_series=data_series,
                comparator_series=comparator_series,
                name=name,
                index_list=[9, 10, 11],
                font_path=font_path_plots,
                font_size=14,
                fig_size=(4.5, 1.5),
                save_path=maternity_file.name,
            )
        maternity_image = Image.open(os.path.join(image_dir.name, f"maternity.png"))
        ward_image.alpha_composite(maternity_image, (750, 450))

    # Add breastfeeding bar chart
    breastfeeding_value = data_unavailable(
        draw=draw,
        data_series=data_series,
        comparator_series=comparator_series,
        font_path=font_path,
        index=(13, 15),
        coordinates=(1670, 530),
    )

    if breastfeeding_value:
        with open(
            os.path.join(image_dir.name, f"breastfeeding.png"), "w"
        ) as breastfeeding_file:
            create_breastfeeding_plot(
                data_series=data_series,
                comparator_series=comparator_series,
                name=name,
                index_list=[13, 14],
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
    outcomes_value = data_unavailable(
        draw=draw,
        data_series=data_series,
        comparator_series=comparator_series,
        font_path=font_path,
        index=(19, 24),
        coordinates=(1520, 795),
    )
    if outcomes_value:
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
        ward_image.alpha_composite(outcomes_image, (1250, 670))

    # Close the temporary directory
    image_dir.cleanup()

    # Text at the bottom of the image
    text_at_bottom = [
        f"* Number of male children - number of female children with WellComm\nRed/Amber or ASQ emerging.",  # Gender gap
        f"**vs {int_or_float(comparator_series[12])} on average across York LSOAs.",  # IMD
        f"*** vs {int_or_float(comparator_series[15])} for all of York.",  # Referral to GP
        f"**** vs {percentage_0(comparator_series[17])} for all of York.",  # Local area good for children
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

    return ward_image
