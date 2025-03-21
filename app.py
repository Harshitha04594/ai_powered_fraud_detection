import streamlit as st

st.title("My New Streamlit App")
st.write("Welcome to my second Streamlit project!")

user_input = st.text_input("Enter your name:")
if st.button("Submit"):
    st.write(f"Hello, {user_input}!")
