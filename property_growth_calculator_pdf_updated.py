
import streamlit as st
import pandas as pd
import PyPDF2
import re

# Title of the app
st.title("Property Value Growth Calculator")

# Instructions
st.write("Upload a **PDF** file containing capital growth rates and enter the property details.")

# File upload for PDF suburb report
uploaded_pdf = st.file_uploader("Upload a PDF file with capital growth rates", type=["pdf"])

def extract_growth_rates_from_pdf(pdf_file):
    """Extracts growth rates from the uploaded PDF."""
    growth_rates = []
    years = []
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text = page.extract_text()
        matches = re.findall(r"Jan (\d{4})\s+(-?\d+\.\d+)%", text)  # Extracts year and percentage
        for match in matches:
            year, rate = match
            years.append(int(year))
            growth_rates.append(float(rate) / 100)  # Convert percentage to decimal

    return years, growth_rates

if uploaded_pdf is not None:
    # Extract growth rates and years from PDF
    years, growth_rates = extract_growth_rates_from_pdf(uploaded_pdf)

    if growth_rates and years:
        max_year = max(years)  # Get the latest year available in the PDF

        # User input: Purchase year (limited to the available years in PDF)
        purchase_year = st.number_input(
            "Enter the year the property was bought:",
            min_value=min(years), 
            max_value=max_year, 
            value=min(years), 
            step=1
        )

        # User input: Initial property value
        initial_value = st.number_input("Enter the initial property value ($):", min_value=0.0, value=200000.0, step=1000.0)

        # Dataframe for calculations
        data = {"Year": [], "Property Value ($)": []}

        # Perform calculations starting from the purchase year
        current_value = initial_value
        for i, rate in enumerate(growth_rates[: (max_year - purchase_year) + 1]):
            year = purchase_year + i
            current_value *= (1 + rate)
            data["Year"].append(year)
            data["Property Value ($)"].append(round(current_value, 2))

        # Convert to DataFrame
        result_df = pd.DataFrame(data)

        # Display results
        st.write("### Growth Over Time:")
        st.dataframe(result_df)

        # Plot the data
        st.line_chart(result_df.set_index("Year"))

        st.success(f"Calculation completed successfully! (Max Year: {max_year})")

    else:
        st.error("No growth rates found in the uploaded PDF. Please check the file format.")

else:
    st.info("Please upload a PDF file with capital growth rates to proceed.")
