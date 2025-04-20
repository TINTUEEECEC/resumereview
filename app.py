from dotenv import load_dotenv
load_dotenv()
import io
import base64
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(upload_file):
    if upload_file is not None:
        images = pdf2image.convert_from_bytes(upload_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{

            "mime_type":"image/jpeg",
            "data":base64.b64encode(img_byte_arr).decode()

        }]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="ATS Review", layout="wide")
st.header("ATS Review system")
input_text = st.text_area("JD:", key = "input")
uploaded_file = st.file_uploader("upload your resume", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1 = st.button("Tell me about the Resume")
 
submit2 = st.button("percentage match")


input_prompt1 = """ 
    You are an experienced HR with Technical experience in the field of Data Science, Full stack, web development, Big data Engineering, DEVOPS, Data Analyst your task is to review the provided resume against the Job Description for these profiles.
    Please share your professional evaluation on whether the candidates pfofile aligns with the Job description. Highlights the strengths and weakness of the applicant in relation to the specified job description. """


input_prompt2 = """ 
    You are a skilled ATS (Applicant tracking System) scanner with a deep understanding of Data Science, Full stack, web development, Big data Engineering, DEVOPS, Data Analyst and deep ATS functionality
    your task is to evaluate the resume against the provided job description. Give the percentage of match if the resume matches job description. First the output should come as percentage and then keywords missing and last final thoughts.

    """

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload file")

if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2,pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload file")