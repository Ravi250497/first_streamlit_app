import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('MY PARENTS NEW HEALTHY DINER')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toas')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')   

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
# Display the table on the page.
streamlit.dataframe(my_fruit_list)

#fruits as index instead number
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
# Display the table on the page.
#streamlit.dataframe(my_fruit_list)
# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
# Display the table on the page.
streamlit.dataframe(my_fruit_list)
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#display table
streamlit.dataframe(fruits_to_show)
#new section to display
streamlit.header("Fruityvice Fruit Advice!")
#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")


# changing to table format
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

#streamlit.dataframe(fruityvice_normalized)
#Edited after import statements
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select the fruit to get the information")
  else:
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

#streamlit.write('The user entered ', fruit_choice)
#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
streamlit.stop()
#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("FRUIT LOAD LIST CONTAINS")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('what fruit would you like to add')
streamlit.write('thanks for adding my fruit',add_my_fruit)

my_cur.execute("insert into fruit_load_list values('from streamlit')")
