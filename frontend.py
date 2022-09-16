import streamlit as st

st.title('Hate Speech detection with Modular Pipelines')

title = st.text_input('Text to analyze (use ; to add multiple)', 'Life of Brian')
st.write('The current movie title is', title)