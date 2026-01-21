"""
Wejha - Interactive Spatial Analysis Dashboard for Tuwaiq Academy
A professional dashboard combining spatial analysis with visual aesthetics.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from folium.raster_layers import ImageOverlay
from folium.plugins import HeatMap
from PIL import Image
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
import base64


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Wejha - Tuwaiq Academy",
    page_icon="data/wejha_logo_textless.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.logo("data/wejha_logo_textless.png",size="large")

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================
def load_custom_css():
    st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary-color: #6C63FF;
            --secondary-color: #4ECDC4;
            --accent-color: #FF6B6B;
            --background-dark: #1a1a2e;
            --background-light: #16213e;
            --text-color: #eaeaea;
            --card-bg: rgba(255, 255, 255, 0.05);
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Main header styling */
        .main-header {
            background: linear-gradient(135deg, #6C63FF 0%, #4ECDC4 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 10px 40px rgba(108, 99, 255, 0.3);
        }

        .main-header h1 {
            color: white;
            font-size: 3rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .main-header p {
            color: rgba(255,255,255,0.9);
            font-size: 1.2rem;
            margin-top: 0.5rem;
        }

        /* Metric cards */
        .metric-card {
            background: linear-gradient(145deg, #1e1e30, #2a2a40);
            border-radius: 15px;
            padding: 1.5rem;
            margin-top: 1rem;
            text-align: center;
            border: 1px solid rgba(108, 99, 255, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(108, 99, 255, 0.2);
        }

        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #6C63FF, #4ECDC4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .metric-label {
            color: #888;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0.5rem;
        }

        /* Section headers */
        .section-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: #6C63FF;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(108, 99, 255, 0.3);
        }

        /* Info boxes */
        .info-box {
            background: linear-gradient(145deg, rgba(108, 99, 255, 0.1), rgba(78, 205, 196, 0.1));
            border-left: 4px solid #6C63FF;
            padding: 1rem 1.5rem;
            border-radius: 0 10px 10px 0;
            margin: 1rem 0;
        }

        /* Route result card */
        .route-card {
            background: linear-gradient(145deg, #1e1e30, #2a2a40);
            border-radius: 15px;
            padding: 2rem;
            border: 1px solid rgba(78, 205, 196, 0.3);
            margin: 1rem 0;
        }

        .route-card h3 {
            color: #4ECDC4;
            margin-bottom: 1rem;
        }

        /* POI category badges */
        .poi-badge {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin: 0.2rem;
        }

        .badge-classroom { background: rgba(108, 99, 255, 0.2); color: #6C63FF; }
        .badge-amenity { background: rgba(78, 205, 196, 0.2); color: #4ECDC4; }
        .badge-facility { background: rgba(255, 107, 107, 0.2); color: #FF6B6B; }
        .badge-emergency { background: rgba(255, 193, 7, 0.2); color: #FFC107; }

        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        }

        /* Animation for cards */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .animate-fade-in {
            animation: fadeInUp 0.5s ease-out forwards;
        }

        /* Streamlit elements customization */
        .stSelectbox > div > div {
            background-color: #2a2a40;
            border-color: rgba(108, 99, 255, 0.3);
        }

        .stButton > button {
            background: linear-gradient(135deg, #6C63FF 0%, #4ECDC4 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(108, 99, 255, 0.4);
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: rgba(108, 99, 255, 0.1);
            border-radius: 10px;
            padding: 10px 20px;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #6C63FF 0%, #4ECDC4 100%);
        }

        /* Floor plan container */
        .floor-plan-container {
            background: #1a1a2e;
            border-radius: 15px;
            padding: 1rem;
            border: 1px solid rgba(108, 99, 255, 0.2);
        }

        /* Legend styling */
        .legend-item {
            display: flex;
            align-items: center;
            margin: 0.5rem 0;
        }

        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA DEFINITIONS
# ============================================================================

# POI Categories and Icons
POI_CATEGORIES = {
    'classroom': {'icon': '', 'color': '#6C63FF', 'label': 'Classroom'},
    'amenity': {'icon': '', 'color': '#4ECDC4', 'label': 'Amenity'},
    'facility': {'icon': '', 'color': '#FF6B6B', 'label': 'Facility'},
    'emergency': {'icon': '', 'color': '#FFC107', 'label': 'Emergency'},
    'prayer_rooms': {'icon': '', 'color': '#9C27B0', 'label': 'Prayer Rooms'},
    'administrative': {'icon': '', 'color': '#FF9800', 'label': 'Administrative'},
    'navigation': {'icon': '', 'color': '#00BCD4', 'label': 'Navigation'},
}

def categorize_poi(name):
    """Categorize a POI based on its name."""
    name_lower = name.lower()
    if any(x in name_lower for x in ['b0-', 'b1-']):
        return 'classroom'
    elif any(x in name_lower for x in ['cafeteria', 'dunkin', 'sandwich', 'subway', 'rest area', 'waiting', 'maps']):
        return 'amenity'
    elif any(x in name_lower for x in ['bathroom', 'elevator']):
        return 'facility'
    elif 'emergency' in name_lower:
        return 'emergency'
    elif 'prayer' in name_lower:
        return 'prayer_rooms'
    elif any(x in name_lower for x in ['reception', 'entrance', 'principal']):
        return 'administrative'
    else:
        return 'facility'

# Floor 0 POIs
FLOOR_0_POIS = {
    'Entrance': {'x': 0.784, 'y': -0.722},
    'Reception': {'x': -4.225, 'y': -0.722},
    'Waiting Area': {'x': -9.394, 'y': -0.512},
    'Elevator': {'x': -8.427, 'y': -0.512},
    "Dunkin' Donuts": {'x': -7.922, 'y': -0.512},
    'B0-1': {'x': -6.738, 'y': -0.512},
    'Bathroom/M': {'x': -2.905, 'y': -0.512},
    'Bathroom/F': {'x': -1.713, 'y': -0.512},
    'Rest Area 1': {'x': -2.009, 'y': -0.512},
    'Rest Area 2': {'x': 1.722, 'y': -0.512},
    'Maps': {'x': 4.503, 'y': -0.512},
    'Cafeteria': {'x': -1.12, 'y': -0.512},
    'Sandwich': {'x': -1.59, 'y': -0.512},
    'Subway': {'x': 7.594, 'y': -0.512},
}

# Floor 1 POIs
FLOOR_1_POIS = {
    'Reception': {'x': -4.46, 'y': 3.48},
    'Rest Area 3': {'x': -5.742, 'y': 3.48},
    'Elevator 2': {'x': -8.39, 'y': 3.48},
    'School Principal': {'x': -4.7, 'y': 3.48},
    'B1-1': {'x': -6.956, 'y': 3.48},
    'Prayer Room/F': {'x': -9.376, 'y': 3.48},
    'Bathroom/F': {'x': -16.758, 'y': 3.48},
    'Emergency Exit': {'x': -19.728, 'y': 3.48},
    'B1-2': {'x': -34.319, 'y': 3.48},
    'B1-3': {'x': -33.97, 'y': 3.48},
    'B1-4': {'x': -42.17, 'y': 3.48},
    'B1-7': {'x': -49.233, 'y': 3.48},
    'B1-5': {'x': -41.508, 'y': 3.48},
    'B1-6': {'x': -56.97, 'y': 3.48},
    'B1-8': {'x': -62.929, 'y': 3.48},
    'Emergency Exit 2': {'x': -70.977, 'y': 3.48},
    'Bathroom/M': {'x': -74.495, 'y': 3.48},
    'Prayer Room/M': {'x': -81.424, 'y': 3.48},
    'B1-9': {'x': -83.442, 'y': 3.48},
}

# ============================================================================
# TRAFFIC DATA - Real student/people counts per time period
# ============================================================================

# Pixel coordinates mapped to classroom names
CLASSROOM_COORDS = {
    'B1-1': (388, 1012),
    'B1-2': (380, 1176),
    'B1-3': (376, 1388),
    'B1-4': (108, 1384),    
    'B1-5': (96, 1200),
    'B1-6': (108, 972),
    'B1-7': (84, 780),
    'B1-8': (1016, 2016),
    'B1-9': (1012, 1744),
    'B0-1': (1268, 2020),
    'Reception': (1308, 1748),
}

PRAYER_ROOM_COORDS = {
    'Prayer Room/M': (100, 1820),
    'Prayer Room/F': (104, 344),
}

# Student counts per classroom per time period
# Time periods: 0=4:00-5:30, 1=5:30-6:00(break), 2=6:00-7:00, 3=7:00-7:30(break), 4=7:30-9:00, 5=9:00-10:00(end)
CLASSROOM_STUDENTS = {
    'B1-1': [28, 0, 25, 0, 22, 5],      # Full class -> empty during breaks -> fewer at end
    'B1-2': [32, 0, 30, 0, 28, 8],
    'B1-3': [25, 0, 28, 0, 25, 6],
    'B1-4': [30, 0, 32, 0, 30, 10],
    'B1-5': [22, 0, 20, 0, 18, 4],
    'B1-6': [35, 0, 33, 0, 30, 12],
    'B1-7': [28, 0, 26, 0, 24, 8],
    'B1-8': [20, 0, 22, 0, 20, 5],
    'B1-9': [18, 0, 20, 0, 18, 3],
    'B0-1': [15, 0, 18, 0, 15, 2],      # Ground floor class
    'Reception': [3, 5, 3, 5, 3, 8],    # Reception staff + visitors
}

# People in prayer rooms per time period (peaks during breaks for prayer times)
PRAYER_ROOM_PEOPLE = {
    'Prayer Room/M': [5, 80, 8, 85, 10, 25],   # Low during class, high during breaks (prayer times)
    'Prayer Room/F': [3, 45, 5, 50, 6, 15],
}

# Hallway traffic multiplier per time period (people per hallway segment)
# Higher during breaks when students move between classes
HALLWAY_TRAFFIC = [2, 15, 3, 18, 2, 8]  # per segment: low during class, high during breaks

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_poi_dataframe(floor_pois, floor_name):
    """Create a DataFrame from POI dictionary."""
    data = []
    for name, coords in floor_pois.items():
        category = categorize_poi(name)
        cat_info = POI_CATEGORIES[category]
        data.append({
            'name': name,
            'x': coords['x'],
            'y': coords['y'],
            'floor': floor_name,
            'category': category,
            'icon': cat_info['icon'],
            'color': cat_info['color'],
            'display_name': f"{cat_info['icon']} {name}"
        })
    return pd.DataFrame(data)

def calculate_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)

def calculate_walking_time(distance, speed=1.4):
    """Calculate walking time in seconds (speed in m/s)."""
    return distance / speed

def format_time(seconds):
    """Format seconds into readable time string."""
    if seconds < 60:
        return f"{seconds:.0f} seconds"
    else:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"

def find_nearest_facility(current_location, facility_type, all_pois_df):
    """Find the nearest facility of a given type from current location."""
    current_poi = all_pois_df[all_pois_df['name'] == current_location].iloc[0]

    # Filter facilities by type
    if facility_type == 'Bathroom (Male)':
        facilities = all_pois_df[all_pois_df['name'].str.contains('Bathroom/M', case=False)]
    elif facility_type == 'Bathroom (Female)':
        facilities = all_pois_df[all_pois_df['name'].str.contains('Bathroom/F', case=False)]
    elif facility_type == 'Emergency Exit':
        facilities = all_pois_df[all_pois_df['name'].str.contains('Emergency', case=False)]
    elif facility_type == 'Prayer Room (Male)':
        facilities = all_pois_df[all_pois_df['name'].str.contains('Prayer Room/M', case=False)]
    elif facility_type == 'Prayer Room (Female)':
        facilities = all_pois_df[all_pois_df['name'].str.contains('Prayer Room/F', case=False)]
    elif facility_type == 'Elevator':
        facilities = all_pois_df[all_pois_df['name'].str.contains('Elevator', case=False)]
    elif facility_type == 'Food':
        facilities = all_pois_df[all_pois_df['name'].str.contains('Cafeteria|Dunkin|Sandwich|Subway|Maps', case=False, regex=True)]
    else:
        facilities = all_pois_df[all_pois_df['category'] == facility_type]

    if facilities.empty:
        return None, None

    min_distance = float('inf')
    nearest = None

    for _, facility in facilities.iterrows():
        dist = calculate_distance(
            {'x': current_poi['x'], 'y': current_poi['y']},
            {'x': facility['x'], 'y': facility['y']}
        )
        if dist < min_distance and facility['name'] != current_location:
            min_distance = dist
            nearest = facility

    return nearest, min_distance

def calculate_centrality(pois_df):
    """Calculate the most central location (closest to all other points on average)."""
    coords = pois_df[['x', 'y']].values
    distances = cdist(coords, coords)
    avg_distances = distances.mean(axis=1)
    central_idx = avg_distances.argmin()
    return pois_df.iloc[central_idx], avg_distances[central_idx]

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_category_breakdown(pois_df, title="POI Categories"):
    """Create a pie chart of POI categories."""
    category_counts = pois_df['category'].value_counts()
    colors = [POI_CATEGORIES[cat]['color'] for cat in category_counts.index]
    labels = [f"{POI_CATEGORIES[cat]['icon']} {POI_CATEGORIES[cat]['label']}" for cat in category_counts.index]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=category_counts.values,
        hole=0.4,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textinfo='percent+label',
        textfont=dict(size=12, color='white')
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='white')),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig

def create_accessibility_chart(pois_df, elevator_locations):
    """Create a bar chart showing distance from elevator for each POI."""
    distances = []
    for _, poi in pois_df.iterrows():
        min_dist = float('inf')
        for elev in elevator_locations:
            dist = calculate_distance(
                {'x': poi['x'], 'y': poi['y']},
                {'x': elev['x'], 'y': elev['y']}
            )
            min_dist = min(min_dist, dist)
        distances.append(min_dist)

    pois_df = pois_df.copy()
    pois_df['elevator_distance'] = distances
    pois_df_sorted = pois_df.sort_values('elevator_distance', ascending=True)

    fig = go.Figure(data=[go.Bar(
        x=pois_df_sorted['name'],
        y=pois_df_sorted['elevator_distance'],
        marker=dict(
            color=pois_df_sorted['elevator_distance'],
            colorscale='RdYlGn_r',
            showscale=True,
            colorbar=dict(title='Distance (m)')
        )
    )])

    fig.update_layout(
        title=dict(text='Distance from Nearest Elevator', font=dict(size=18, color='white')),
        xaxis=dict(
            title=dict(text='Location', font=dict(color='white')),
            tickangle=45,
            tickfont=dict(size=8, color='white')
        ),
        yaxis=dict(
            title=dict(text='Distance (meters)', font=dict(color='white')),
            tickfont=dict(color='white')
        ),
        plot_bgcolor='rgba(26, 26, 46, 0.9)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        height=400,
        margin=dict(l=50, r=50, t=60, b=120)
    )

    return fig

# ============================================================================
# HEATMAP INTEGRATION (from heatmap_timeline_v2.py)
# ============================================================================

def get_heatmap_periods():
    """Return the list of time periods for the heatmap."""
    return [
        "4:00-5:30 PM (Classes)",
        "5:30-6:00 PM (Break - Hallways & Prayer)",
        "6:00-7:00 PM (Classes)",
        "7:00-7:30 PM (Break - Hallways & Prayer)",
        "7:30-9:00 PM (Classes)",
        "9:00-10:00 PM (End of Day)",
    ]


def generate_heatmap_html(period_index=0):
    """
    Generate the heatmap HTML using Folium for a specific time period.

    Args:
        period_index: Index of the time period (0-5)
    """
    # Load the floor plan image
    img_path = "data/floor1.png"
    img = Image.open(img_path)
    W, H = img.size

    # Build heatmap data from real student/people counts
    heatmap_data = []

    # Add classroom data with actual student counts
    for name, coords in CLASSROOM_COORDS.items():
        students = CLASSROOM_STUDENTS[name][period_index]
        if students > 0:
            # Add point with student count as weight
            heatmap_data.append([coords[0], coords[1], students])

    # Add prayer room data with actual people counts
    for name, coords in PRAYER_ROOM_COORDS.items():
        people = PRAYER_ROOM_PEOPLE[name][period_index]
        if people > 0:
            heatmap_data.append([coords[0], coords[1], people])

    # Create hallway points with traffic data
    hallway_traffic = HALLWAY_TRAFFIC[period_index]

    # Hallway 1 (vertical corridor)
    y_points = np.linspace(1356, 244, 30)
    x_points = np.linspace(1896, 1876, 30)
    for y, x in zip(y_points, x_points):
        heatmap_data.append([int(y), int(x), hallway_traffic])

    # Hallway 2 (horizontal corridor)
    y_points = np.linspace(244, 264, 30)
    x_points = np.linspace(1876, 376, 30)
    for y, x in zip(y_points, x_points):
        heatmap_data.append([int(y), int(x), hallway_traffic])
    # zoom = -3
    # Create the base map
    m = folium.Map(
        
        crs="Simple",
        zoom_control=False,
        min_zoom=-5,
        max_zoom= 5
        # scrollWheelZoom=True
    )

    bounds = [[0, 0], [H, W]]

    ImageOverlay(
        img_path,
        bounds=bounds,
        opacity=1.0,
        interactive=True
    ).add_to(m)

    m.fit_bounds(bounds)

    # Add the heatmap for the selected period
    HeatMap(
        heatmap_data,
        radius=15,
        blur=10,
        min_opacity=0.3,
        max_opacity=0.8,
        gradient={
            0.0: '#6C63FF',
            0.3: '#4ECDC4',
            0.5: '#FFE66D',
            0.7: '#FF9F43',
            1.0: '#FF6B6B'
        }
    ).add_to(m)

    # Add CSS for map styling
    map_css = """
