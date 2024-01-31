import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Random Data Collector Portal")
st.markdown("Note : This is an Sample Data Collector for Traffic Load Checking ")
st.markdown("Enter the details in the below given Fields : ")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="RandomData", usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")

# List of Business Types and Products
YearofStudy = [
    1,
    2,
    3,
    4
 
]
Skills = [
    "Python",
    "Machine Learning",
    "Excel",
    "C",
    "Cloud",
    "Java",
    "IOT"
]

# Onboarding New Vendor Form
with st.form(key="student_form"):
    student_name = st.text_input(label="Student Name*")
    year_of_study = st.selectbox("Year of Study*", options=YearofStudy, index=None)
    skills = st.multiselect("Skill Set", options=Skills)
    projects_count = st.slider("Projects Done Count", 0, 50, 5)
    date_of_submission = st.date_input(label="Date of Submission")
    remarks = st.text_area(label="Additional Notes")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit Student Details")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not year_of_study or not skills:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        # elif existing_data["CompanyName"].str.contains(company_name).any():
        #     st.warning("A vendor with this company name already exists.")
        #     st.stop()
        else:
            # Create a new row of vendor data
            student_data = pd.DataFrame(
                [
                    {
                        "Name": student_name,
                        "YearofStudy": year_of_study,
                        "Skills": ", ".join(skills),
                        "ProjectCount": projects_count,
                        "DOS": date_of_submission.strftime("%d-%m-%y"),
                        "Remarks": remarks,
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, student_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="RandomData", data=updated_df)

            st.success("Student details successfully submitted!")
