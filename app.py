import streamlit as st
import csv
import io

from text_variant import question_generator

def file_to_list(bytes_data:bytes) -> list[str]:
    data = []
    with io.StringIO(bytes_data.decode('utf-8')) as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)  # Skip the header row
        for row in reader:
            data.append(row[0])
    return data
    
# Streamlit app
def main():
    st.title(" 🤖 AI Assist for Educators ")
    st.header("Question Variant Generator", 
            divider="gray")
    st.write("""This app transforms your original quiz 
            questions into multiple variants with just 
            a TSV file upload. """)

    # File Uploader
    uploaded_file = st.file_uploader(
            label="Upload a TSV file with questions", 
            type="tsv")
        
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        q_list = file_to_list(bytes_data)        

        # Generate variants for each question 
        variant_1, variant_2 = question_generator(q_list)    
        output = io.StringIO()
        writer = csv.writer(output, delimiter='\t')
        writer.writerow(["question", "variant1", "variant2"])
        for row in zip(q_list, variant_1, variant_2):
            writer.writerow(row)
            st.write("Question : " , row[0])
            st.write("Variant 1: " , row[1])
            st.write("Variant 2 :" , row[2])
        
        st.subheader("Output with 2 variants of each question")
        csv_data = output.getvalue()
        st.download_button(
            label="Download Processed Data as TSV",
            data=csv_data,
            file_name="processed_data.tsv",
            mime="text/csv",
            )
        
if __name__ == "__main__":
    main()
