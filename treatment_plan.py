# Import necessary libraries
from typing_extensions import Protocol
from langchain.llms import OpenAI
from collections.abc import Iterator
from langchain.llms.openai import OpenAI
from langchain.chains import LLMChain, SequentialChain
import os
import time
import streamlit as st
from langchain.prompts import PromptTemplate
from docx import Document

# Treatment Plan Template
treatment_plan_template = PromptTemplate(
    input_variables=["diagnosis"],
    template="Create a treatment plan for this diagnosis: {diagnosis}",
)

# Follow-Up Schedule Template
follow_up_schedule_template = PromptTemplate(
    input_variables=["treatment_plan"],
    template="Generate a follow-up schedule for this treatment plan: {treatment_plan}",
)

# Initialize OpenAI LLM
llm = OpenAI(openai_api_key='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', temperature=0.7)

# Treatment Plan Chain
treatment_plan_chain = LLMChain(
    llm=llm,
    prompt=treatment_plan_template,
    output_key="treatment_plan",
    verbose=True
)

# Follow-Up Schedule Chain
follow_up_schedule_chain = LLMChain(
    llm=llm,
    prompt=follow_up_schedule_template,
    output_key="follow_up_schedule",
    verbose=True
)

# Overall Chain
overall_chain = SequentialChain(
    chains=[treatment_plan_chain, follow_up_schedule_chain],
    input_variables=["diagnosis"],
    output_variables=["treatment_plan", "follow_up_schedule"],
    verbose=True
)

# Streamlit Interface
st.title("Medical Treatment Planner")
user_prompt = st.text_input("Enter diagnosis")

if st.button("Generate Treatment Plan and Follow-Up Schedule") and user_prompt:
    output = overall_chain({'diagnosis': user_prompt})
    treatment_plan_output = output['treatment_plan']
    follow_up_schedule_output = output['follow_up_schedule']

    # Convert to Word Document
    def text_to_word_doc(text, filename):
        doc = Document()
        doc.add_paragraph(text)
        doc.save(filename)

    text_to_word_doc(treatment_plan_output + "\n\n" + follow_up_schedule_output, "medical_plan.docx")

    # Download button for Word document
    with open("medical_plan.docx", "rb") as file:
        st.download_button('Download Medical Plan as Word Doc', file, "medical_plan.docx")
