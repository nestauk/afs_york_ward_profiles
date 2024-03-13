"""This module contains the function to create and download a zip file with ward profiles."""

import streamlit as st
import pandas as pd
import os
import zipfile
import tempfile
from PIL import Image
from afs_york_ward_profiles.pipeline.create_ward_profile import create_ward_profile


# Function to create and download a zip file
def download_zip_file(template_image: Image, filenames: dict, ward_data: pd.DataFrame):
    """Creates a zip file with ward profiles.
    The zip file is then downloaded if the user clicks the download button.

    Args:
        template_image (Image): The template image to be used as a base for the ward profiles.
        filenames (dict): A dictionary with the names of the files to be included in the zip file.
        ward_data (pd.DataFrame): The data to be used to create the ward profiles.

    Returns:
        None
    """
    # Create a temporary directory
    with st.spinner("Creating the zip file..."):
        # Create a temporary directory
        temp_dir = tempfile.TemporaryDirectory()
        # Creating zip file path
        zip_file_path = os.path.join(temp_dir.name, "Ward_Profiles.zip")

        # Creating zip file
        with zipfile.ZipFile(zip_file_path, "w") as zip_file:

            # Create images with custom names inside the temporary directory
            for fname in filenames.keys():
                # Create a temporary file
                with open(os.path.join(temp_dir.name, f"{fname}.png"), "w") as file:
                    # Creating a ward profile
                    ward_series = ward_data[filenames[fname]]
                    image = create_ward_profile(
                        template_image, ward_series, ward_data["York"], filenames[fname]
                    )
                    # Save the modified image to the temporary file
                    image.save(file.name)

                # Adds the file to the zip
                zip_file.write(
                    os.path.join(temp_dir.name, f"{fname}.png"), f"{fname}.png"
                )

    # Display the download button for users to download the zip file
    with open(zip_file_path, "rb") as zip_file_temp:
        st.download_button(
            label="Click to download",
            data=zip_file_temp,
            file_name="Ward_Profiles.zip",
            mime="application/zip",
        )

    # Clean up the temporary directory (deletes the temporary directory and all its contents)
    temp_dir.cleanup()
