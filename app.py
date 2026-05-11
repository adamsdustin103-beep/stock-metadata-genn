import streamlit as st
from google import genai
import PIL.Image
import io
import csv
import time

st.set_page_config(page_title="Stock Metadata AI", layout="wide")
st.title("📸 Adobe & Shutterstock Metadata Generator")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    uploaded_files = st.file_uploader("ছবি সিলেক্ট করুন...", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

    if uploaded_files:
        if st.button("Generate Metadata"):
            results = []
            for uploaded_file in uploaded_files:
                st.write(f"এনালাইসিস হচ্ছে: {uploaded_file.name}")
                img = PIL.Image.open(uploaded_file)
                prompt = "Analyze this image for Adobe Stock. Provide Title (max 100 chars) and 45 keywords. Format: Title: [Title] Keywords: [Keywords separated by commas]"
                try:
                    time.sleep(10) # লিমিট ঠিক রাখতে
                    response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt, img])
                    text = response.text
                    title = text.split('Title:')[1].split('Keywords:')[0].strip()
                    keywords = text.split('Keywords:')[1].strip()
                    results.append([uploaded_file.name, title, keywords])
                except Exception as e:
                    st.error(f"Error: {e}")

            if results:
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(['Filename', 'Title', 'Keywords'])
                writer.writerows(results)
                st.download_button(label="📥 Download CSV", data=output.getvalue(), file_name="metadata.csv", mime="text/csv")
else:
    st.warning("সাইডবারে API Key দিন।")
