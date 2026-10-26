# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, width='stretch')
st.stop()

ingredients_list = st.multiselect(
  'Choose up to 5 ingredients'
  , my_dataframe
  , max_selections=5
)

if ingredients_list:
  ingredients_string=''

  for fruits_chosen in ingredients_list:
    ingredients_string += fruits_chosen + ' '
    st.subheader(fruits_chosen + ' Nutrition Information')
    smoothiefront_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruits_chosen)
    st_df = st.dataframe(data=smoothiefront_response.json(), width='stretch')

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
                                                                          