<style>
    .folium-map {
        border-radius: 10px;
        overflow: hidden;
        # transform: rotate(90deg)
    }
</style>
"""
    m.get_root().html.add_child(folium.Element(map_css))

    return m._repr_html_()


def get_cluster_analysis(period_index=0, n_clusters=3):
    """
    Perform KMeans clustering on the heatmap data for a specific time period.

    Args:
        period_index: Index of the time period (0-5)
        n_clusters: Number of clusters to identify

    Returns:
        cluster_centers: Array of cluster center coordinates
        cluster_labels: Array of cluster labels for each point
        points_data: The weighted points data used for clustering
        closest_pois: List of closest POI names for each cluster
    """
    # Build data from real student/people counts (same as heatmap)
    current_data = []

    # Add classroom data with actual student counts
    for name, coords in CLASSROOM_COORDS.items():
        students = CLASSROOM_STUDENTS[name][period_index]
        if students > 0:
            current_data.append([coords[0], coords[1], students])

    # Add prayer room data with actual people counts
    for name, coords in PRAYER_ROOM_COORDS.items():
        people = PRAYER_ROOM_PEOPLE[name][period_index]
        if people > 0:
            current_data.append([coords[0], coords[1], people])

    # Create hallway points with traffic data
    hallway_traffic = HALLWAY_TRAFFIC[period_index]

    # Hallway 1 (vertical corridor)
    y_points = np.linspace(1356, 244, 30)
    x_points = np.linspace(1896, 1876, 30)
    for y, x in zip(y_points, x_points):
        current_data.append([int(y), int(x), hallway_traffic])

    # Hallway 2 (horizontal corridor)
    y_points = np.linspace(244, 264, 30)
    x_points = np.linspace(1876, 376, 30)
    for y, x in zip(y_points, x_points):
        current_data.append([int(y), int(x), hallway_traffic])

    # Extract coordinates for clustering
    coordinates = np.array([[point[0], point[1]] for point in current_data])
    weights = np.array([point[2] for point in current_data])

    # Apply KMeans clustering with sample weights
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(coordinates, sample_weight=weights)

    # Find closest POI for each cluster center (only actual POIs, not hallways)
    def get_closest_poi(center):
        min_dist = float('inf')
        closest_name = "Unknown"

        # Check classrooms
        for name, coords in CLASSROOM_COORDS.items():
            dist = np.sqrt((center[0] - coords[0])**2 + (center[1] - coords[1])**2)
            if dist < min_dist:
                min_dist = dist
                closest_name = name

        # Check prayer rooms
        for name, coords in PRAYER_ROOM_COORDS.items():
            dist = np.sqrt((center[0] - coords[0])**2 + (center[1] - coords[1])**2)
            if dist < min_dist:
                min_dist = dist
                closest_name = name

        return closest_name

    closest_pois = [get_closest_poi(center) for center in kmeans.cluster_centers_]

    return kmeans.cluster_centers_, kmeans.labels_, current_data, closest_pois


def generate_cluster_map_html(cluster_centers, cluster_labels, points_data):
    """
    Generate a Folium map showing cluster centers as markers.

    Args:
        cluster_centers: Array of cluster center coordinates
        cluster_labels: Array of cluster labels for each point
        points_data: The weighted points data
    """
    # Load the floor plan image
    img_path = "data/floor1.png"
    img = Image.open(img_path)
    W, H = img.size

    # Create the base map
    m = folium.Map(
        crs="Simple",
        zoom_control=False,
        min_zoom=-5,
        max_zoom=5
    )

    bounds = [[0, 0], [H, W]]

    ImageOverlay(
        img_path,
        bounds=bounds,
        opacity=1.0,
        interactive=True
    ).add_to(m)

    m.fit_bounds(bounds)

    # Cluster colors
    cluster_colors = ['#FF6B6B', '#4ECDC4', '#6C63FF', '#FFE66D', '#FF9F43']

    # Add cluster center markers
    for i, center in enumerate(cluster_centers):
        color = cluster_colors[i % len(cluster_colors)]
        cluster_points = [p for j, p in enumerate(points_data) if cluster_labels[j] == i]
        avg_weight = np.mean([p[2] for p in cluster_points]) if cluster_points else 0

        # Create styled marker with centered number
        marker_html = f'''
        <div style="
            width: 40px;
            height: 40px;
            background: {color};
            border: 3px solid white;
            border-radius: 50%;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        ">{i+1}</div>
        '''

        folium.Marker(
            location=[center[0], center[1]],
            icon=folium.DivIcon(
                html=marker_html,
                icon_size=(40, 40),
                icon_anchor=(20, 20)
            ),
            popup=f"<b>Cluster {i+1}</b><br>Points: {len(cluster_points)}<br>Avg Activity: {avg_weight:.2f}",
            tooltip=f"Cluster {i+1}"
        ).add_to(m)

    # Add CSS for map styling
    map_css = """
