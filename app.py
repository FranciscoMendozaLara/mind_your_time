import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

# Load life expectancy data
@st.cache
def load_life_expectancy_data(filepath):
    return pd.read_csv(filepath)

def calculate_life_expectancy(age, country, gender, df):
    """Lookup life expectancy based on country and gender."""
    row = df[df['name'] == country]
    if not row.empty:
        if gender == 'Male':
            expectancy = row.iloc[0]['male']
        else:  # Female
            expectancy = row.iloc[0]['female']
        return expectancy - age
    return None  # Indicate no data found

# def visualize_life_expectancy(total_years, lived_years, social_media_years, future_social_media_years):
#     """Create a visualization for life expectancy."""
#     fig, ax = plt.subplots(figsize=(10, 2))
#     # Ensuring the total is not less than the sum of components due to rounding
#     total_years = max(total_years, lived_years + int(social_media_years) + int(future_social_media_years))
#     circles = ['grey'] * lived_years + ['red'] * int(social_media_years) + ['blue'] * int(future_social_media_years) + ['green'] * (total_years - lived_years - int(social_media_years) - int(future_social_media_years))
#     for i, color in enumerate(circles):
#         ax.add_patch(plt.Circle((i % total_years, i // total_years), 0.4, color=color))
#     ax.set_xlim(0, total_years)
#     ax.set_ylim(-1, 1)
#     ax.axis('off')
#     st.pyplot(fig)

def visualize_life_expectancy_bars(lived_years, social_media_years, future_social_media_years, remaining_years):
    data = {
        "Category": ["Lived Years", "Social Media Years", "Future Social Media Years", "Remaining Years"],
        "Years": [lived_years, social_media_years, future_social_media_years, remaining_years]
    }
    df = pd.DataFrame(data)

    fig = px.bar(df, x='Category', y='Years', color='Category', title="Visualization of Life Expectancy Breakdown")
    fig.update_layout(xaxis=dict(title="Life Segments"), yaxis=dict(title="Years"), plot_bgcolor='white')

    st.plotly_chart(fig, use_container_width=True)

def visualize_life_expectancy(total_years, lived_years, social_media_years, future_social_media_years):
    # Calculate the breakdown
    total_years_adjusted = max(total_years, lived_years + int(social_media_years) + int(future_social_media_years))
    categories = ['Lived'] * lived_years + ['Social Media'] * int(social_media_years) + ['Projected Social'] * int(future_social_media_years) + ['Remaining'] * (total_years_adjusted - lived_years - int(social_media_years) - int(future_social_media_years))
    years = list(range(1, total_years_adjusted + 1))
    colors = ['grey'] * lived_years + ['red'] * int(social_media_years) + ['blue'] * int(future_social_media_years) + ['green'] * (total_years_adjusted - lived_years - int(social_media_years) - int(future_social_media_years))

    # Create a scatter plot with custom markers
    fig = go.Figure(data=go.Scatter(
        x=years,
        y=[1] * total_years_adjusted, # Y-axis values don't change because we want to simulate a line of circles
        mode='markers',
        marker=dict(size=20, color=colors), # Customize marker size and color
        text=categories, # Show category on hover
        hoverinfo='text+x'
    ))

    # Customize layout
    fig.update_layout(
        title="Visualization of Life Expectancy Breakdown",
        xaxis=dict(title="Years", showgrid=False, zeroline=False, visible=True),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='white',
        height=300, # Adjust the height to fit the single line of circles
        width=800, # Adjust the width as needed
    )

    fig.update_xaxes(range=[0, total_years_adjusted + 1]) # Adjust x-axis range to fit all circles

    st.plotly_chart(fig, use_container_width=True)    
    
    st.markdown("""
    ## How to Interpret the Graph

    The graph visualizes the breakdown of your life expectancy in relation to social media usage:

    - **Grey Circles**: Represent the years of life you have already lived. It's a look back at the time passed.
    - **Red Circles**: Indicate the estimated total years you've spent on social media based on your past usage. This highlights the impact of social media on your time.
    - **Blue Circles**: Show the projected time you will spend on social media if you continue with your current usage habits. It's a forward-looking estimate based on current trends.
    - **Green Circles**: Represent the remaining years of your life, excluding the time spent on social media. This is the time you have to pursue other activities, based on life expectancy data.

    Hover over the circles to see more details about each year. This visualization aims to provide a perspective on how social media fits into the broader context of your life, encouraging a thoughtful reflection on how you spend your time.
    """)



