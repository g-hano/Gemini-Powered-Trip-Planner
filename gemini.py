from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
import json
from IPython.display import display, Markdown
import textwrap

class Gemini:
    def __init__(self, city, country, days, members):
        self.city = city
        self.country = country
        self.days = days
        self.members = members
        
        self.model = genai.GenerativeModel('gemini-pro')
        
    @staticmethod    
    def to_markdown(text):
        text = text.replace('•', '  *')
        return textwrap.indent(text, '> ', predicate=lambda _: True)

    def parse_trip_plan(self, trip_plan, return_=True):
        days = trip_plan.split("**Day ")[1:]  # Split the trip plan by "**Day " and remove the first empty string
        trip_dict = {}
        for i, day in enumerate(days, start=1):
            day_num = f"Day {i}"
            parts = day.split("*Morning:*")
            morning = parts[1].split("*Afternoon:*")[0].strip()
            afternoon = parts[1].split("*Afternoon:*")[1].split("*Evening:*")[0].strip()
            evening = parts[1].split("*Evening:*")[1].strip()
            trip_dict[day_num] = {
                "*Morning*:": f"\n{morning}\n",
                "*Afternoon*:": f"\n{afternoon}\n",
                "*Evening*:": f"\n{evening}\n"
            }
        with open("gemini_answer.json", "w") as json_file:
            json.dump(trip_dict, json_file, indent=4)
        if return_:
            return trip_dict
    
    def get_response(self, markdown=True):

        prompt = f"""Generate a trip plan for {self.city}, {self.country} spanning {self.days} days for a group of {self.members}.
        We are interested in a mix of historical sightseeing, cultural experiences, and delicious food.
        Provide a detailed itinerary for each day.
        Exclude any prices or costs. Make sure it is utf-8 encoded. I want the output in that format:
        **Day 1:**
        *Morning:*
        *Afternoon:*
        *Evening:*

        **Day 2:**
        *Morning:*
        *Afternoon:*
        *Evening:*
        """
        response = self.model.generate_content(prompt)
        if response.parts:
            response = response.parts[0].text
        
        if markdown:
            response = self.to_markdown(response)
        else:
            response = self.parse_trip_plan(response)
        return response