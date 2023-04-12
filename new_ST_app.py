import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import random

# Define the coffee and mood image URLs
coffee_urls = [
    "https://images.unsplash.com/photo-1508921912182-ccd3ce2d6843",
    "https://images.unsplash.com/photo-1532635339-9ca9ac52cd75",
    "https://images.unsplash.com/photo-1545265177-3a2a497d8a0f",
    "https://images.unsplash.com/photo-1534361960058-f2aa62d0cfc1",
    "https://images.unsplash.com/photo-1550684845-5d4c0d0e5a5a"
]

mood_urls = [
    "https://images.unsplash.com/photo-1542362567-3d3b3fadc3c0",
    "https://images.unsplash.com/photo-1553155099-d8a0555840e4",
    "https://images.unsplash.com/photo-1567318388593-7c3e9a9a8e16",
    "https://images.unsplash.com/photo-1600404828348-997803aca55b",
    "https://images.unsplash.com/photo-1604643448024-e0d122b30ee2"
]

# Define a function to display images
def show_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    st.image(img, width=300)

# Define the Streamlit app
def main():
    # Set up the sidebar
    st.sidebar.header("Input Parameters")
    show_coffee = st.sidebar.checkbox("Show coffee images")
    show_mood = st.sidebar.checkbox("Show mood images")
    button_clicked = st.sidebar.button("Submit")
    
    # Display the images if the Submit button is clicked
    if button_clicked:
        if show_coffee:
            st.subheader("Random Coffee Images")
            for i in range(5):
                random_coffee_url = random.choice(coffee_urls)
                show_image(random_coffee_url)
        if show_mood:
            st.subheader("Random Mood Images")
            for i in range(5):
                random_mood_url = random.choice(mood_urls)
                show_image(random_mood_url)

if __name__ == "_main_":
    main()