<style>
    .folium-map {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
"""
    m.get_root().html.add_child(folium.Element(map_css))

    return m._repr_html_()


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    load_custom_css()

    # Create DataFrames
    floor_0_df = create_poi_dataframe(FLOOR_0_POIS, 'Floor 0')
    floor_1_df = create_poi_dataframe(FLOOR_1_POIS, 'Floor 1')
    all_pois_df = pd.concat([floor_0_df, floor_1_df], ignore_index=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>Wejha</h1>
        <p>Interactive Spatial Analysis Dashboard for   <span style="font-size:1.5rem;">Tuwaiq Academy</span></p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### Navigation")
        page = st.radio(
            "Select View",
            ["Dashboard", "Route Analysis", "Nearest Facility", "Analytics", "Traffic Analysis"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Quick stats
        st.markdown("### Quick Stats")
        st.markdown(f"""
        <div class="info-box">
            <strong>Total POIs:</strong> {len(all_pois_df)}<br>
            <strong>Floor 0:</strong> {len(floor_0_df)} locations<br>
            <strong>Floor 1:</strong> {len(floor_1_df)} locations
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### About Wejha")
        st.markdown("""
        <div style='font-size: 0.9rem; color: #888;'>
        Wejha is an advance indoors AR navigation system that uses VPS Technology.\n 
        This dashboard is intended for the administrators to help them understand the layout, the best routes, 
        and the traffic of the building
        </div>
        """, unsafe_allow_html=True)

    # Use all POIs
    display_df = all_pois_df

    # ========================================================================
    # DASHBOARD VIEW
    # ========================================================================
    if page == "Dashboard":
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(all_pois_df)}</div>
                <div class="metric-label">Total Locations</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            classrooms = len(all_pois_df[all_pois_df['category'] == 'classroom'])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{classrooms}</div>
                <div class="metric-label">Classrooms</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            amenities = len(all_pois_df[all_pois_df['category'] == 'amenity'])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{amenities}</div>
                <div class="metric-label">Amenities</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            facilities = len(all_pois_df[all_pois_df['category'].isin(['facility', 'emergency', 'prayer_rooms'])])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{facilities}</div>
                <div class="metric-label">Facilities</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Category breakdown
        with st.container():
            st.markdown('<p class="section-header">POI Categories</p>', unsafe_allow_html=True)
            fig_pie = create_category_breakdown(display_df)
            st.plotly_chart(fig_pie, width='stretch')

            # Category legend
            st.markdown("**Legend:**")
            for category, info in POI_CATEGORIES.items():
                count = len(display_df[display_df['category'] == category])
                if count > 0:
                    st.markdown(f"{info['icon']} **{info['label']}**: {count}")

    # ========================================================================
    # ROUTE ANALYSIS VIEW
    # ========================================================================
    elif page == "Route Analysis":
        st.markdown('<p class="section-header">Route Analysis</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            start_point = st.selectbox(
                "Starting Point",
                options=display_df['display_name'].tolist(),
                key="start"
            )

        with col2:
            end_point = st.selectbox(
                "Destination",
                options=display_df['display_name'].tolist(),
                key="end"
            )

        if st.button("Calculate Route", width='stretch'):
            start_name = start_point.split(' ', 1)[1]  # Remove emoji prefix
            end_name = end_point.split(' ', 1)[1]

            start_poi = display_df[display_df['name'] == start_name].iloc[0]
            end_poi = display_df[display_df['name'] == end_name].iloc[0]

            distance = calculate_distance(
                {'x': start_poi['x'], 'y': start_poi['y']},
                {'x': end_poi['x'], 'y': end_poi['y']}
            )
            walking_time = calculate_walking_time(distance)

            # Results
            col_result1, col_result2, col_result3 = st.columns(3)

            with col_result1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{distance:.2f}m</div>
                    <div class="metric-label">Distance</div>
                </div>
                """, unsafe_allow_html=True)

            with col_result2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{format_time(walking_time)}</div>
                    <div class="metric-label">Walking Time</div>
                </div>
                """, unsafe_allow_html=True)

            with col_result3:
                floor_change = "Yes" if start_poi['floor'] != end_poi['floor'] else "No"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{floor_change}</div>
                    <div class="metric-label">Floor Change Required</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Route details
            change_floor_message = "<small>You dont have to change the floor when going to this destination<small>"
            st.markdown(f"""
            <div class="route-card">
                <h3>Route Details</h3>
                <p><strong>From:</strong> {start_point} ({start_poi['floor']})</p>
                <p><strong>To:</strong> {end_point} ({end_poi['floor']})</p>
                <p><strong>Distance:</strong> {distance:.2f} meters</p>
                <p><strong>Estimated Walking Time:</strong> {format_time(walking_time)} (at 1.4 m/s)</p>
            </div>
            """, unsafe_allow_html=True)

    # ========================================================================
    # NEAREST FACILITY VIEW
    # ========================================================================
    elif page == "Nearest Facility":
        st.markdown('<p class="section-header">Find Nearest Facility</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            current_location = st.selectbox(
                "Your Current Location",
                options=all_pois_df['display_name'].tolist()
            )

        with col2:
            facility_type = st.selectbox(
                "Facility Type",
                options=['Bathroom (Male)', 'Bathroom (Female)', 'Prayer Room (Male)', 'Prayer Room (Female)', 'Elevator', 'Emergency Exit', 'Food']
            )

        if st.button("Find Nearest", width='stretch'):
            current_name = current_location.split(' ', 1)[1]
            nearest, distance = find_nearest_facility(current_name, facility_type, all_pois_df)
            
            if nearest is not None:
                walking_time = calculate_walking_time(distance)

                col_r1, col_r2 = st.columns(2)

                with col_r1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{nearest['icon']} {nearest['name']}</div>
                        <div class="metric-label">Nearest {facility_type}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col_r2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{distance:.2f}m</div>
                        <div class="metric-label">Distance ({format_time(walking_time)})</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f"No {facility_type} found.")

    # ========================================================================
    # ANALYTICS VIEW
    # ========================================================================
    elif page == "Analytics":
        st.markdown('<p class="section-header">Spatial Analytics</p>', unsafe_allow_html=True)

        # Centrality Analysis
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Most Central Location")

            for floor_df, floor_name in [(floor_0_df, "Floor 0"), (floor_1_df, "Floor 1")]:
                central_poi, avg_dist = calculate_centrality(floor_df)
                st.markdown(f"""
                <div class="info-box">
                    <strong>{floor_name}:</strong> {central_poi['icon']} {central_poi['name']}<br>
                    <small>Avg distance: {avg_dist:.2f}m</small>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### Average Distance from Entrance")

            # Calculate average distance from entrance
            entrance = floor_0_df[floor_0_df['name'] == 'Entrance'].iloc[0]
            distances = []
            for _, poi in all_pois_df.iterrows():
                dist = calculate_distance(
                    {'x': entrance['x'], 'y': entrance['y']},
                    {'x': poi['x'], 'y': poi['y']}
                )
                distances.append(dist)

            avg_from_entrance = np.mean(distances)
            max_from_entrance = np.max(distances)
            farthest_poi = all_pois_df.iloc[np.argmax(distances)]

            st.markdown(f"""
            <div class="route-card">
                <h3>Distance Statistics</h3>
                <p><strong>Average:</strong> {avg_from_entrance:.2f}m</p>
                <p><strong>Maximum:</strong> {max_from_entrance:.2f}m</p>
                <p><strong>Farthest POI:</strong> {farthest_poi['icon']} {farthest_poi['name']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Accessibility Analysis
        st.markdown("#### Accessibility Analysis (Elevator Proximity)")

        elevator_locations = [
            {'x': FLOOR_0_POIS['Elevator']['x'], 'y': FLOOR_0_POIS['Elevator']['y']},
            {'x': FLOOR_1_POIS['Elevator 2']['x'], 'y': FLOOR_1_POIS['Elevator 2']['y']}
        ]

        fig_access = create_accessibility_chart(display_df, elevator_locations)
        st.plotly_chart(fig_access, width='stretch')

        # Emergency Exit Coverage
        st.markdown("#### Emergency Exit Coverage")

        emergency_exits = all_pois_df[all_pois_df['name'].str.contains('Emergency', case=False)]

        col_e1, col_e2 = st.columns(2)

        with col_e1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(emergency_exits)}</div>
                <div class="metric-label">Emergency Exits</div>
            </div>
            """, unsafe_allow_html=True)

        with col_e2:
            # Calculate average distance to nearest emergency exit
            exit_distances = []
            for _, poi in all_pois_df.iterrows():
                min_dist = float('inf')
                for _, exit_poi in emergency_exits.iterrows():
                    dist = calculate_distance(
                        {'x': poi['x'], 'y': poi['y']},
                        {'x': exit_poi['x'], 'y': exit_poi['y']}
                    )
                    min_dist = min(min_dist, dist)
                exit_distances.append(min_dist)

            avg_exit_dist = np.mean(exit_distances)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_exit_dist:.1f}m</div>
                <div class="metric-label">Avg. Distance to Exit</div>
            </div>
            """, unsafe_allow_html=True)

    # ========================================================================
    # TRAFFIC ANALYSIS VIEW
    # ========================================================================
    elif page == "Traffic Analysis":
        st.markdown('<p class="section-header">Traffic Analysis</p>', unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
            <strong>About this visualization:</strong> This heatmap shows the estimated foot traffic
            patterns throughout the day at Tuwaiq Academy. Use the slider to explore different time periods.
        </div>
        """, unsafe_allow_html=True)

        # Time period selector (outside iframe)
        periods = get_heatmap_periods()
        selected_period = st.select_slider(
            "Select Time Period",
            options=periods,
            value=periods[0]
        )
        period_index = periods.index(selected_period)

        # Generate and display heatmap for selected period
        heatmap_html = generate_heatmap_html(period_index)

        # Display in iframe
        st.components.v1.html(heatmap_html, height=650, scrolling=False)

        # Clustering Analysis Section
        st.markdown("---")
        st.markdown("#### Cluster Analysis")
        st.markdown("""
        <div class="info-box">
            <strong>About clustering:</strong> KMeans clustering identifies high-density areas
            based on the current time period's activity patterns. Each cluster center represents
            a hotspot of activity.
        </div>
        """, unsafe_allow_html=True)

        # Get cluster data for the selected period
        cluster_centers, cluster_labels, points_data, closest_pois = get_cluster_analysis(period_index)

        # Display cluster metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(cluster_centers)}</div>
                <div class="metric-label">Identified Clusters</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(points_data)}</div>
                <div class="metric-label">Total Data Points</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            # Find the cluster with highest average weight
            cluster_weights = []
            for i in range(len(cluster_centers)):
                cluster_points = [p for j, p in enumerate(points_data) if cluster_labels[j] == i]
                avg_weight = np.mean([p[2] for p in cluster_points]) if cluster_points else 0
                cluster_weights.append(avg_weight)
            hottest_cluster = np.argmax(cluster_weights) + 1

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">Cluster {hottest_cluster}</div>
                <div class="metric-label">Highest Activity</div>
            </div>
            """, unsafe_allow_html=True)

        # Display cluster details
        st.markdown("#### Cluster Centers")

        cluster_colors = ['#FF6B6B', '#4ECDC4', '#6C63FF', '#FFE66D', '#FF9F43']

        cols = st.columns(len(cluster_centers))
        for i in range(len(cluster_centers)):
            with cols[i]:
                color = cluster_colors[i % len(cluster_colors)]
                cluster_points = [p for j, p in enumerate(points_data) if cluster_labels[j] == i]

                st.markdown(f"""
                <div style="background: {color}20; border: 2px solid {color};
                            padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 1rem">
                    <div style="font-size: 1.5rem; font-weight: bold; color: {color};">Cluster {i+1}</div>
                    <div style="color: #888; font-size: 0.9rem;">
                        Points: {len(cluster_points)}<br>
                        Closest POI: {closest_pois[i]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Button to show cluster map
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Show Clusters on Map", use_container_width=True):
            st.markdown("#### Cluster Locations")
            cluster_map_html = generate_cluster_map_html(cluster_centers, cluster_labels, points_data)
            st.components.v1.html(cluster_map_html, height=650, scrolling=False)

if __name__ == "__main__":
    main()
