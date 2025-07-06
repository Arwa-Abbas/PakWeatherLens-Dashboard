import streamlit as st
import pandas as pd
import requests
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import patheffects as PathEffects
from PIL import Image
import os

st.set_page_config(page_title="PakWeatherLens", layout="wide")

neon_blue = "#00d4ff"
neon_purple = "#9400ff"
neon_colors = ["#00d4ff", "#0095ff", "#001aff", "#9400ff"]
neon_cmap = LinearSegmentedColormap.from_list("neon", neon_colors)


def get_temp_icon(temp):
    """Returns appropriate thermometer icon based on temperature"""
    if temp >= 40:
        icon_path = "icons/temperature_hot.png"
    elif temp >= 25:
        icon_path = "icons/temperature_moderate.png"
    else:
        icon_path = "icons/temperature_cold.png"
    
    try:
        return Image.open(icon_path)
    except:
        return None


def get_humidity_icon(humidity):
    """Returns appropriate humidity icon based on percentage"""
    if humidity >= 70:
        icon_path = "icons/humidity_high.png"
    elif humidity >= 40:
        icon_path = "icons/humidity_mid.png"
    else:
        icon_path = "icons/humidity_low.png"
    
    try:
        return Image.open(icon_path)
    except:
        return None



def get_condition_icon(condition_text):
    """Returns appropriate condition icon based on weather condition"""
    condition_text = condition_text.lower()
    
    if 'sunny' in condition_text or 'clear' in condition_text:
        icon_path = "icons/sunny.png"
    elif 'cloudy' in condition_text or 'overcast' in condition_text:
        icon_path = "icons/cloudy.png"
    elif 'rain' in condition_text or 'drizzle' in condition_text:
        icon_path = "icons/rainy.png"
    elif 'thunder' in condition_text or 'storm' in condition_text:
        icon_path = "icons/thunder.png"
    elif 'snow' in condition_text or 'sleet' in condition_text:
        icon_path = "icons/snowy.png"
    elif 'fog' in condition_text or 'mist' in condition_text:
        icon_path = "icons/fog.png"
    else:
        icon_path = "icons/cloudy.png"  # default
    
    try:
        return Image.open(icon_path)
    except:
        return None


