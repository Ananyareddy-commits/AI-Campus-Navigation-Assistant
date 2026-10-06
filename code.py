import os
import math
import streamlit as st
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv

# Optional Gemini AI
try:
    from google import genai
except ImportError:
    genai = None


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

APP_NAME = "AI Campus Navigation Assistant"

COLLEGE_NAME = "MALLA REDDY ENGINEERING COLLEGE FOR WOMEN"

COLLEGE_LOCATION = (
    "Maisammaguda, Dhulapally (Kompally), "
    "Hyderabad, Telangana"
)

# Demo coordinates.
# Replace with verified college coordinates if needed.
COLLEGE_LAT = 17.5500
COLLEGE_LON = 78.4800

# Student roll number
# Replace this with the actual roll number.
STUDENT_ROLL_NUMBER = "MRECW-ROLL-001"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# CAMPUS LOCATIONS
# ============================================================

CAMPUS_LOCATIONS = {

    "Main Gate": {
        "lat": COLLEGE_LAT,
        "lon": COLLEGE_LON,
        "category": "Entrance",
        "description": "Main entrance of the campus."
    },

    "Administrative Block": {
        "lat": COLLEGE_LAT + 0.0010,
        "lon": COLLEGE_LON + 0.0005,
        "category": "Administration",
        "description": "Administrative offices and student services."
    },

    "Central Library": {
        "lat": COLLEGE_LAT + 0.0018,
        "lon": COLLEGE_LON + 0.0010,
        "category": "Academic",
        "description": "Library and learning resources."
    },

    "Computer Science Block": {
        "lat": COLLEGE_LAT + 0.0015,
        "lon": COLLEGE_LON - 0.0010,
        "category": "Academic",
        "description": "Computer science classrooms and laboratories."
    },

    "Engineering Block": {
        "lat": COLLEGE_LAT - 0.0008,
        "lon": COLLEGE_LON + 0.0013,
        "category": "Academic",
        "description": "Engineering classrooms and laboratories."
    },

    "Canteen": {
        "lat": COLLEGE_LAT - 0.0014,
        "lon": COLLEGE_LON - 0.0008,
        "category": "Food",
        "description": "Campus food and refreshments."
    },

    "Auditorium": {
        "lat": COLLEGE_LAT + 0.0002,
        "lon": COLLEGE_LON + 0.0020,
        "category": "Events",
        "description": "Events and seminars."
    },

    "Sports Ground": {
        "lat": COLLEGE_LAT - 0.0020,
        "lon": COLLEGE_LON + 0.0008,
        "category": "Sports",
        "description": "Outdoor sports and activities."
    },

    "Medical Room": {
        "lat": COLLEGE_LAT - 0.0005,
        "lon": COLLEGE_LON - 0.0015,
        "category": "Health",
        "description": "Basic first-aid and medical assistance."
    }
}


# ============================================================
# LOGIN
# ============================================================

def login_page():

    st.title("🎓 AI Campus Navigation Assistant")

    if os.path.exists("logo.png"):
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.image("logo.png", width=140)

    st.header(COLLEGE_NAME)

    st.write(COLLEGE_LOCATION)

    st.divider()

    st.subheader("Login")

    role = st.selectbox(
        "Login as",
        ["Student", "Faculty"]
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        # Student
        if (
            role == "Student"
            and username == "student"
            and password == "student123"
        ):

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.session_state.page = "Dashboard"

            st.rerun()

        # Faculty
        elif (
            role == "Faculty"
            and username == "faculty"
            and password == "faculty123"
        ):

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.session_state.page = "Dashboard"

            st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )

    st.divider()

    st.info(
        "Demo Student Login: student / student123"
    )

    st.info(
        "Demo Faculty Login: faculty / faculty123"
    )


# ============================================================
# SIDEBAR
# ============================================================

