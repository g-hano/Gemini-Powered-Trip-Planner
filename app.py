import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
import json
from IPython.display import display, Markdown
from gemini import Gemini

import folium
import requests
import spacy
import streamlit.components.v1 as components
from streamlit_folium import folium_static

nlp = spacy.load("en_core_web_sm")

# Function to extract locations
def extract_locations(text):
    if type(text) is dict:
        a = ""
        for t in text.values():    
            a += f"{t}"
        text = a
        
    locations = {}
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Check if the entity is a geopolitical entity (i.e., a location)
            locations[ent.text] = geocode_location(ent.text)
    return {k: v for k, v in locations.items() if v is not None}
    
        
# Function to geocode location
def geocode_location(location):
    api_key = os.environ.get("GOOGLEMAPS_API_KEY")  # Replace with your API key
    map_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {'address': location, 'key': api_key}
    response = requests.get(map_url, params=params).json()
    if response['status'] == 'OK':
        latlng = response['results'][0]['geometry']['location']
        return latlng['lat'], latlng['lng']
    else:
        return None

if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
if 'generate_button_clicked' not in st.session_state:
    st.session_state["generate_button_clicked"] = False
if 'model' not in st.session_state:
    st.session_state["model"] = None
if 'response' not in st.session_state:
    st.session_state["response"] = ""

def main():
    session_state = st.session_state
        
    st.title("Travel Planner")
    model = st.session_state["model"]

    col1, col2, col3 = st.columns([1, 4, 2])
    print(session_state)
    
    #with col1:
    st.sidebar.header("Trip Details")
    country = st.sidebar.text_input("Enter the country", "Russia")
    city = st.sidebar.text_input("Enter the city", "Moscow")
    days = st.sidebar.number_input("For how many days?",  min_value=1, value=3)
    members = st.sidebar.number_input("How big is your group?",  min_value=1, value=1)
    if st.sidebar.button("Generate Trip Plan"):
        model = Gemini(city, country, days, members)
        model.get_response(markdown=False)
        st.session_state["model"] = model
        session_state["generate_button_clicked"] = True
                
    with col2:
        st.title("Gemini Response")
        response = {}
        if st.session_state["generate_button_clicked"]:
            with open(r'C:\Users\Cihan\Desktop\streamlit\gemini_answer.json', 'r', encoding="utf-8") as file:
                response = json.load(file)
                st.session_state["response"] = response
        current_day = f"Day {st.session_state['counter'] + 1}"
        current_day_placeholder = st.empty()
        current_day_infos = st.empty()
        if model is not None:
            if current_day in response:
                info = "".join([f"**{key}** {value}\n" for key, value in response[current_day].items()])
                result = f"{info}"
                current_day_placeholder.write(f"{current_day}")                   
                current_day_infos.write(model.to_markdown(result))
            else:
                current_day_infos.write("Generate a Trip Plan!")

        button = st.button("Next Day")
        if button and st.session_state['counter'] != len(response) - 1:
            st.session_state['counter'] += 1
            
            if current_day in response:
                if model is not None:
                    current_day_infos.empty()
                    info = "".join([f"**{key}** {value.strip('    ')}\n" for key, value in response[current_day].items()])
                    result = f"{info}"
                                
                    current_day_infos.write(model.to_markdown(result))
                else:
                    print("Model none")
            else:
                current_day_infos.empty()
                current_day_infos.write("No information available for this day.")

    with col3:
        locations = extract_locations(st.session_state["response"])
  
        #print(locations)
        coordinates = [location for location in locations.values() if location is not None]
        map_center = [sum(coord) / len(coord) for coord in zip(*coordinates)] if coordinates else None
        if map_center:
            mymap = folium.Map(location=map_center, zoom_start=3)
            
            # Add markers for each location
            for place_name, loc in locations.items():
                if loc is not None:
                    folium.Marker(loc, popup=place_name).add_to(mymap)
            #st.title("\t\tMap Viewer")
            st.markdown("<div style='text-align: right; font-size: 30px; font-weight: bold;'>Map Viewer</div>", unsafe_allow_html=True)

            folium_static(mymap, width=600, height=400)

if __name__ == '__main__':
    main()