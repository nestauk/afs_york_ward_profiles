from afs_york_ward_profiles import streamlit_config, PROJECT_DIR
from afs_york_ward_profiles.utils.processing import preprocess_strings
from afs_york_ward_profiles.utils.download_zip_file import download_zip_file
from afs_york_ward_profiles.pipeline.create_ward_profile import create_ward_profile
import streamlit as st
from PIL import Image
import pandas as pd
import tempfile

colours = streamlit_config["nesta_colours"]

# INSERT THE TITLE OF YOUR APP HERE
APP_TITLE = "York Ward Deep Dives"

# icon to be used as the favicon on the browser tab
im = Image.open("afs_york_ward_profiles/app_utils/images/favicon.ico")

# sets page configuration with favicon and title specified on line 4
st.set_page_config(page_title=APP_TITLE, layout="wide", page_icon=im)

header = st.container()
with header:
    # nesta logo
    nesta_logo = Image.open(f"afs_york_ward_profiles/app_utils/images/nesta_logo.png")

    # set title of app to be title specified
    st.title(APP_TITLE)
    # Indicate that this dashboard is still a draft. Remove once final.
    st.markdown(
        "This dashboard is designed for York to use internally to create Enhanced Ward Profiles relevant to children aged 0-5. These images provide a snapshot of the demographic and socio-economic characteristics of a ward in York amd provides a comparison with the York average."
    )
    st.write(
        "Please note if this is taking a long time to load, make sure the download the zip file option is No."
    )

tab1, tab2, tab3 = st.tabs(
    ["Creating the Ward Profiles", "About the Ward Profile", "How to create the data"]
)

with tab1:
    st.write(
        "This tab allows the use to upload their data to create the Ward Profile. The user can view each ward profile, as well as download all of the Ward deep dives in a zip file."
    )
    # Uploading the data
    uploaded_file = st.file_uploader("Upload csv with Ward data", type=["csv"])
    ward_data = None
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        # Process the uploaded file here
        ward_data = pd.read_csv(uploaded_file, encoding="latin-1")
    else:
        st.write("No csv uploaded! Please upload a csv file.")

    # Load the template image
    template_image = Image.open("afs_york_ward_profiles/app_utils/images/template.png")

    if ward_data is not None:
        # Create a select box with the York wards
        selected_ward = st.selectbox(
            "Select or type a York ward", streamlit_config["york_wards"]
        )
        ward_file_names = preprocess_strings(pd.Series(streamlit_config["york_wards"]))
        ward_series = ward_data[selected_ward]

        # Create a temporary file to draw on the image
        with tempfile.NamedTemporaryFile(suffix=".png") as temp:
            ward_image = create_ward_profile(
                template_image, ward_series, ward_data["York"], selected_ward
            )
            # Save the modified image to the temporary file
            ward_image.save(temp.name)

            # Resize the image
            ward_image = Image.open(temp.name)
            ward_image = ward_image.resize((1280, 720))

            # Display the image
            st.image(ward_image, use_column_width="auto")
        # Close the temporary file
        temp.close()

    # Check if ward_data is not None
    if ward_data is not None:
        # Create a download button for the zip file
        download_data = st.selectbox(
            "Do you wish to download all of the Ward deep dives?",
            ["Yes", "No"],
            index=1,
        )
        if download_data == "Yes":
            dict_filenames = dict(zip(ward_file_names, streamlit_config["york_wards"]))
            download_zip_file(template_image, dict_filenames, ward_data)

with tab2:
    st.image(
        "afs_york_ward_profiles/app_utils/images/explainer.png",
        use_column_width="auto",
    )
    # About the Ward Profile
    st.write(
        "The image above shows the layout for the Ward profiles. For more detail on the layout, select a number below to give more information."
    )
    # Create a select box with the numbers
    selected_number = st.selectbox(
        "Select or type a number:", [f"{i+1}" for i in range(18)]
    )

    # Load the csv file with the information
    layout_info = pd.read_csv("afs_york_ward_profiles/app_utils/layout_information.csv")

    # Display the information
    split_explanation = layout_info.iloc[int(selected_number) - 1]["Explanation"].split(
        "\n "
    )
    for i in split_explanation:
        st.write(i)

with tab3:
    st.write(
        "This tab provides the user with information on how to create the data for the Ward Profile."
    )
    # How to create the data
    st.write(
        "To create the data for the Ward Profile, the user needs to have a csv file with the York and York wards as columns. Then the data can be input using the number for the rows based on the explanation sheet in the About the data tab. To avoid mismatches in Ward name strings, the user can download a template csv file to fill in to create the Ward Profile."
    )

    # Load the template csv file
    template_data = pd.read_csv(
        "afs_york_ward_profiles/app_utils/ward_template.csv",
        encoding="latin-1",
    )
    # How to create the data
    st.write(
        "To create the data for the Ward Profile, the user needs to have a csv file with the York average and the York wards as columns."
    )
    st.dataframe(template_data.head(5))
    st.write(
        "Then the data can be input using the explanation sheet in the About the data ta with the numbers in the sheet referring to the Number column."
    )
    st.write(
        "To avoid mismatches in Ward name strings, please download a template csv file to fill in order to create the Ward Profile."
    )

    # Create a download button for the csv file
    download_csv = st.selectbox(
        "Do you wish to download the template csv file to create the Ward Profile?",
        ["Yes", "No"],
        index=1,
    )
    if download_csv == "Yes":
        # Create the csv file
        st.download_button(
            label="Click here",
            data=template_data.to_csv(index=False).encode("utf-8"),
            file_name="ward_template.csv",
            mime="text/csv",
        )

    st.write(
        "If the user wishes to create the Ward Profile using dummy data, they can download the csv file below. You can then use this csv file in the Creating the Ward Profiles tab."
    )
    st.write(
        "**Please note** that the dummy data is not representative of the York wards and has been generated using a normal distribution."
    )

    download_csv_dummy = st.selectbox(
        "Do you wish to download the dummy csv file to create the Ward Profile?",
        ["Yes", "No"],
        index=1,
    )
    if download_csv_dummy == "Yes":
        # Create the csv file
        dummy_data = (
            pd.read_csv(
                "afs_york_ward_profiles/app_utils/ward_dummy_data.csv",
                encoding="latin-1",
            )
            .to_csv(index=False)
            .encode("utf-8")
        )
        st.download_button(
            label="Click here",
            data=dummy_data,
            file_name="ward_dummy_data.csv",
            mime="text/csv",
        )

    st.write("For any queries, please contact:")
    st.markdown(
        "  **website:** https://www.york.gov.uk/ **| website:** https://www.nesta.org/ **| email:** jess.gillam@nesta.org.uk **| email:** rachel.wilcock@nesta.org.uk "
    )