def sidebar():

    with st.sidebar:

        if os.path.exists("logo.png"):
            st.image("logo.png", width=90)

        st.title("Campus Assistant")

        st.caption(
            COLLEGE_NAME
        )

        st.divider()

        pages = [
            "Dashboard",
            "Campus Map",
            "Navigation",
            "AI Assistant",
            "Emergency",
            "Profile",
            "About College"
        ]

        selected_page = st.radio(
            "Menu",
            pages,
            index=pages.index(
                st.session_state.page
            )
        )

        st.session_state.page = selected_page

        st.divider()

        st.write(
            f"User: {st.session_state.username}"
        )

        st.write(
            f"Role: {st.session_state.role}"
        )

        st.divider()

        if st.button(
            "Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.session_state.messages = []

            st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    st.title("🏠 Campus Dashboard")

    st.subheader(
        f"Welcome, {st.session_state.username}!"
    )

    st.write(
        "Welcome to the AI Campus Navigation Assistant."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Campus Locations",
            len(CAMPUS_LOCATIONS)
        )

    with col2:
        st.metric(
            "Navigation",
            "Available"
        )

    with col3:
        st.metric(
            "AI Assistant",
            "Available"
        )

    with col4:
        st.metric(
            "Emergency",
            "24/7"
        )

    st.divider()

    st.subheader("Available Features")

    col1, col2 = st.columns(2)

    with col1:

        st.write("🗺️ **Campus Map**")
        st.write(
            "View important locations on the campus map."
        )

        st.write("🧭 **Navigation**")
        st.write(
            "Calculate approximate distance between campus locations."
        )

        st.write("🤖 **AI Assistant**")
        st.write(
            "Ask questions about campus facilities."
        )

    with col2:

        st.write("🚨 **Emergency**")
        st.write(
            "View important emergency contact numbers."
        )

        st.write("👤 **Profile**")
        st.write(
            "View your student or faculty information."
        )

        st.write("🎓 **About College**")
        st.write(
            "View basic information about the college."
        )


# ============================================================
# CAMPUS MAP
# ============================================================

def campus_map():

    st.title("🗺️ Campus Map")

    st.write(
        "View important campus locations."
    )

    campus = folium.Map(
        location=[
            COLLEGE_LAT,
            COLLEGE_LON
        ],
        zoom_start=17,
        control_scale=True
    )

    for name, data in CAMPUS_LOCATIONS.items():

        popup = (
            f"{name}<br>"
            f"Category: {data['category']}<br>"
            f"{data['description']}"
        )

        folium.Marker(
            location=[
                data["lat"],
                data["lon"]
            ],
            tooltip=name,
            popup=popup
        ).add_to(campus)

    st_folium(
        campus,
        width=None,
        height=600,
        returned_objects=[]
    )

    st.warning(
        "The map coordinates in this demo are approximate. "
        "Use verified campus coordinates for a real deployment."
    )


# ============================================================
# DISTANCE CALCULATION
# ============================================================

def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2
):

    radius = 6371

    lat_difference = math.radians(
        lat2 - lat1
    )

    lon_difference = math.radians(
        lon2 - lon1
    )

    value = (
        math.sin(lat_difference / 2) ** 2
        +
        math.cos(math.radians(lat1))
        *
        math.cos(math.radians(lat2))
        *
        math.sin(lon_difference / 2) ** 2
    )

    distance = (
        2
        * math.atan2(
            math.sqrt(value),
            math.sqrt(1 - value)
        )
    )

    return radius * distance


# ============================================================
# NAVIGATION
# ============================================================