# def visualize_life_expectancy(total_years, lived_years, social_media_years, future_social_media_years):
#     """Create a visualization for life expectancy using Plotly with explanations."""
#     categories = ['Years Lived', 'Years on Social Media', 'Projected Social Media Use', 'Remaining Years']
#     values = [lived_years, social_media_years, future_social_media_years, total_years - lived_years - social_media_years - future_social_media_years]

#     # Create the figure
#     fig = go.Figure(data=[go.Bar(x=categories, y=values,
#                                  marker_color=['grey', 'red', 'blue', 'green'],
#                                  text=values,
#                                  textposition='auto')])

#     # Customize the layout
#     fig.update_layout(title_text='Life Expectancy Breakdown',
#                       yaxis=dict(title='Years'),
#                       plot_bgcolor='white')

#     st.plotly_chart(fig, use_container_width=True)

#     # Including explanatory text in the app
#     st.markdown("""
#     - **Years Lived**: The total years you've already lived.
#     - **Years on Social Media**: The estimated total years spent on social media based on your past usage.
#     - **Projected Social Media Use**: If you continue with your current social media habits, this is the additional time you might spend on social media.
#     - **Remaining Years**: Based on life expectancy data, this is the estimated time you have left, excluding the time spent on social media.
#     """)




def calculate_time_spent(start_year, total_daily_usage):
    """Calculate total time spent on social media so far."""
    current_year = datetime.now().year
    years_using_social_media = current_year - start_year
    # Assuming total_daily_usage is in minutes, convert to days
    total_minutes_spent = years_using_social_media * 365 * total_daily_usage
    total_days_spent = total_minutes_spent / (24 * 60)  # 24 hours in a day, 60 minutes in an hour
    return total_days_spent

def main():
    st.title("Mind Your Time")
    df_life_expectancy = load_life_expectancy_data('Life_Expectancy_by_Country_2021.csv')

    with st.form("user_input"):
        country = st.selectbox("Select your country:", df_life_expectancy['name'].unique())
        gender = st.selectbox("Select your gender:", ['Male', 'Female'])
        start_year = st.number_input("Year you started using social media:", min_value=1980, max_value=datetime.now().year, value=2010)
        daily_usage = st.multiselect("Select your social media platforms:", ['Facebook', 'Instagram', 'TikTok', 'Twitter', 'Snapchat', 'LinkedIn', 'YouTube', 'Reddit'])
        usage_time = {platform: st.number_input(f"Daily usage time for {platform} (in minutes):", min_value=0, value=30) for platform in daily_usage}
        age = st.number_input("Your current age:", min_value=10, max_value=100, value=25)
        submitted = st.form_submit_button("Calculate")

    if submitted:
        total_daily_usage = sum(usage_time.values())
        life_expectancy = calculate_life_expectancy(age, country, gender, df_life_expectancy)
        if life_expectancy is not None:
            days_spent = calculate_time_spent(start_year, total_daily_usage)
            years_remaining = life_expectancy
            total_years = int(age + years_remaining)
            projected_social_media_time = (total_daily_usage / 60) * 365 * years_remaining / 24 / 365
            remaining_years = years_remaining - projected_social_media_time

            # Calculate percentages
            percent_life_lived = (age / total_years) * 100
            percent_social_media_time = (days_spent / (age * 365)) * 100
            percent_life_left = 100 - percent_life_lived

            st.write(f"Based on your inputs, you have spent approximately {days_spent / 30:.2f} months ({days_spent:.2f} days) on social media so far.")
            st.write(f"With a life expectancy of approximately {total_years} years, you have about {years_remaining:.2f} years left.")
            st.write(f"If you continue with your current habits, you will spend about {projected_social_media_time:.2f} more years on social media.")

            # st.write(f"You have spent approximately {percent_social_media_time:.2f}% of your life on social media.")
            # st.write(f"You have about {percent_life_left:.2f}% of your life left.")
            # Display metrics
            st.metric(label="Percentage of Life Lived", value=f"{(age / total_years) * 100:.2f}%")
            st.metric(label="Percentage of Life Spent on Social Media", value=f"{(days_spent / (age * 365)) * 100:.2f}%")
            st.metric(label="Percentage of Life Left", value=f"{(remaining_years / total_years) * 100:.2f}%")


            visualize_life_expectancy(total_years, age, days_spent / 365, projected_social_media_time)
            # visualize_life_expectancy_bars(total_years, age, days_spent / 365, projected_social_media_time)

        else:
            st.write("Life expectancy data not available for your selections.")

if __name__ == "__main__":
    main()

