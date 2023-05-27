from fillpdf import fillpdfs
import streamlit as st
from io import BytesIO
from datetime import datetime
import base64

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%m/%d/%Y")

st.subheader("SAMC FM RESIDENCY FEEDBACK/INCIDENT FORM")
st.markdown("<mark style='background-color: yellow'>Contact the Program Director or DIO for urgent/emergent matters. Do not use this form!</mark><br><span style='color: red'>NOTE: This site does NOT gather any user data</span>", unsafe_allow_html=True)
st.markdown("""
    1. Fill out each field 
    2. Click Generate Form
    3. Get download link
    4. Print/Save locally
    5. Remember to drop it off in Feedback Box (Rounding Room)
            """, unsafe_allow_html=True)

filing_date = st.date_input('Filing Date', datetime.now(), disabled=True)
incident_date = st.date_input('Incident Date', max_value=current_datetime)

privacy_level = st.selectbox("Privacy Level", index=0, options=('Choose an item', 'Anonymous', 'Non-Anonymous'))

name = ''
if privacy_level == 'Non-Anonymous':
    name = st.text_input("Name (only if non-anonymous)")

feedback = st.selectbox(label="Feedback/Incident Type", index=0,  
                        options=('Choose an item', 
                                 'Rotation Feedback',
                                 'Faculty Feedback',
                                 'Medical Student Feedback',
                                 'Nursing Staff Feedback',
                                 'General Residency Feedback',
                                 'Disruptive Behavior',
                                 'Unprofessional Conduct',
                                 'Safety Concern',
                                 'Resource Failure',
                                 'Scheduling'
                                 ))
position = st.selectbox(label='Position', index=0,
                        options=('Choose an item',
                                'Resident',
                                'Faculty',
                                'Medical Student',
                                'Support Staff',
                                'Elect not to say'))
description = st.text_area(label='Narrative/Description', max_chars=900)
if privacy_level == 'Anonymous':
    disposition = st.selectbox(label="**Disposition**", 
        index=0, 
        options=('Choose an item',
                'I only want to report and desire no direct follow-up',
                'I want the DIO to be notified, but request no follow-up'
                ))
else:
    disposition = st.selectbox(label="**Disposition**", 
        index=0, 
        options=('Choose an item',
                'I want PD to contact me (Non-anonymous submissions only)',
                'I want my advisor to contact me (Non-anonymous submissions only)',
                'I want the DIO to be notified and request follow-up (Non-Anonymous submissions only)',
                'I would like the chief resident to contact me (Non-anonymous submissions only)',
                'I would like the program coordinator to contact me (Non-anonymous submissions only)',
                'I would like the Director of GME (DGME) to contact me (Non-anonymous submissions only)'))

print(name)
# file path input
input_pdf_path = 'pdf_feedback_form.pdf'

get_field = fillpdfs.get_form_fields("pdf_feedback_form.pdf")

get_field['filing_field'] = filing_date.strftime('%m/%d/%Y')
get_field['incident_field'] = incident_date.strftime('%m/%d/%Y')
get_field['privacy_field'] = privacy_level
get_field['name_field'] = name
get_field['feedback_field'] = feedback
get_field['position_field'] = position
get_field['describe_field'] = description
get_field['disposition_field'] = disposition

print(get_field)

#fill the PDF form and save output to memory
output_pdf_data = BytesIO()
fillpdfs.write_fillable_pdf(input_pdf_path, output_pdf_data, get_field, flatten=True)
output_pdf_data.seek(0) # Reset the stream position to 0

# Create a download link
def create_download_link(val, filename):
    b64_pdf_data = base64.b64encode(val.getvalue()).decode()
    return f'<a href="data:application/pdf;base64,{b64_pdf_data}" download="{filename}.pdf">Download Filled PDF</a>'

#create form validation list
form_valid_list = {'Privacy Level': privacy_level, 'Feedback/Incident Type': feedback, 'Position': position, 'Narrative/Description': description, 'Disposition': disposition}

export_pdf = st.button("Generate PDF")
if export_pdf:
    is_valid = True 
    for key, value in form_valid_list.items():
        if value == 'Choose an item' or value =='':
            is_valid = False
            st.error(f"Please select/complete: {key}")
    if privacy_level == 'Non-Anonymous':
        if name == '':
            is_valid = False
            st.error("Please enter your name")
    if is_valid:
        html = create_download_link(output_pdf_data, "completed_form")
        st.markdown(html, unsafe_allow_html=True)