def navigation():

    st.title("🧭 Campus Navigation")

    st.write(
        "Select a starting location and destination."
    )

    locations = list(
        CAMPUS_LOCATIONS.keys()
    )

    col1, col2 = st.columns(2)

    with col1:

        start = st.selectbox(
            "Starting Location",
            locations
        )

    with col2:

        destination = st.selectbox(
            "Destination",
            locations,
            index=1
        )

    st.divider()

    if st.button(
        "Find Route",
        use_container_width=True
    ):

        if start == destination:

            st.warning(
                "Starting location and destination "
                "must be different."
            )

            return

        start_data = CAMPUS_LOCATIONS[start]

        destination_data = CAMPUS_LOCATIONS[
            destination
        ]

        distance_km = calculate_distance(
            start_data["lat"],
            start_data["lon"],
            destination_data["lat"],
            destination_data["lon"]
        )

        distance_m = distance_km * 1000

        walking_minutes = max(
            1,
            round(distance_m / 80)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.success(
                f"Distance: {distance_m:.0f} metres"
            )

        with col2:

            st.info(
                f"Approximate walking time: "
                f"{walking_minutes} minutes"
            )

        st.divider()

        center_lat = (
            start_data["lat"]
            + destination_data["lat"]
        ) / 2

        center_lon = (
            start_data["lon"]
            + destination_data["lon"]
        ) / 2

        route_map = folium.Map(
            location=[
                center_lat,
                center_lon
            ],
            zoom_start=17
        )

        folium.Marker(
            [
                start_data["lat"],
                start_data["lon"]
            ],
            tooltip=f"Start: {start}"
        ).add_to(route_map)

        folium.Marker(
            [
                destination_data["lat"],
                destination_data["lon"]
            ],
            tooltip=f"Destination: {destination}"
        ).add_to(route_map)

        folium.PolyLine(
            [
                [
                    start_data["lat"],
                    start_data["lon"]
                ],
                [
                    destination_data["lat"],
                    destination_data["lon"]
                ]
            ],
            weight=5
        ).add_to(route_map)

        st_folium(
            route_map,
            width=None,
            height=500,
            returned_objects=[]
        )

        st.caption(
            "This is an approximate straight-line route, "
            "not an actual road or walking route."
        )


# ============================================================
# FALLBACK AI
# ============================================================

def fallback_ai(question):

    question = question.lower()

    if "library" in question:

        return (
            "The Central Library is one of the available "
            "campus locations. Open the Campus Map or "
            "Navigation page to locate it."
        )

    if (
        "canteen" in question
        or "food" in question
    ):

        return (
            "The Canteen is available as a campus location. "
            "Use the Campus Map or Navigation page."
        )

    if (
        "computer" in question
        or "cse" in question
    ):

        return (
            "The Computer Science Block is available "
            "as a campus location."
        )

    if "engineering" in question:

        return (
            "The Engineering Block is available "
            "as a campus location."
        )

    if (
        "medical" in question
        or "first aid" in question
    ):

        return (
            "The Medical Room is available for basic "
            "first-aid and medical assistance."
        )

    if (
        "emergency" in question
        or "ambulance" in question
    ):

        return (
            "For an emergency in India, call 112. "
            "Ambulance emergency service is 108."
        )

    if (
        "map" in question
    ):

        return (
            "Open the Campus Map page from the sidebar "
            "to view campus locations."
        )

    if (
        "route" in question
        or "navigate" in question
        or "navigation" in question
    ):

        return (
            "Open the Navigation page and select your "
            "starting location and destination."
        )

    if (
        "hello" in question
        or "hi" in question
    ):

        return (
            "Hello! I am your AI Campus Assistant. "
            "You can ask me about campus locations, "
            "navigation and facilities."
        )

    return (
        "I can help with campus locations, navigation, "
        "facilities and emergency information."
    )


# ============================================================
# GEMINI AI
# ============================================================

def gemini_answer(question):

    if genai is None:
        return None

    if not GEMINI_API_KEY:
        return None

    try:

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        campus_details = "\n".join(
            [
                f"{name}: {data['description']}"
                for name, data
                in CAMPUS_LOCATIONS.items()
            ]
        )

        prompt = f"""
You are an AI Campus Assistant.

College:
{COLLEGE_NAME}

Location:
{COLLEGE_LOCATION}

Campus information:
{campus_details}

Student question:
{question}

Answer briefly and clearly.

Only use the provided campus information
for college-specific facts.

Do not invent college-specific information.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception:
        return None


# ============================================================
# AI ASSISTANT
# ============================================================

def ai_assistant():

    st.title("🤖 AI Campus Assistant")

    st.write(
        "Ask questions about the campus."
    )

    st.divider()

    # Previous messages
    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    question = st.chat_input(
        "Ask something about the campus..."
    )

    if question:

        # User message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # Gemini
        answer = gemini_answer(
            question
        )

        # Fallback
        if not answer:

            answer = fallback_ai(
                question
            )

        # Assistant message
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()

    if st.session_state.messages:

        if st.button(
            "Clear Chat"
        ):

            st.session_state.messages = []

            st.rerun()


# ============================================================
# EMERGENCY
# ============================================================

def emergency():

    st.title("🚨 Emergency Assistance")

    st.write(
        "Important emergency numbers in India."
    )

    st.warning(
        "For an immediate emergency, contact the "
        "appropriate emergency service."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🚨 General Emergency")

        st.metric(
            "Emergency",
            "112"
        )

        st.write(
            "Integrated emergency response number."
        )

        st.divider()

        st.subheader("🚑 Ambulance")

        st.metric(
            "Ambulance",
            "108"
        )

    with col2:

        st.subheader("👮 Police")

        st.metric(
            "Police",
            "100"
        )

        st.write(
            "Police emergency number."
        )

        st.divider()

        st.subheader("🔥 Fire & Rescue")

        st.metric(
            "Fire",
            "101"
        )

        st.write(
            "Fire and rescue emergency number."
        )


# ============================================================
# PROFILE
# ============================================================

def profile():

    st.title("👤 My Profile")

    st.divider()

    if st.session_state.role == "Student":

        roll_number = STUDENT_ROLL_NUMBER

    else:

        roll_number = "Faculty"

    col1, col2 = st.columns([1, 2])

    with col1:

        if os.path.exists("logo.png"):

            st.image(
                "logo.png",
                width=150
            )

        else:

            st.write("🎓")

    with col2:

        st.subheader(
            "Account Information"
        )

        st.write(
            f"Username: {st.session_state.username}"
        )

        st.write(
            f"Roll Number: {roll_number}"
        )

        st.write(
            f"Role: {st.session_state.role}"
        )

        st.write(
            f"College: {COLLEGE_NAME}"
        )

        st.write(
            f"Location: {COLLEGE_LOCATION}"
        )


# ============================================================
# ABOUT COLLEGE
# ============================================================

def about_college():

    st.title("🎓 About College")

    st.divider()

    col1, col2 = st.columns([1, 3])

    with col1:

        if os.path.exists("logo.png"):

            st.image(
                "logo.png",
                width=160
            )

        else:

            st.write("🎓")

    with col2:

        st.header(
            COLLEGE_NAME
        )

        st.write(
            COLLEGE_LOCATION
        )

    st.divider()

    st.subheader(
        "College Information"
    )

    st.write(
        f"{COLLEGE_NAME} is located at "
        f"{COLLEGE_LOCATION}."
    )

    st.info(
        "Official college details, departments, "
        "facilities and contact information can "
        "be added here later."
    )


# ============================================================
# MAIN APP
# ============================================================

def main():

    # Login first
    if not st.session_state.logged_in:

        login_page()

        return

    # Sidebar
    sidebar()

    # Current page
    page = st.session_state.page

    if page == "Dashboard":

        dashboard()

    elif page == "Campus Map":

        campus_map()

    elif page == "Navigation":

        navigation()

    elif page == "AI Assistant":

        ai_assistant()

    elif page == "Emergency":

        emergency()

    elif page == "Profile":

        profile()

    elif page == "About College":

        about_college()

    st.divider()

    st.caption(
        f"{APP_NAME} | {COLLEGE_NAME}"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()