def set_background(image_file, overlay_color="rgba(0, 100, 200, 0.4)"):
    """Set background with customizable overlay"""
    if not Path(image_file).exists():
        st.error(f"Background image not found at: {image_file}")
        return

    with open(image_file, "rb") as f:
        img_data = f.read()
    encoded = base64.b64encode(img_data).decode()

    css = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 255, 0.55), rgba(0,0, 255, 0.25)), 
                   url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        text-align: center;
        color: white;
        text-shadow: 0 0 10px {neon_blue};
    }}
    
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        border-radius: 10px;
        padding: 2rem;
    }}
    
    section[data-testid="stSidebar"] {{
        background-color: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(8px);
        border-right: 1px solid {neon_blue};
    }}
    
    .metric-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 10px;
        padding: 15px;
    }}
    
    .metric-title {{
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 5px;
    }}
    
    .metric-value {{
        font-size: 2rem;
        font-weight: bold;
    }}
    
    .dashboard-card {{
        background-color: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(5px);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 8px 16px;
        border-radius: 4px;
        background-color: rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: rgba(0, 212, 255, 0.2);
        border-bottom: 2px solid #00d4ff;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)



set_background("backgrounds/main_bg.jpg", overlay_color="rgba(25, 100, 200, 0.3)")


# API 
api_key = "378637af2f4a4f5b8ad64142250607"  # Your API key
cities = [
    "Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad",
    "Hyderabad", "Multan", "Peshawar", "Quetta", "Sialkot",
    "Bahawalpur", "Sargodha", "Gujranwala", "Abbottabad", "Mirpur"
]


# Sidebar
with st.sidebar:
    st.title("🌦️ Dashboard Controls")
    dashboard_view = st.radio("View Mode", ["Single City", "All Cities Comparison"])
    
    if dashboard_view == "Single City":
        selected_city = st.selectbox("Select City", cities)
        day_option = st.radio("Select Day", ["Today", "Yesterday"])
    else:
        day_option = st.radio("Compare Days", ["Today vs Yesterday"])


st.title("PakWeatherLens Dashboard")
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  # Added space


def fetch_weather_data():
    """Fetch weather data for all cities"""
    today_weather = []
    yesterday_weather = []
    yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    with st.spinner("Fetching latest weather data..."):
        for city in cities:
            # Today's weather
            url_today = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
            res_today = requests.get(url_today)
            if res_today.status_code == 200:
                data_today = res_today.json()
                today_weather.append({
                    "City": city,
                    "Date": datetime.date.today().strftime("%Y-%m-%d"),
                    "Temp (°C)": data_today['current']['temp_c'],
                    "Humidity (%)": data_today['current']['humidity'],
                    "Condition": data_today['current']['condition']['text']
                })

            # Yesterday's weather
            url_yest = f"http://api.weatherapi.com/v1/history.json?key={api_key}&q={city}&dt={yesterday_date}"
            res_yest = requests.get(url_yest)
            if res_yest.status_code == 200:
                data_yest = res_yest.json()
                try:
                    y = data_yest['forecast']['forecastday'][0]['day']
                    yesterday_weather.append({
                        "City": city,
                        "Date": yesterday_date,
                        "Temp (°C)": y['avgtemp_c'],
                        "Humidity (%)": y['avghumidity'],
                        "Condition": y['condition']['text']
                    })
                except:
                    pass

    return pd.DataFrame(today_weather + yesterday_weather)


# Load or fetch data
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    return fetch_weather_data()

combined_data = load_data()


if dashboard_view == "Single City":
    # Convert dates to strings for consistent comparison
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    yesterday_str = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Filter data for selected city and day
    if day_option == "Today":
        city_data = combined_data[
            (combined_data['City'] == selected_city) & 
            (combined_data['Date'] == today_str)
        ]
    else:
        city_data = combined_data[
            (combined_data['City'] == selected_city) & 
            (combined_data['Date'] == yesterday_str)
        ]
    
    # Handle case where no data is found
    if city_data.empty:
        st.warning(f"No weather data available for {selected_city} on {day_option}")
        st.stop()
    
    if not city_data.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            temp = city_data['Temp (°C)'].values[0]
            st.markdown("""
            <div class="metric-container">
                <div class="metric-title">Temperature</div>
                <div class="metric-value">{temp} °C</div>
            """.format(temp=temp), unsafe_allow_html=True)
            
            temp_icon = get_temp_icon(temp)
            if temp_icon:
                st.image(temp_icon, width=80)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            humidity = city_data['Humidity (%)'].values[0]        
            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="metric-title">Humidity</div>
                    <div class="metric-value">{humidity} %</div>
                """,
                unsafe_allow_html=True
            )
            
            hum_icon = get_humidity_icon(humidity)
            if hum_icon:
                st.image(hum_icon, width=80)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            condition = city_data['Condition'].values[0]
            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="metric-title">Condition</div>
                    <div class="metric-value">{condition}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            cond_icon = get_condition_icon(condition)
            if cond_icon:
                st.image(cond_icon, width=80)  # Same size as temp/humidity icons
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.subheader(f"🌤️ Weather Details for {selected_city}")
        
        # Display weather condition image if available
       

else:  # All Cities Comparison
    st.subheader("Pakistan Cities Weather Comparison")
    
    tab1, tab2 = st.tabs(["🌡️ Temperature Trends", "💧 Humidity Patterns"])
    
    with tab1:
        # Prepare temperature data
        temp_df = combined_data.pivot(index='City', columns='Date', values='Temp (°C)')
        temp_df = temp_df.sort_values(by=temp_df.columns[-1], ascending=False)
        
        # Create modern line plot
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Plot each city 
        for i, city in enumerate(temp_df.index):
            ax.plot(temp_df.columns, temp_df.loc[city], 
                   marker='o', 
                   linewidth=2.5,
                   markersize=8,
                   color=neon_colors[i % len(neon_colors)],
                   alpha=0.8,
                   label=city)
        
       
        for line in ax.lines:
            line.set_path_effects([
                PathEffects.Stroke(linewidth=8, foreground=line.get_color(), alpha=0.2),
                PathEffects.Normal()
            ])
        
       
        ax.set_title('Temperature Trends Across Cities', 
                    fontsize=16, pad=20, color='white')
        ax.set_ylabel('Temperature (°C)', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
       
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        
        plt.tight_layout()
        st.pyplot(fig)
        
     
        st.subheader("Temperature Heatmap")
        fig2, ax2 = plt.subplots(figsize=(14, 4))
        sns.heatmap(temp_df, cmap=neon_cmap, annot=True, fmt=".1f", 
                   linewidths=.5, ax=ax2, cbar_kws={'label': 'Temperature (°C)'})
        ax2.set_facecolor('none')
        fig2.patch.set_facecolor('none')
        st.pyplot(fig2)
    
    with tab2:
        # Prepare humidity data
        hum_df = combined_data.pivot(index='City', columns='Date', values='Humidity (%)')
        hum_df = hum_df.sort_values(by=hum_df.columns[-1], ascending=False)
        
        # Create modern area plot
        fig3, ax3 = plt.subplots(figsize=(14, 7))
        
        # Stacked area plot with transparency
        hum_df.T.plot(kind='area', ax=ax3, alpha=0.6, cmap=neon_cmap)
        
     
        ax3.set_title('Humidity Patterns Across Cities', 
                     fontsize=16, pad=20, color='white')
        ax3.set_ylabel('Humidity (%)', fontsize=12)
        ax3.set_xlabel('Date', fontsize=12)
        ax3.grid(True, linestyle='--', alpha=0.3)
        ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
     
        fig3.patch.set_facecolor('none')
        ax3.set_facecolor('none')
        ax3.spines['bottom'].set_color('white')
        ax3.spines['left'].set_color('white')
        ax3.tick_params(colors='white')
        ax3.xaxis.label.set_color('white')
        ax3.yaxis.label.set_color('white')
        ax3.title.set_color('white')
        
        plt.tight_layout()
        st.pyplot(fig3)
        
        # Humidity radar chart 
        st.subheader("Humidity Radar View")
        fig4 = plt.figure(figsize=(10, 10))
        ax4 = fig4.add_subplot(111, polar=True)
        
        # Normalize data for radar chart
        norm_hum = hum_df.apply(lambda x: x/x.max(), axis=1)
        
    
        for idx, city in enumerate(norm_hum.index):
            values = norm_hum.loc[city].tolist()
            values += values[:1]  # Close the radar chart
            angles = [n/float(len(norm_hum.columns))*2*3.14159 for n in range(len(norm_hum.columns))]
            angles += angles[:1]
            ax4.plot(angles, values, linewidth=2, linestyle='solid', 
                    label=city, color=neon_colors[idx % len(neon_colors)])
            ax4.fill(angles, values, alpha=0.1, color=neon_colors[idx % len(neon_colors)])
        
     
        ax4.set_theta_offset(3.14159 / 2)
        ax4.set_theta_direction(-1)
        ax4.set_title("Relative Humidity Comparison", color='white', y=1.1)
        ax4.set_facecolor('none')
        fig4.patch.set_facecolor('none')
        ax4.grid(color='white', alpha=0.3)
        plt.legend(bbox_to_anchor=(1.3, 1), loc='upper right')
        st.pyplot(fig4)


#st.markdown("---")("%Y-%m-%d %H:%M:%S"))