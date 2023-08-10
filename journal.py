import streamlit as st
import datetime
from utils import *
st.title("📖 Journal X")
st.write("👼🏻 Be your own therapist")


tab1, tab2, tab3 = st.tabs(["Log your feelings", "Mood board", "Chat with yourself!"])


with tab1:
    with st.form(key='my_form'):
        date_input = st.date_input("Date", datetime.datetime.now())
        # st.markdown("Mood: 1 - Unhappy, 5 - Calm, 10 - Elated")
        mood_scale = st.slider("Mood Scale (1 : 😣, 5 : 🙂, 10 : 🙃)", min_value=1, max_value=10, value = 5, step=1)
        notes = st.text_area("How are you feeling?", "Enter your notes here...")
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        journal_info = {
            "username" : "DefaultUser",
            "date" : date_input.isoformat(),
            "mood_scale": mood_scale,
            "notes": notes,
            "description" : journal_summary(notes),
            "notes_vec" : embed_text(notes),
        }

        insert_into_db(journal_info)
        st.success("Journal entry submitted successfully!") 

with tab2:
    st.write("Mood board coming soon!")

with tab3:
    st.write("Chatbot coming soon!")