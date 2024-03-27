# Description: Utility functions for the ward profile report.

# Importing the required libraries
import math
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import pandas as pd


def generate_colour_image(hex_code, size) -> Image:
    """Generates a random image with a given hex code and size.

    Args:
        hex_code (str): The hex code for the color of the image.
        size (tuple): The size of the image (width, height).

    Returns:
        PIL.Image.Image: The generated random image.
    """

    # Generate a square of color
    grid = np.array([[hex_to_rgb(hex_code)]], dtype="uint8")

    # Make into PIL Image and scale up using Nearest Neighbour
    im = Image.fromarray(grid).resize(size, resample=Image.NEAREST)

    return im


def pivot_text(
    image: Image,
    xy_start: list,
    angle: int,
    text: str,
    font: ImageFont,
    fill: str = "#0F294A",
    anchor: str = "lt",
    paddingx: int = 0,
    paddingy: int = 0,
) -> Image:
    """Function to pivot text on an image.

    Args:
        image (Image): The image to be modified.
        xy_start (list): The starting point of the text which are the coordinates of the top right corner of the rectangle.
        angle (int): The angle to pivot the text.
        text (str): The text to be added.
        font (ImageFont): The font to be used.
        fill (str, optional): The colour of the text. Defaults to '#0F294A'.
        anchor (str, optional): The anchor of the text. Defaults to 'lt'.
        paddingx (int, optional): The padding on the x axis. Defaults to 0.
        paddingy (int, optional): The padding on the y axis. Defaults to 0.

    Returns:
        Image: The modified image.
    """

    image = image.copy()
    # Measure the text area
    width_ = font.getbbox(text)[2]
    height_ = font.getbbox(text)[3]
    # Copy the relevant area from the source image
    position = (
        xy_start[0] - height_ + paddingx,
        xy_start[1] + paddingy,
        xy_start[0] + paddingx,
        xy_start[1] + paddingy + width_,
    )
    img = image.crop(position)
    # Rotate it backwards
    img = img.rotate(360 - angle, expand=1)

    # Print into the rotated area
    pivot_image = ImageDraw.Draw(img)
    pivot_image.text((0, 0), text, font=font, fill=fill, anchor=anchor)

    # Rotate it forward again
    img = img.rotate(angle, expand=1)

    # Insert it back into the initial image
    image.paste(img, position)

    return image


# Set up font objects
def get_font(font_style: str, size: int, font_path: str) -> ImageFont:
    """Function to get an Averta font object.

    Args:
        font_style (str): The style of the font. Options are Bold or Regular.
        size (int): The size of the font.
        font_path (str): The path to the font file.

    Returns:
        ImageFont: The font object.
    """
    return ImageFont.truetype(f"{font_path}Averta-{font_style}.ttf", size)


def child_or_children(number: float, text: str) -> str:
    """Function to return child or children depending on the number of children.
    The text must default to have the word children with the correct grammar for have/are.

    Args:
        number (int): The number of children.
        text (str): The text to be modified.

    Returns:
        str: The modified text.
    """
    if "children" in text:
        if number == 1:
            if "children have" in text:
                text = text.replace("children have", "child has")
            if "children are" in text:
                text = text.replace("children are", "child is")
            text = text.replace("children", "child")
        return text


def int_or_float(number: float) -> str:
    """Function to return an integer or a float as a string.

    Args:
        number (float): The number to be converted to a string.

    Returns:
        str: The number as a string.
    """
    if math.isnan(number):
        return ""
    elif math.floor(number) == 0:
        if number == 0:
            return "0"
        else:
            return str(number)
    elif number % math.floor(number) == 0:
        return str(int(number))
    else:
        return str(number)


def hex_to_rgb(hex_code) -> list:
    """Converts a hex code to RGB.

    Args:
        hex_code (str): The hex code to convert.

    Returns:
        list: The RGB values as a tuple.
    """
    hex_code = hex_code.lstrip("#")
    return list(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))


def percentage_0(number: float, decimal: int = 1) -> str:
    """Function to round and return the percentage as a string.

    Args:
        number (float): The number to be converted to a percentage.

    Returns:
        str: The percentage as a string.
    """
    round_number = round(number, decimal)
    return int_or_float(round_number) + "%"


def text_york(
    number: float, percentage: bool = False, decimal: int = 1, split: bool = False
) -> str:
    """Function to return the text for the York average.

    Args:
        number (float): The number to be used in the text.

    Returns:
        str: The text for the York average.
    """
    if percentage:
        text_york = f"vs {percentage_0(number)} on average for York wards"
    else:
        text_york = (
            f"vs {int_or_float(round(number,decimal))} on average for York wards"
        )

    # Split into two lines separated by a space between York and wards
    if split:
        text_york = text_york.replace("York wards", "York\nwards")

    return text_york


def data_unavailable(
    draw: ImageDraw,
    data_series: pd.Series,
    comparator_series: pd.Series,
    font_path: str,
    index: tuple,
    coordinates: tuple,
):
    """Function to add text to the image if data is unavailable.

    Args:
        draw (ImageDraw): The ImageDraw object.
        data_series (pd.Series): The data series.
        comparator_series (pd.Series): The comparator series.
        font_path (str): The path to the font file.
        index (tuple): The index of the data.
        coordinates (tuple): The coordinates for the text.

    Returns:

    """
    if any(np.isnan(x) for x in data_series[index[0] : index[1]]) and any(
        np.isnan(x) for x in comparator_series[index[0] : index[1]]
    ):
        draw.text(
            coordinates,
            "Ward and York\ndata unavailable",
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )
        data_available = False
    elif any(np.isnan(x) for x in data_series[index[0] : index[1]]):
        draw.text(
            coordinates,
            "Ward data\nunavailable",
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )
        data_available = False
    elif any(np.isnan(x) for x in comparator_series[index[0] : index[1]]):
        draw.text(
            coordinates,
            "York data\nunavailable",
            font=get_font("Bold", 18, font_path),
            fill="#0F294A",
            anchor="mm",
            align="center",
        )
        data_available = False
    else:
        data_available = True

    return data_available
