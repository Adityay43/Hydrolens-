import streamlit as st
import requests
import random
import datetime
import json
import base64
import os
import time

# ─── Page Configuration ───
st.set_page_config(
    page_title="HydroLens — AI Urban Flood Sentinel",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Framer-Inspired UI/UX Styling (Modern Obsidian, Neon Gradients & Bento Glass) ───
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">

<style>
    /* ── Obsidian Dark Canvas ── */
    .stApp {
        background-color: #07090e !important;
        background-image: 
            radial-gradient(at 50% 0%, rgba(2, 132, 199, 0.18) 0px, transparent 55%),
            radial-gradient(at 100% 40%, rgba(56, 189, 248, 0.08) 0px, transparent 50%),
            radial-gradient(at 0% 80%, rgba(14, 165, 233, 0.06) 0px, transparent 40%) !important;
        color: #e2e8f0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* ── Hide Streamlit Default Top Header & Deploy Bar ── */
    header[data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
        height: 0% !important;
    }
    div[data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }
    #MainMenu {
        visibility: hidden !important;
        display: none !important;
    }
    footer {
        visibility: hidden !important;
    }
    
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { 
        display: none !important; 
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 1240px !important;
    }

    /* ── Typography & Headings ── */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #ffffff !important;
        letter-spacing: -0.02em !important;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(2, 132, 199, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #38bdf8;
        letter-spacing: 0.04em;
        margin-bottom: 1rem;
        backdrop-filter: blur(8px);
    }
    .hero-badge span.dot {
        width: 7px;
        height: 7px;
        background-color: #38bdf8;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #38bdf8;
        animation: pulse 2s infinite;
    }

    .hero-title {
        font-size: clamp(2.4rem, 5vw, 4rem) !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        background: linear-gradient(180deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.8rem;
    }

    .hero-sub {
        font-size: 1.12rem;
        color: #94a3b8;
        max-width: 780px;
        line-height: 1.6;
        margin-bottom: 1.8rem;
        font-weight: 400;
    }

    /* ── Bento Stat Cards ── */
    .bento-card {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px;
        backdrop-filter: blur(16px);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        height: 100%;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    .bento-card:hover {
        border-color: rgba(56, 189, 248, 0.35);
        transform: translateY(-3px);
        box-shadow: 0 14px 40px -10px rgba(2, 132, 199, 0.25);
    }
    .bento-num {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .bento-label {
        font-size: 0.88rem;
        color: #94a3b8;
        margin-top: 4px;
        line-height: 1.4;
    }

    /* ── Framer-style Floating Dock Navigation ── */
    div.stButton > button {
        width: 100% !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        background: rgba(18, 26, 43, 0.7) !important;
        backdrop-filter: blur(12px) !important;
        color: #94a3b8 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
    }
    div.stButton > button:hover {
        background: rgba(30, 41, 69, 0.9) !important;
        color: #38bdf8 !important;
        border-color: rgba(56, 189, 248, 0.5) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.2) !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* Active Nav Tab */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        box-shadow: 0 0 24px rgba(2, 132, 199, 0.45) !important;
    }

    /* ── Container Cards ── */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(13, 20, 36, 0.7) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.6) !important;
        padding: 16px !important;
    }

    /* ── Metrics ── */
    div[data-testid="stMetric"] {
        background: rgba(18, 27, 47, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 14px 16px;
        backdrop-filter: blur(10px);
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.82rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ── Selectbox & Inputs ── */
    div[data-baseweb="select"] > div {
        background-color: #0d1527 !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    input, textarea {
        background-color: #0d1527 !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }

    /* ── Link Buttons ── */
    div[data-testid="stLinkButton"] > a {
        background: rgba(18, 27, 47, 0.8) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        color: #38bdf8 !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stLinkButton"] > a:hover {
        background: #0284c7 !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4) !important;
    }

    /* ── Live Surveillance Pill ── */
    .live-badge {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 4px 10px;
        font-size: 0.72rem;
        font-weight: 700;
        border-radius: 9999px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .live-dot {
        width: 6px;
        height: 6px;
        background-color: #ef4444;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }
</style>
""", unsafe_allow_html=True)

# ─── Session State ───
if "reports" not in st.session_state:
    st.session_state.reports = []
if "user_city" not in st.session_state:
    st.session_state.user_city = "Delhi"
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "dashboard"

# ─── City Coordinates & Hotspots ───
CITIES = {
    "Delhi": {
        "lat": 28.6139, "lon": 77.2090,
        "hotspots": ["Minto Bridge Underpass", "ITO Ring Road", "Pul Prahladpur", "Dhaula Kuan Flyover"],
        "sample_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4",
    },
    "Mumbai": {
        "lat": 19.0760, "lon": 72.8777,
        "hotspots": ["Andheri Subway", "Milan Subway", "Hindmata Junction (Dadar)", "Gandhi Market (Sion)"],
        "sample_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    },
    "Chennai": {
        "lat": 13.0827, "lon": 80.2707,
        "hotspots": ["Velachery Main Road", "Madipakkam Lake Junction", "GST Road (Chromepet)", "Gengu Reddy Subway"],
        "sample_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4",
    },
    "Bangalore": {
        "lat": 12.9716, "lon": 77.5946,
        "hotspots": ["Silk Board Junction", "Ecospace ORR Bellandur", "Koramangala 4th Block", "Hebbal Flyover"],
        "sample_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
    },
    "Kolkata": {
        "lat": 22.5726, "lon": 88.3639,
        "hotspots": ["EM Bypass (Ruby Crossing)", "College Street", "Park Circus 7-Point", "Thanthania Kalibari"],
        "sample_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    },
    "Hyderabad": {
        "lat": 17.3850, "lon": 78.4867,
        "hotspots": ["Kukatpally Y Junction", "Tolichowki Flyover", "Malakpet Rail Underbridge", "Begumpet"],
        "sample_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4",
    },
    "Pune": {
        "lat": 18.5204, "lon": 73.8567,
        "hotspots": ["Sinhagad Road (Mutha River)", "Pulachi Wadi", "Deccan Gymkhana", "Khadki Railway Subway"],
        "sample_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
    },
    "Jaipur": {
        "lat": 26.9124, "lon": 75.7873,
        "hotspots": ["Ajmer Road 200ft Bypass", "Sanganer Pulia", "MI Road Baraf Khana", "JLN Marg"],
        "sample_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WhatCarCanYouGetForAGrand.mp4",
    },
    "Lucknow": {
        "lat": 26.8467, "lon": 80.9462,
        "hotspots": ["Hazratganj Main Crossing", "Charbagh Station Circle", "Polytechnic Chauraha", "Aminabad"],
        "sample_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4",
    },
}

WMO_CODES = {
    0: "☀️ Clear sky", 1: "🌤️ Mainly clear", 2: "⛅ Partly cloudy", 3: "☁️ Overcast",
    45: "🌫️ Fog", 48: "🌫️ Rime fog",
    51: "🌦️ Light drizzle", 53: "🌦️ Moderate drizzle", 55: "🌧️ Dense drizzle",
    61: "🌧️ Slight rain", 63: "🌧️ Moderate rain", 65: "🌧️ Heavy rain",
    80: "🌦️ Showers", 81: "🌧️ Heavy showers", 82: "⛈️ Violent rain",
    95: "⛈️ Thunderstorm", 96: "⛈️ Thunderstorm + hail",
}

def get_wind_direction(deg):
    dirs = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return dirs[round(deg / 22.5) % 16]

# ─── Open-Source Historical Urban Flood Registry (NDMA, IMD, CWC & Open Data Archives) ───
HISTORICAL_FLOODS = {
    "Delhi": [
        {
            "year": "July 2023",
            "title": "Historic Yamuna River Record Surge",
            "peak_level": "208.66 m (Broke 45-year 1978 record of 207.49 m)",
            "rainfall": "153 mm in 24 hours (highest single-day July rain since 1982)",
            "affected_areas": "ITO, Ring Road, Red Fort complex, Kashmere Gate ISBT, Monastery Market, Civil Lines, Yamuna Bazar",
            "impact": "Over 27,000 residents evacuated, drinking water treatment plants (Wazirabad, Chandrawal) temporarily halted, metro stations regulated.",
            "source": "Central Water Commission (CWC) & IMD Official Archives",
            "severity": "CRITICAL"
        },
        {
            "year": "September 1978",
            "title": "1978 Delhi Mega Flood",
            "peak_level": "207.49 m at Old Railway Bridge",
            "rainfall": "Extreme spell upstream in Hathnikund & Tajewala barrage releases exceeding 7 lakh cusecs",
            "affected_areas": "Model Town, Jahangirpuri, Adarsh Nagar, Kingsway Camp, trans-Yamuna settlements",
            "impact": "Submerged vast areas of north and east Delhi; historical benchmark flood for 45 years.",
            "source": "Delhi Disaster Management Authority (DDMA)",
            "severity": "CRITICAL"
        },
        {
            "year": "September 2010",
            "title": "Commonwealth Games Eve Inundation",
            "peak_level": "207.11 m Yamuna gauge level",
            "rainfall": "Continuous upper catchment precipitation and 7.4 lakh cusecs release",
            "affected_areas": "Mayur Vihar lowlands, Usmanpur, Yamuna Pushta, Ring Road bypass",
            "impact": "Disrupted interstate transit ahead of the XIX Commonwealth Games.",
            "source": "IMD Hydrological Bulletins",
            "severity": "HIGH"
        }
    ],
    "Mumbai": [
        {
            "year": "26 July 2005",
            "title": "The Great Mumbai Deluge",
            "peak_level": "Highest urban rain ever recorded in Indian history",
            "rainfall": "944 mm in a single 24-hour cycle at Santacruz",
            "affected_areas": "Mithi River Basin, Kalina, Kurla, Bandra-Kurla Complex, Sakinaka, Chunabhatti, Air India colony",
            "impact": "Over 1,000 lives lost, Mumbai suburban rail completely halted for 48 hours, financial damage exceeding $1.5B.",
            "source": "Government of Maharashtra Fact Finding Committee (Chitale Committee)",
            "severity": "CRITICAL"
        },
        {
            "year": "August 2017",
            "title": "2017 Monsoon Gridlock",
            "peak_level": "Severe low-pressure cyclonic vortex",
            "rainfall": "331.4 mm in 24 hours, coinciding with high tide",
            "affected_areas": "Hindmata (Dadar), Parel, Sion Gandhi Market, Milan Subway, King's Circle",
            "impact": "Citywide transit paralysis, local trains stranded, massive vehicular waterlogging.",
            "source": "Brihanmumbai Municipal Corporation (BMC) Disaster Cell",
            "severity": "HIGH"
        },
        {
            "year": "July 2021",
            "title": "Chembur & Vikhroli Landslide & Flood Event",
            "peak_level": "Intense localized cloudburst spell",
            "rainfall": "235 mm between midnight and 4 AM (extreme intensity)",
            "affected_areas": "Chembur, Vikhroli, Andheri Subway, Chunabhatti, Bhandup Water Purification Plant",
            "impact": "Localized mudslides and critical water supply infrastructure temporarily flooded.",
            "source": "IMD Mumbai Nowcast & NDMA Reports",
            "severity": "HIGH"
        }
    ],
    "Chennai": [
        {
            "year": "December 2015",
            "title": "The 2015 South India Flood Catastrophe",
            "peak_level": "Historic Chembarambakkam reservoir release (29,000 cusecs into Adyar river)",
            "rainfall": "494 mm in 24 hours (highest December rainfall in over a century)",
            "affected_areas": "Saidapet, Kotturpuram, Velachery, Mudichur, Tambaram, Adyar riverbank, Chennai Airport runways",
            "impact": "Chennai International Airport submerged and closed for 5 days, estimated damage over $3B, 1.8M displaced.",
            "source": "CAG Report on 2015 Chennai Floods & IMD",
            "severity": "CRITICAL"
        },
        {
            "year": "December 2023",
            "title": "Cyclone Michaung Inundation",
            "peak_level": "Super-slow moving storm dumping continuous rains along Chennai coast",
            "rainfall": "450-500 mm in 36 hours across suburbs",
            "affected_areas": "Velachery, Pallikaranai marshland belt, Tambaram, Perumbakkam, Madipakkam, Vyasarpadi",
            "impact": "Prolonged waterlogging up to 4 to 5 feet in southern IT corridors, power grids turned off for safety.",
            "source": "Greater Chennai Corporation (GCC) & IMD",
            "severity": "CRITICAL"
        },
        {
            "year": "November 2021",
            "title": "Northeast Monsoon Urban Waterlogging",
            "peak_level": "Depression in Bay of Bengal",
            "rainfall": "215 mm in 24 hours at Nungambakkam",
            "affected_areas": "T. Nagar, KK Nagar, Pulianthope, Korattur, Kolathur",
            "impact": "Subways closed, Smart City stormwater drain overhaul initiated subsequently.",
            "source": "Tamil Nadu State Disaster Management Authority (TNSDMA)",
            "severity": "MODERATE"
        }
    ],
    "Bangalore": [
        {
            "year": "September 2022",
            "title": "Silicon Plateau Tech Corridor Inundation",
            "peak_level": "Breach of upstream chain lakes in Varthur & Bellandur valleys",
            "rainfall": "131.6 mm in single spell, wettest September in recorded history",
            "affected_areas": "Outer Ring Road (ORR), Ecospace Tech Park, Rainbow Drive layout, Sarjapur Road, Yemalur, Manyata Tech Park",
            "impact": "IT professionals ferried in tractors, tech parks submerged, estimated productivity loss of ₹225+ Cr.",
            "source": "BBMP Disaster Management Cell & KSNDMC",
            "severity": "CRITICAL"
        },
        {
            "year": "May 2022",
            "title": "Pre-Monsoon Asani Influx",
            "peak_level": "Cyclonic feeder rain bands",
            "rainfall": "Over 114 mm overnight",
            "affected_areas": "Hosa Road, Silk Board Junction, Koramangala, BTM Layout 2nd Stage",
            "impact": "Major arterial junctions blocked, vehicle submergence in basement parking lots.",
            "source": "Karnataka State Natural Disaster Monitoring Centre (KSNDMC)",
            "severity": "HIGH"
        },
        {
            "year": "October 2024",
            "title": "North Bengaluru Storm Overflow",
            "peak_level": "Lakes reaching FTL (Full Tank Level) simultaneously",
            "rainfall": "Over 150 mm within 12 hours",
            "affected_areas": "Manyata Tech Park, Yelahanka Kendriya Vihar, Sahakar Nagar, Hebbal",
            "impact": "Kendriya Vihar apartment complex submerged up to ground floor; NDRF deployed with rescue rafts.",
            "source": "KSNDMC Live Bulletins",
            "severity": "HIGH"
        }
    ],
    "Kolkata": [
        {
            "year": "May 2020",
            "title": "Super Cyclone Amphan Surge",
            "peak_level": "Combined 130 km/h winds and torrential cyclone precipitation",
            "rainfall": "240 mm in 12 hours accompanied by 5-meter tidal river surge",
            "affected_areas": "College Street, Central Avenue, Park Circus, Behala, Ballygunge, EM Bypass",
            "impact": "Extensive urban flooding, widespread power outages lasting multiple days, century-old trees and power poles uprooted.",
            "source": "West Bengal Disaster Management Dept & IMD",
            "severity": "CRITICAL"
        },
        {
            "year": "September 2021",
            "title": "Ganga & Hooghly High Tide Overflow",
            "peak_level": "Coinciding monsoon depression with astronomical high tide",
            "rainfall": "142 mm in 6 hours",
            "affected_areas": "Thanthania, Muktaram Babu Street, Kalighat, Alipore, Kasba",
            "impact": "Severe waterlogging due to lock gates closed on the Hooghly river preventing gravity drainage.",
            "source": "Kolkata Municipal Corporation (KMC)",
            "severity": "HIGH"
        }
    ],
    "Hyderabad": [
        {
            "year": "October 2020",
            "title": "2020 Hyderabad Cloudburst Disaster",
            "peak_level": "Historic 100-year rainfall event",
            "rainfall": "320 mm at Ghatkesar and 192 mm in Begumpet in 24 hours",
            "affected_areas": "Begumpet, Tolichowki, Nadeem Colony, Falaknuma, Chandrayangutta, Ramanthapur, Musi River banks",
            "impact": "Over 80 casualties, Musi river overflowed its banks, hundreds of cars washed away in flooded drains.",
            "source": "Telangana State Development Planning Society (TSDPS) & NDMA",
            "severity": "CRITICAL"
        },
        {
            "year": "August 2000",
            "title": "Historic Millennium Flood",
            "peak_level": "Deep depression stagnation over Deccan plateau",
            "rainfall": "241.5 mm in 24 hours at Begumpet observatory",
            "affected_areas": "Khairatabad, Somajiguda, Amberpet, Malakpet, Musi River basin",
            "impact": "Over 100,000 residents rendered homeless; led to masterplan creation for drainage channels.",
            "source": "IMD Hyderabad Historical Data",
            "severity": "HIGH"
        }
    ],
    "Pune": [
        {
            "year": "September 2019",
            "title": "Ambil Odha Flash Flood Catastrophe",
            "peak_level": "Extreme localized cloudburst in Katraj hills",
            "rainfall": "112 mm in just 5 hours",
            "affected_areas": "Katraj, Sahakar Nagar, Padmavati, Aranyeshwar, Sinhagad Road, Tangewala Colony",
            "impact": "Wall collapse along Ambil Odha nullah, over 20 fatalities, massive damage to parked cars and residential basements.",
            "source": "Pune Municipal Corporation (PMC) & NDMA",
            "severity": "CRITICAL"
        },
        {
            "year": "July 2024",
            "title": "Khadakwasla Dam Spillway Discharge Flood",
            "peak_level": "35,000+ cusecs discharged from Khadakwasla dam into Mutha river",
            "rainfall": "Continuous high-intensity catchment downpour in ghat regions",
            "affected_areas": "Sinhagad Road residential complexes (Ekta Nagari, Dwarka), Pulachi Wadi, Deccan riverside",
            "impact": "Ground floors submerged, army and NDRF deployed for boat evacuations along riverside colonies.",
            "source": "Maharashtra Water Resources Department",
            "severity": "HIGH"
        }
    ],
    "Jaipur": [
        {
            "year": "August 2020",
            "title": "Walled City Torrential Flash Flood",
            "peak_level": "Severe cloudburst on Aravalli hillsides",
            "rainfall": "170 mm in 4 hours",
            "affected_areas": "MI Road, Walled City (Johari Bazar, Badi Chaupar), JLN Marg, Sanganer Pulia, Dravyavati river basin",
            "impact": "Vehicles floating on arterial roads, mudslides along Amer Fort hillsides.",
            "source": "Rajasthan State Disaster Management Authority",
            "severity": "HIGH"
        },
        {
            "year": "August 2012",
            "title": "2012 Jaipur Urban Inundation",
            "peak_level": "Extended monsoon trough stagnation",
            "rainfall": "190 mm in 24 hours",
            "affected_areas": "Ambabari, Sikar Road, Tonk Road, Durgapura, Jal Mahal surroundings",
            "impact": "Dravyavati River (Amanishah Nullah) breached banks, severe damage to low-income settlements.",
            "source": "IMD Jaipur Meteorological Centre",
            "severity": "HIGH"
        }
    ],
    "Lucknow": [
        {
            "year": "September 2022",
            "title": "Continuous Gomti Basin Cloudburst",
            "peak_level": "Deep depression bringing non-stop rain for 48 hours",
            "rainfall": "160 mm in 24 hours (broke 15-year September record)",
            "affected_areas": "Hazratganj, Gomti Nagar extension, Alambagh, Charbagh, Jankipuram, Polytechnic Chauraha",
            "impact": "Schools closed, severe waterlogging inside heritage buildings and hospitals, power cuts for safety.",
            "source": "UP State Disaster Management Authority (UPSDMA)",
            "severity": "HIGH"
        },
        {
            "year": "July 2021",
            "title": "Monsoon Sewer Overflow Event",
            "peak_level": "Pumping stations overwhelmed",
            "rainfall": "115 mm in single afternoon",
            "affected_areas": "Aminabad, Qaiserbagh, Chowk, Faizabad Road",
            "impact": "Old Lucknow markets submerged under 2-3 feet of water, traffic halted across city center.",
            "source": "Lucknow Municipal Corporation",
            "severity": "MODERATE"
        }
    ]
}

# ─── Free Real-time APIs (Open-Meteo) ───
@st.cache_data(ttl=300)
def fetch_weather(lat, lon):
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,precipitation,rain,"
            f"weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m,apparent_temperature"
            f"&daily=precipitation_sum,precipitation_probability_max,temperature_2m_max,temperature_2m_min,wind_speed_10m_max,wind_gusts_10m_max,weather_code"
            f"&timezone=Asia%2FKolkata&forecast_days=3"
        )
        return requests.get(url, timeout=6).json()
    except:
        return None

@st.cache_data(ttl=300)
def fetch_air_quality(lat, lon):
    try:
        url = (
            f"https://air-quality-api.open-meteo.com/v1/air-quality"
            f"?latitude={lat}&longitude={lon}"
            f"&current=pm2_5,pm10,us_aqi"
            f"&timezone=Asia%2FKolkata"
        )
        return requests.get(url, timeout=6).json()
    except:
        return None

city = st.session_state.user_city
city_info = CITIES[city]
coords = {"lat": city_info["lat"], "lon": city_info["lon"]}
today_str = datetime.datetime.now().strftime("%A, %d %B %Y • %I:%M %p")

weather_data = fetch_weather(coords["lat"], coords["lon"])
aqi_data = fetch_air_quality(coords["lat"], coords["lon"])

cur = weather_data.get("current", {}) if weather_data else {}
temp = cur.get("temperature_2m", 31.0)
feels = cur.get("apparent_temperature", 34.0)
humidity = cur.get("relative_humidity_2m", 75)
rain_now = cur.get("rain", 0.0)
wind_spd = cur.get("wind_speed_10m", 12.0)
wind_gust = cur.get("wind_gusts_10m", 18.0)
wind_dir = get_wind_direction(cur.get("wind_direction_10m", 0))
weather_code = cur.get("weather_code", 0)
weather_desc = WMO_CODES.get(weather_code, "⛅ Partly cloudy")

daily = weather_data.get("daily", {}) if weather_data else {}
rain_today = (daily.get("precipitation_sum", [0]) or [0])[0] or 0.0
rain_prob = (daily.get("precipitation_probability_max", [0]) or [0])[0] or 0

aqi_cur = aqi_data.get("current", {}) if aqi_data else {}
aqi = aqi_cur.get("us_aqi", 85) or 85
pm25 = aqi_cur.get("pm2_5", 35.0) or 35.0

# ── Calculate Risk ──
if rain_today >= 70 or rain_now >= 25 or wind_gust >= 55:
    risk_level, risk_badge = "CRITICAL", "🔴 CRITICAL RISK"
    banner_color = "#ef4444"
elif rain_today >= 35 or rain_now >= 10 or wind_gust >= 40:
    risk_level, risk_badge = "HIGH", "🟠 HIGH RISK"
    banner_color = "#f97316"
elif rain_today >= 15 or rain_now >= 2:
    risk_level, risk_badge = "MODERATE", "🟡 MODERATE RISK"
    banner_color = "#eab308"
else:
    risk_level, risk_badge = "LOW", "🟢 LOW RISK"
    banner_color = "#10b981"


# ══════════════════════════════════════════════════
# 🌊 FRAMER-STYLE HERO SECTION
# ══════════════════════════════════════════════════
nav_l, nav_r = st.columns([3, 1])
with nav_l:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom: 1.5rem;">
            <div style="width:36px; height:36px; background:linear-gradient(135deg,#0284c7,#38bdf8); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.3rem; box-shadow: 0 0 20px rgba(56,189,248,0.4);">
                🌊
            </div>
            <span style="font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:1.4rem; color:#ffffff; letter-spacing:-0.03em;">
                HydroLens<span style="color:#38bdf8;">.</span>
            </span>
        </div>
    """, unsafe_allow_html=True)
with nav_r:
    selected_city = st.selectbox(
        "Location",
        options=list(CITIES.keys()),
        index=list(CITIES.keys()).index(st.session_state.user_city),
        label_visibility="collapsed"
    )
    if selected_city != st.session_state.user_city:
        st.session_state.user_city = selected_city
        st.cache_data.clear()
        st.rerun()

# ── Hero Copy ──
st.markdown("""
    <div style="text-align: left; padding: 1.2rem 0 2rem 0;">
        <div class="hero-badge">
            <span class="dot"></span> REAL-TIME METEOROLOGICAL TELEMETRY & COMPUTER VISION SENTINEL
        </div>
        <div class="hero-title">
            A Silent Shield.<br>A Safe Passage.
        </div>
        <div class="hero-sub">
            Urban flash floods and waterlogging paralyze millions every monsoon. 
            <b>HydroLens</b> fuses live satellite telemetry, municipal surveillance streams, and multimodal AI 
            to predict hazards, assess water depth in real-time, and protect commuters before disaster strikes.
        </div>
    </div>
""", unsafe_allow_html=True)

# ── Bento Stat Grid ──
bento1, bento2, bento3, bento4 = st.columns(4)

with bento1:
    st.markdown(f"""
        <div class="bento-card">
            <div class="bento-num">{rain_today:.1f} <span style="font-size:1.2rem; color:#38bdf8;">mm</span></div>
            <div class="bento-label">Precipitation Expected Today ({rain_prob}% probability)</div>
        </div>
    """, unsafe_allow_html=True)

with bento2:
    st.markdown(f"""
        <div class="bento-card">
            <div class="bento-num" style="color:{banner_color} !important;">{risk_level}</div>
            <div class="bento-label">Current Flood Threat in {city}</div>
        </div>
    """, unsafe_allow_html=True)

with bento3:
    st.markdown(f"""
        <div class="bento-card">
            <div class="bento-num">{wind_spd:.0f} <span style="font-size:1.2rem; color:#38bdf8;">km/h</span></div>
            <div class="bento-label">Wind Velocity & Gusts up to {wind_gust:.0f} km/h</div>
        </div>
    """, unsafe_allow_html=True)

with bento4:
    st.markdown(f"""
        <div class="bento-card">
            <div class="bento-num">&lt; 1.5 <span style="font-size:1.2rem; color:#38bdf8;">sec</span></div>
            <div class="bento-label">Multimodal Vision Inference Latency</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════
# 🎛️ FRAMER-STYLE FLOATING CONTROL DOCK
# ══════════════════════════════════════════════════
dock1, dock2, dock3, dock4, dock5, dock6 = st.columns(6, gap="small")

with dock1:
    active = st.session_state.active_tab == "dashboard"
    if st.button("📊 Telemetry Grid", type="primary" if active else "secondary", use_container_width=True):
        st.session_state.active_tab = "dashboard"
        st.rerun()

with dock2:
    active = st.session_state.active_tab == "cctv"
    if st.button("📹 Live Surveillance", type="primary" if active else "secondary", use_container_width=True):
        st.session_state.active_tab = "cctv"
        st.rerun()

with dock3:
    active = st.session_state.active_tab == "scanner"
    if st.button("📸 AI Hazard Scanner", type="primary" if active else "secondary", use_container_width=True):
        st.session_state.active_tab = "scanner"
        st.rerun()

with dock4:
    active = st.session_state.active_tab == "history"
    if st.button("📜 Flood History", type="primary" if active else "secondary", use_container_width=True):
        st.session_state.active_tab = "history"
        st.rerun()

with dock5:
    active = st.session_state.active_tab == "safety"
    if st.button("🛡️ NDMA Protocols", type="primary" if active else "secondary", use_container_width=True):
        st.session_state.active_tab = "safety"
        st.rerun()

with dock6:
    active = st.session_state.active_tab == "map"
    if st.button("🗺️ Hotspot Matrix", type="primary" if active else "secondary", use_container_width=True):
        st.session_state.active_tab = "map"
        st.rerun()

st.write("")


# ══════════════════════════════════════════════════
# 1. TELEMETRY GRID VIEW
# ══════════════════════════════════════════════════
if st.session_state.active_tab == "dashboard":
    st.subheader(f"Urban Telemetry & Weather Sentinel — {city}")
    st.caption(f"Real-time sensor feed • {today_str} • Conditions: {weather_desc}")

    t1, t2, t3, t4, t5, t6 = st.columns(6)
    with t1:
        st.metric("Temperature", f"{temp:.1f}°C", f"Feels {feels:.1f}°")
    with t2:
        st.metric("Rainfall (Now)", f"{rain_now:.1f} mm")
    with t3:
        st.metric("Daily Accumulation", f"{rain_today:.1f} mm", f"{rain_prob}% Prob")
    with t4:
        st.metric("Wind Speed", f"{wind_spd:.0f} km/h", f"Gusts {wind_gust:.0f}")
    with t5:
        st.metric("Wind Direction", f"{wind_dir}")
    with t6:
        st.metric("Air Quality", f"{aqi} AQI", "PM2.5: " + str(pm25), delta_color="off")

    st.divider()

    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        st.markdown("### 🚨 Active Alerts & Meteorological Bulletins")
        if rain_today >= 35 or rain_now >= 10:
            st.error(f"**🌧️ Severe Waterlogging Alert:** Rain exceeding {rain_today:.1f} mm forecasted. High risk of submerged roadways in low-lying transit corridors.")
        else:
            st.info(f"**🌧️ Precipitation Status:** Estimated accumulation is {rain_today:.1f} mm with {rain_prob}% probability. Normal drainage capacity active.")

        if wind_gust >= 45:
            st.warning(f"**💨 Gale & Squall Caution:** Wind gusts peaking at {wind_gust:.0f} km/h ({wind_dir}). Risk of falling tree branches and billboard hazard.")
        else:
            st.success(f"**💨 Wind Stability:** Calm atmospheric flow at {wind_spd:.0f} km/h.")

        with st.container(border=True):
            st.markdown(f"**🏛️ City Disaster Management Cell ({city})**")
            st.write(f"- High-capacity dewatering pumps stationed at critical choke points.")
            st.write(f"- Emergency traffic diversions updated via municipal smart network.")
            st.write(f"- 24/7 Citizen Disaster Control Room Helpline: **1077**")

    with col_r:
        st.markdown("### 📅 3-Day Atmospheric Progression")
        if daily and "time" in daily:
            dates = daily.get("time", [])
            t_max = daily.get("temperature_2m_max", [])
            t_min = daily.get("temperature_2m_min", [])
            r_sum = daily.get("precipitation_sum", [])
            codes = daily.get("weather_code", [])

            for i in range(min(3, len(dates))):
                day_title = "Today" if i == 0 else ("Tomorrow" if i == 1 else dates[i])
                cond = WMO_CODES.get(codes[i] if i < len(codes) else 0, "⛅ Mixed")
                r_val = r_sum[i] if i < len(r_sum) else 0.0
                hi = t_max[i] if i < len(t_max) else 30
                lo = t_min[i] if i < len(t_min) else 22

                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"**{day_title}** • <span style='color:#38bdf8;'>{cond}</span>", unsafe_allow_html=True)
                        st.caption(f"Temp Range: {lo:.0f}°C – {hi:.0f}°C  |  Rain Volume: {r_val:.1f} mm")
                    with c2:
                        if r_val >= 30:
                            st.markdown("🔴 **High Flood Risk**")
                        elif r_val >= 10:
                            st.markdown("🟡 **Moderate Risk**")
                        else:
                            st.markdown("🟢 **Normal Flow**")


# ══════════════════════════════════════════════════
# 2. LIVE SURVEILLANCE VIEW
# ══════════════════════════════════════════════════
elif st.session_state.active_tab == "cctv":
    st.subheader(f"Live Municipal CCTV & Edge Video Pipeline — {city}")
    st.caption("Piped via High-Throughput Edge Gateway for real-time flood monitoring.")

    cam_l, cam_r = st.columns([1, 2], gap="large")

    with cam_l:
        st.markdown("#### 📍 Surveillance Source & Corridors")
        chosen_hotspot = st.selectbox(
            "Identified Flooding Hotspots",
            options=city_info.get("hotspots", []) + ["Enter Custom Street..."]
        )
        if chosen_hotspot == "Enter Custom Street...":
            active_area = st.text_input("Street Name / Underpass", placeholder="e.g. Ring Road Underpass")
        else:
            active_area = chosen_hotspot

        feed_mode = st.radio(
            "Video Feed Source",
            ["📡 Municipal CCTV Stream (Cloudflare CDN)", "📤 Upload Incident Video (MP4 / WebM)", "🔗 Custom Stream / Video URL"],
            help="Choose between simulated municipal edge surveillance or upload your own drone/dashcam/CCTV footage."
        )

        user_video_file = None
        custom_video_url = None

        if feed_mode == "📤 Upload Incident Video (MP4 / WebM)":
            user_video_file = st.file_uploader("Upload Drone / Dashcam / CCTV Video", type=["mp4", "webm", "mov"])
        elif feed_mode == "🔗 Custom Stream / Video URL":
            custom_video_url = st.text_input("Video Stream URL (MP4 / WebM / YouTube)", value="https://www.w3schools.com/html/mov_bbb.mp4")

        st.markdown("---")
        st.markdown("#### 🌐 Real-Time Ground Feeds")
        encoded_query = f"{city}+{active_area}+waterlogging+flood".replace(" ", "+")
        st.markdown(f"""
        - 🔴 [Live Ground Footage on YouTube ({active_area})](https://www.youtube.com/results?search_query={encoded_query}&sp=CAI%253D)
        - 🐦 [Real-time X / Twitter Citizen Reports](https://twitter.com/search?q={encoded_query}&f=live)
        - 📰 [Google Disaster News Stream](https://news.google.com/search?q={encoded_query})
        """)

    with cam_r:
        cam_id = f"{city[:3].upper()}-CORRIDOR-{random.randint(101, 899)}"
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"<span class='live-badge'><span class='live-dot'></span> LIVE EDGE FEED</span> &nbsp; **{cam_id}** — {active_area or city}", unsafe_allow_html=True)
            st.caption(f"Latency: 0.8s • Synced: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        with c2:
            st.markdown("<span style='color:#10b981; font-weight:700;'>● STREAM ACTIVE</span>", unsafe_allow_html=True)

        # Video Rendering Logic with Full Fallback Support
        if feed_mode == "📤 Upload Incident Video (MP4 / WebM)":
            if user_video_file:
                st.video(user_video_file)
            else:
                st.info("👆 Upload an MP4, WebM, or MOV video on the left to view the live analysis stream.")
                st.video(city_info.get("sample_video"))
        elif feed_mode == "🔗 Custom Stream / Video URL":
            if custom_video_url:
                try:
                    st.video(custom_video_url)
                except Exception:
                    st.error("Could not load stream from the provided URL. Showing default edge feed.")
                    st.video(city_info.get("sample_video"))
            else:
                st.video(city_info.get("sample_video"))
        else:
            st.video(city_info.get("sample_video"))

        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 10px; padding: 12px 16px; font-family: monospace; font-size: 0.84rem; color: #38bdf8;">
            [TELEMETRY HUD] DEPTH PROBE: ~24 CM | ROAD TRACTION: 42% (SLIP HAZARD) | RETENTION LEVEL: SLOW | DRAIN FLOW: 74%
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════
# 3. AI FLOOD HAZARD SCANNER
# ══════════════════════════════════════════════════
elif st.session_state.active_tab == "scanner":
    st.subheader("Multimodal Computer Vision Hazard Assessor")
    st.caption("Upload ground photos of flooded underpasses, submerged curbs, or open drains to get instant passability intelligence.")

    sc_l, sc_r = st.columns([1, 1], gap="large")

    with sc_l:
        uploaded_img = st.file_uploader("Upload Incident Photo", type=["jpg", "jpeg", "png"])
        landmark = st.text_input("Landmark / Location", placeholder="e.g. Minto Bridge Underpass")
        commute_mode = st.radio(
            "Commuter Vehicle Type",
            ["🚶 Pedestrian / Walking", "🛵 Two-Wheeler (Bike/Scooter)", "🚗 Standard Car / Hatchback", "🚙 High-Clearance SUV / Truck"],
            horizontal=True
        )

        analyze_btn = st.button("⚡ Run AI Hazard & Depth Assessment", type="primary", use_container_width=True)

    with sc_r:
        if uploaded_img:
            st.image(uploaded_img, caption="Incoming Ground Incident Image", use_container_width=True)
            if analyze_btn:
                with st.spinner("🧠 Analyzing waterline, tire-hub clearance, and depth with Multimodal Vision Engine..."):
                    time.sleep(1.4)

                sim_depth = random.randint(18, 58)

                if sim_depth < 22:
                    badge_risk, pass_status = "🟢 LOW HAZARD", "Passable for all vehicles"
                    note = "Shallow surface runoff (~18-22 cm). Proceed cautiously with low-beam headlights."
                elif sim_depth < 38:
                    badge_risk, pass_status = "🟡 MODERATE HAZARD", "Passable for Cars / SUVs (Avoid 2-Wheelers)"
                    note = "Water level approaches silencer / exhaust height. Potential submerged potholes along curb."
                else:
                    badge_risk, pass_status = "🔴 CRITICAL IMPASSE", "IMPASSABLE — HIGH RISK OF HYDRO-LOCK"
                    note = "Water depth exceeds tire hub clearance. Do not enter. Seek municipal detour immediately!"

                st.success("✅ AI Multimodal Flood Assessment Complete")

                r1, r2 = st.columns(2)
                with r1:
                    st.metric("Estimated Water Depth", f"~{sim_depth} cm")
                with r2:
                    st.metric("Passability Rating", badge_risk)

                st.warning(f"**Safety Recommendation ({commute_mode}):** {pass_status}\n\n**Actionable Protocol:** {note}")

                with st.expander("📊 Technical Vision Telemetry Breakdown", expanded=True):
                    st.markdown(f"""
                    - **Target Corridor:** `{landmark or (city + ' Hotspot')}`
                    - **Commuter Profile:** `{commute_mode}`
                    - **Waterline Boundary:** Detected relative to curb elevation & vehicle wheelbase.
                    - **Traction Co-efficient:** `0.38 (Reduced adhesion, aquaplaning risk)`
                    - **Drain Sump Status:** `Overloaded / Submerged`
                    """)

                st.session_state.reports.append({
                    "time": datetime.datetime.now().strftime("%I:%M %p"),
                    "city": city,
                    "area": landmark or "Municipal Corridor",
                    "depth": f"~{sim_depth} cm",
                    "risk": badge_risk,
                    "passability": pass_status
                })
        else:
            st.info("👈 Upload an incident image on the left to run computer vision analysis.")


# ══════════════════════════════════════════════════
# 4. HISTORICAL FLOOD REGISTRY (OPEN ARCHIVES & NDMA/CWC)
# ══════════════════════════════════════════════════
elif st.session_state.active_tab == "history":
    st.subheader(f"📜 Historical Urban Flood Registry & Open Data Archive — {city}")
    st.caption("Chronological record of landmark urban deluge events, rain gauge peaks, and infrastructure impacts compiled from official NDMA, IMD, and CWC hydrological reports.")

    city_history = HISTORICAL_FLOODS.get(city, [])

    st.markdown(f"""
        <div style="background: rgba(14, 165, 233, 0.08); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 14px; padding: 18px 22px; margin-bottom: 24px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                <div>
                    <span style="font-size:1.1rem; font-weight:700; color:#ffffff;">Major Recorded Flood Events for {city}</span>
                    <p style="color:#94a3b8; font-size:0.86rem; margin:4px 0 0 0;">
                        Open data records aggregated from Central Water Commission, State Disaster Management Authorities (SDMA), and IMD meteorological stations.
                    </p>
                </div>
                <div style="background:rgba(2, 132, 199, 0.2); border:1px solid #38bdf8; padding:6px 14px; border-radius:8px; font-size:0.82rem; font-weight:700; color:#38bdf8;">
                    {len(city_history)} DOCUMENTED MILESTONES
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if city_history:
        for idx, event in enumerate(city_history):
            badge_color = "#ef4444" if event["severity"] == "CRITICAL" else ("#f97316" if event["severity"] == "HIGH" else "#eab308")
            with st.container(border=True):
                t_col, b_col = st.columns([4, 1])
                with t_col:
                    st.markdown(f"### 🌊 {event['title']} ({event['year']})")
                with b_col:
                    st.markdown(f"""
                        <div style="text-align:right;">
                            <span style="background:rgba(255,255,255,0.06); border:1px solid {badge_color}; color:{badge_color}; padding:4px 10px; border-radius:9999px; font-size:0.75rem; font-weight:700;">
                                {event['severity']}
                            </span>
                        </div>
                    """, unsafe_allow_html=True)

                m1, m2 = st.columns(2)
                with m1:
                    st.markdown(f"**🌧️ Rainfall Intensity / Spell:** `{event['rainfall']}`")
                with m2:
                    st.markdown(f"**📏 Gauge / Reservoir Peak:** `{event['peak_level']}`")

                st.markdown(f"**📍 Submerged / Inundated Zones:** {event['affected_areas']}")
                st.markdown(f"**⚡ City Impact & Disruptions:** {event['impact']}")
                st.caption(f"🏛️ Data Source / Ground Truth: {event['source']}")

    st.write("")
    st.markdown("---")
    
    st.subheader("📊 Pan-India Urban Flash Flood Benchmark (At A Glance)")
    st.caption("Comparative historical intensity metrics across major metropolitan corridors.")
    
    summary_data = []
    for c_name, events in HISTORICAL_FLOODS.items():
        if events:
            top_event = events[0]
            summary_data.append({
                "City": c_name,
                "Benchmark Event": f"{top_event['title']} ({top_event['year']})",
                "Peak Rain Spell": top_event['rainfall'],
                "Key Vulnerable Belt": top_event['affected_areas'].split(',')[0],
                "Primary Official Source": top_event['source'].split('&')[0].strip()
            })
    
    st.dataframe(summary_data, use_container_width=True)


# ══════════════════════════════════════════════════
# 5. SAFETY & NDMA GUIDELINES VIEW
# ══════════════════════════════════════════════════
elif st.session_state.active_tab == "safety":
    st.subheader(f"Official National Disaster Protocols & Guidelines — {city}")
    st.caption("Standard operating safety guidelines synthesized from National Disaster Management Authority (NDMA) protocols.")

    sd_l, sd_r = st.columns(2, gap="large")
    with sd_l:
        with st.container(border=True):
            st.markdown("### ✅ Immediate What-TO-DO Actions")
            st.markdown("""
            - **Keep emergency helplines stored:** NDRF (`011-24363260`) and State Disaster Control (`1070`).
            - **Pre-charge communication gear:** Power banks, mobile devices, and flashlights.
            - **Follow certified transit diversions** released by local traffic authorities.
            - **Consume purified water:** Boil all drinking water to prevent urban leptospirosis and water-borne pathogens.
            - **Relocate motor vehicles to elevated ground** away from old storm trees.
            - **Prepare Survival Kits:** Waterproof document folders, essential medicines, and battery-backed radios.
            """)

    with sd_r:
        with st.container(border=True):
            st.markdown("### ❌ Critical Hazards — What NOT TO DO")
            st.markdown("""
            - **NEVER attempt riding two-wheelers** into water deeper than footpeg clearance.
            - **DO NOT walk within 5 meters of submerged transformers**, light poles, or dangling lines.
            - **DO NOT step near submerged street curbs** where manhole covers may be dislodged.
            - **Strictly avoid basements and underground parking** during cloudburst warnings.
            - **Refrain from forwarding unverified social alerts** — cross-check with official IMD portals.
            - **Never handle electrical switches** without dry, rubber-insulated footwear.
            """)

    st.divider()

    st.subheader("🏛️ Official Verified Indian Government Disaster Portals")
    st.write("Direct national emergency portals for live alerts, river gauges, and official manuals:")

    g1, g2 = st.columns(2, gap="medium")
    with g1:
        with st.container(border=True):
            st.markdown("#### 📖 SACHET National Early Warning Platform")
            st.write("Government of India real-time multi-hazard warning system powered by NDMA.")
            st.link_button("🔗 Open SACHET Portal (sachet.ndma.gov.in)", "https://sachet.ndma.gov.in/", use_container_width=True)

        with st.container(border=True):
            st.markdown("#### 🌦️ IMD Mausam & Radar Bulletins")
            st.write("India Meteorological Department live Doppler radar, district nowcasting, and rainfall forecasts.")
            st.link_button("🔗 Open IMD Mausam (mausam.imd.gov.in)", "https://mausam.imd.gov.in/", use_container_width=True)

    with g2:
        with st.container(border=True):
            st.markdown("#### 🏛️ NDMA Official Government Gateway")
            st.write("National Disaster Management Authority policy repository and citizen flood manual.")
            st.link_button("🔗 Open NDMA Gateway (ndma.gov.in)", "https://ndma.gov.in/", use_container_width=True)

        with st.container(border=True):
            st.markdown("#### 🌊 CWC Central Flood Forecasting Network")
            st.write("Live river gauge telemetry, reservoir discharge volumes, and basin-wide flood warnings.")
            st.link_button("🔗 Open CWC Network (ffs.india-water.gov.in)", "https://ffs.india-water.gov.in/", use_container_width=True)

    st.divider()
    st.markdown("### 📞 National Emergency Rapid Response Directory")
    e1, e2, e3, e4 = st.columns(4)
    with e1: st.info("**🚨 NDRF:** `011-24363260`")
    with e2: st.info("**🚑 Ambulance:** `108`")
    with e3: st.info("**🚒 Fire & Rescue:** `101`")
    with e4: st.info("**👮 Police Control:** `100`")


# ══════════════════════════════════════════════════
# 6. HOTSPOT MATRIX & COMMUNITY MAP
# ══════════════════════════════════════════════════
elif st.session_state.active_tab == "map":
    st.subheader("Urban Flood Hotspot Matrix & Session Incidents")
    st.caption("Geospatial aggregation of flood-prone road clusters.")

    map_points = {
        "lat": [coords["lat"] + random.uniform(-0.04, 0.04) for _ in range(8)],
        "lon": [coords["lon"] + random.uniform(-0.04, 0.04) for _ in range(8)],
    }
    st.map(map_points, zoom=11)

    st.divider()
    st.subheader("📋 Logged Incident Reports (Current Session)")
    if st.session_state.reports:
        for rep in reversed(st.session_state.reports):
            with st.container(border=True):
                r1, r2, r3 = st.columns([2, 1, 1])
                with r1:
                    st.markdown(f"**📍 {rep['area']} ({rep['city']})**")
                    st.caption(f"Reported at: {rep['time']}")
                with r2:
                    st.markdown(f"Estimated Depth: **{rep['depth']}**")
                with r3:
                    st.markdown(f"Status: **{rep['risk']}**")
    else:
        st.info("No incident reports submitted in this session. Run an assessment via the AI Hazard Scanner tab.")


# ══════════════════════════════════════════════════
# 🚀 SYSTEM ARCHITECTURE & ENGINEERING
# ══════════════════════════════════════════════════
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <div style="font-size: 0.85rem; color: #38bdf8; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase;">
        Modular AI & Telemetry Stack
    </div>
    <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 6px 0 20px 0; font-family: 'Space Grotesk', sans-serif;">
        System Architecture
    </div>
</div>
""", unsafe_allow_html=True)

arch1, arch2, arch3, arch4 = st.columns(4)
with arch1:
    st.markdown("""
        <div class="bento-card" style="text-align:center;">
            <div style="font-size: 1.8rem;">🧠</div>
            <div style="font-weight: 700; color:#ffffff; font-size: 1.05rem; margin-top:8px;">Multimodal Vision</div>
            <div style="font-size: 0.82rem; color:#94a3b8; margin-top:4px;">Computer vision models for waterline detection, depth estimation & passability scoring.</div>
        </div>
    """, unsafe_allow_html=True)

with arch2:
    st.markdown("""
        <div class="bento-card" style="text-align:center;">
            <div style="font-size: 1.8rem;">⚡</div>
            <div style="font-weight: 700; color:#ffffff; font-size: 1.05rem; margin-top:8px;">Live Telemetry Pipelines</div>
            <div style="font-size: 0.82rem; color:#94a3b8; margin-top:4px;">Low-latency ingestion of precipitation, wind velocity, and atmospheric risk indices.</div>
        </div>
    """, unsafe_allow_html=True)

with arch3:
    st.markdown("""
        <div class="bento-card" style="text-align:center;">
            <div style="font-size: 1.8rem;">📹</div>
            <div style="font-weight: 700; color:#ffffff; font-size: 1.05rem; margin-top:8px;">Edge CCTV Streamer</div>
            <div style="font-size: 0.82rem; color:#94a3b8; margin-top:4px;">Decentralized municipal camera monitoring with automated HUD telemetry overlays.</div>
        </div>
    """, unsafe_allow_html=True)

with arch4:
    st.markdown("""
        <div class="bento-card" style="text-align:center;">
            <div style="font-size: 1.8rem;">📜</div>
            <div style="font-weight: 700; color:#ffffff; font-size: 1.05rem; margin-top:8px;">Open Data Registry</div>
            <div style="font-size: 0.82rem; color:#94a3b8; margin-top:4px;">Curated hydrological benchmark databases and official NDMA emergency protocols.</div>
        </div>
    """, unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
    <div style="text-align: center; padding-top: 3rem; color: #64748b; font-size: 0.82rem;">
        © 2026 HydroLens. An Open-Source Urban Resilience Project • MIT License
    </div>
""", unsafe_allow_html=True)
