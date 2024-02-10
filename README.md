# Gemini Powered Trip Planner

Gemini Powered Trip Planner is a Python project that leverages Google's Generative AI capabilities to generate detailed trip plans for various destinations. It utilizes Streamlit for the user interface and incorporates Google's Generative AI model (Gemini) to create personalized travel itineraries.

## Table of Contents
- [Introduction](#introduction)
- [Gemini Class](#gemini-class)
- [Streamlit Code](#streamlit-code)
- [How to Use](#how-to-use)
- [Usage Video](#usage-video)
- [Dependencies](#dependencies)

## Introduction

Planning a trip can be a daunting task, especially when trying to balance different interests and preferences. Gemini Powered Trip Planner aims to simplify this process by providing users with personalized trip itineraries based on their specified preferences.

## Gemini Class

The `Gemini` class is the backbone of this project. It is responsible for generating trip plans using Google's Generative AI model (Gemini). Key functionalities of the `Gemini` class include:
- Initializing trip parameters such as city, country, duration, and group size.
- Generating trip plans based on provided parameters.
- Parsing and formatting trip plans into Markdown or JSON format.
- Communicating with Google's Generative AI model to generate detailed trip itineraries.

## Streamlit Code

The Streamlit code serves as the user interface for the Gemini Powered Trip Planner. It allows users to input their trip details and view the generated trip plan. Key features of the Streamlit code include:
- Input fields for specifying trip details such as country, city, duration, and group size.
- A "Generate Trip Plan" button to trigger the generation of the trip itinerary.
- Display of the generated trip plan, including daily activities and locations on an interactive map.
- Navigation buttons to browse through the generated trip plan day by day.

## How to Use

To use Gemini Powered Trip Planner, follow these steps:
1. Ensure all dependencies are installed (see Dependencies section).
2. Run the Streamlit code using Python.
3. Enter the desired trip details including country, city, duration, and group size.
4. Click on the "Generate Trip Plan" button to generate the trip itinerary.
5. Navigate through the generated trip plan using the "Next Day" button.
6. Explore the interactive map to view the locations mentioned in the trip plan.

## Usage Video

You can watch a demonstration of how to use Gemini Powered Trip Planner by clicking the video link below:

[![Watch the video](https://img.shields.io/badge/-Watch%20the%20video-blue)](usage.mp4)

Click the badge above to watch the video demonstration of Gemini Powered Trip Planner.

## Dependencies

Ensure you have the following dependencies installed to run Gemini Powered Trip Planner:
- Streamlit
- Dotenv
- Google Generative AI
- Folium
- Requests
- Spacy
- Streamlit Folium

You can install these dependencies using pip:

```bash
pip install streamlit python-dotenv google-generativeai folium requests spacy streamlit-folium
