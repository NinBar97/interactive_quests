# ./streamlit_app/main.py

import streamlit as st
from quests import quest1, quest3, quest4, quest5, quest6

# Sidebar navigation
selection = st.sidebar.radio(("Select a Quest"), ["Quest 1", "Quest 3", "Quest 4", "Quest 5", "Quest 6"])

if selection == "Quest 1":
    quest1.run()
elif selection == "Quest 3":
    quest3.run()
elif selection == "Quest 4":
    quest4.run()
elif selection == "Quest 5":
    quest5.run()
elif selection == "Quest 6":
    quest6.run()