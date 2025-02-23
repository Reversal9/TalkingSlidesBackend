import pymupdf
import openai
from openai import OpenAI
import os



system_prompt = """
You are a helpful assistant. You will be provided with a document delimited by triple quotes.
Your goal is to convert the text in the document to a presentation script for a video.
Divide the script into sections that are at most 3 minutes long. Include markers to indicate
a new section in the script in the format [Section #N].
"""

script_formatter = """

"""
def parse_pdf(filename):
    delimited_text = ""
    doc = pymupdf.open(filename)
    num_pages = doc.page_count
    page_num = 0
    for page in doc: 
        page_text = page.get_text("blocks")  
        for block in page_text:
            delimited_text += block
            delimited_text += "[Section {page_num}]\n"
        page_num += 1
    return delimited_text

def parse_pdf_binary(binary_content):
    doc = pymupdf.open(stream=binary_content,filetype="pdf")
    delimited_text = ""
    num_pages = doc.page_count
    page_num = 0
    for page in doc: 
        page_text = page.get_text("blocks")  
        for block in page_text:
            delimited_text += block[4]
            delimited_text += "[Section {page_num}]\n"
        page_num += 1
    doc.close()
    return delimited_text
        
def generate_script(input_text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    script = ""
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": system_prompt},
            {
                "role": "user",
                "content": f"Convert these lecture notes into a presentation script. {input_text}"
            }
        ],
        stream=True,
        prediction={
            "type": "content",
            "content": script_formatter
        }
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            script += chunk.choices[0].delta.content
        
    return script

