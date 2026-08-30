import streamlit as st
import json
import random
import urllib.error
import urllib.request
import pandas as pd

# ============================================================
# CLOUD CONFIGURATION & SECURITY
# ============================================================
JSONBIN_BIN_ID = "6a939368da38895dfe21c244"
JSONBIN_MASTER_KEY = "$2a$10$N6A/7tTzu0bIYUNeer5RveMMym14VTQdspb2Rd64c80KH3WZVKIXa"
ACCESS_PASSWORD = "wikiwiki123"

# ============================================================
# MOTIVATIONAL PHRASES
# ============================================================
MOTIVATIONAL_PHRASES = [
    "Keep going. Every call is another opportunity to improve.",
    "Progress is built one call at a time.",
    "Stay focused. Your next result can improve your performance.",
    "Consistency creates strong results.",
    "Wikiiii-wikiiiiiiiiiiiiii.",
    "Magpag-pag, kung maraming DROP!",
    "Small improvements lead to better performance.",
    "Keep pushing. Your numbers can change with every call.",
    "Focus on the next call and give your best.",
    "Strong performance starts with discipline.",
    "Every release brings you closer to your target.",
    "Stay calm, stay focused, and keep improving.",
    "Your effort today builds your performance tomorrow.",
    "Do not stop. Keep working toward your target.",
    "One good call can start a better streak.",
    "Keep your momentum going.",
    "Believe in your progress and continue improving.",
]

# ============================================================
# CLOUD SYNC CLASS
# ============================================================
class CloudSync:
    @staticmethod
    def load_data():
        if not JSONBIN_BIN_ID or not JSONBIN_MASTER_KEY:
            return None
        try:
            url = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}/latest"
            req = urllib.request.Request(
                url,
                headers={"X-Master-Key": JSONBIN_MASTER_KEY, "X-Access-Key": ""},
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                res = json.loads(response.read().decode())
                return res.get("record", {})
        except Exception as e:
            return None

    @staticmethod
    def save_data(data):
        if not JSONBIN_BIN_ID or not JSONBIN_MASTER_KEY:
            return False
        try:
            url = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}"
            req_data = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=req_data,
                method="PUT",
                headers={
                    "Content-Type": "application/json",
                    "X-Master-Key": JSONBIN_MASTER_KEY,
                },
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                return True
        except Exception as e:
            return False

# ============================================================
# METRICS CALCULATION
# ============================================================
def calculate_metrics(release, unrelease):
    total = release + unrelease
    percentage = 0 if total == 0 else (release / total) * 100
    deficit = max(0, (unrelease * 6) - release)
    
    if release == 0 and unrelease == 0:
        status = "NO DATA"
    elif percentage >= 85:
        status = "PASSING"
    else:
        status = "BELOW TARGET"
        
    return percentage, deficit, status

# ============================================================
# CUSTOM CSS (THEME & BUBBLES)
# ============================================================
def inject_custom_css():
    st.markdown("""
    <style>
    /* Dark Glassmorphism Theme */
    .stApp {
        background-color: #08080D;
        color: #FFFFFF;
    }
    
    /* Bubble Animation */
    .bubbles-container {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        z-index: 0; overflow: hidden; pointer-events: none;
    }
    .bubble {
        position: absolute;
        bottom: -50px;
        background-color: rgba(139, 92, 246, 0.15);
        border-radius: 50%;
        animation: floatUp linear infinite;
    }
    @keyframes floatUp {
        0% { transform: translateY(0) scale(1); opacity: 1; }
        80% { opacity: 0.8; }
        100% { transform: translateY(-100vh) scale(1.5); opacity: 0; }
    }
    
    /* Content over bubbles */
    .main-content {
        position: relative;
        z-index: 1;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #151520;
        border: 1px solid #303044;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-title { font-size: 12px; font-weight: bold; color: #A1A1AA; }
    .metric-value { font-size: 28px; font-weight: bold; color: #FFFFFF; }
    </style>
    
    <div class="bubbles-container">
        <div class="bubble" style="width:20px; height:20px; left:10%; animation-duration:8s;"></div>
        <div class="bubble" style="width:30px; height:30px; left:30%; animation-duration:12s; animation-delay:2s;"></div>
        <div class="bubble" style="width:15px; height:15px; left:50%; animation-duration:6s; animation-delay:1s;"></div>
        <div class="bubble" style="width:25px; height:25px; left:70%; animation-duration:10s; animation-delay:4s;"></div>
        <div class="bubble" style="width:35px; height:35px; left:85%; animation-duration:14s;"></div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN APPLICATION
# ============================================================
st.set_page_config(page_title="CLUSTER ARLEN | TEAM REEYAAA", layout="wide")
inject_custom_css()

# Session State Initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "members" not in st.session_state:
    st.session_state.members = None

# --- LOGIN SCREEN ---
if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center; color: #FFFFFF;'>CLUSTER ARLEN | LOGIN</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A1A1AA;'>Enter Password to Access System</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password_input = st.text_input("Password", type="password", label_visibility="collapsed")
        if st.button("LOGIN", use_container_width=True, type="primary"):
            if password_input == ACCESS_PASSWORD:
                st.session_state.authenticated = True
                # Load cloud data on successful login
                cloud_data = CloudSync.load_data()
                st.session_state.members = cloud_data if cloud_data is not None else {}
                st.rerun()
            else:
                st.error("Incorrect Password. Please try again.")
    st.stop()

# --- HEADER ---
st.markdown("<div class='main-content'>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>CLUSTER ARLEN</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #A78BFA; margin-top: 0;'>TEAM REEYAAA WIKI-WIKIIIIII</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #71717A; font-size: 12px;'>Programmed by: @CLA TECHFORGE | Clarence Gabriel Obida | @serclasocials</p>", unsafe_allow_html=True)

# --- CONTROLS ---
col_head1, col_head2, col_head3 = st.columns([2, 1, 1])
with col_head1:
    st.markdown("**TEAM PERFORMANCE SYSTEM**")
with col_head2:
    new_member = st.text_input("Name", placeholder="Member Name", label_visibility="collapsed", key="add_input")
    if st.button("+ COUNT ME IN", use_container_width=True):
        if new_member and new_member not in st.session_state.members:
            st.session_state.members[new_member] = {"release": 0, "unrelease": 0, "transfer": 0}
            CloudSync.save_data(st.session_state.members)
            st.rerun()
with col_head3:
    if st.button("RESET ALL", use_container_width=True):
        st.session_state.members = {}
        CloudSync.save_data({})
        st.rerun()

st.markdown("---")

# --- TABS CREATION ---
tab_titles = ["LEADER DASHBOARD"] + list(st.session_state.members.keys())
tabs = st.tabs(tab_titles)

# --- TAB 0: LEADER DASHBOARD ---
with tabs[0]:
    st.subheader("LIVE TEAM METRICS OVERVIEW & RANKINGS")
    
    total_rel = sum(m["release"] for m in st.session_state.members.values())
    total_unrel = sum(m["unrelease"] for m in st.session_state.members.values())
    
    # Calculate group stats
    total_calls = total_rel + total_unrel
    group_perc = (total_rel / total_calls * 100) if total_calls > 0 else 0
    total_def = sum(max(0, (m["unrelease"] * 6) - m["release"]) for m in st.session_state.members.values())
    
    # Summary Cards
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    sc1.metric("MEMBERS", len(st.session_state.members))
    sc2.metric("RELEASE", total_rel)
    sc3.metric("UNRELEASE", total_unrel)
    sc4.metric("DEFICIT", total_def)
    sc5.metric("GROUP %", f"{group_perc:.2f}%")
    
    st.info(f"💡 {random.choice(MOTIVATIONAL_PHRASES)}")
    
    # Data Table
    table_data = []
    for name, data in st.session_state.members.items():
        perc, deficit, status = calculate_metrics(data["release"], data["unrelease"])
        table_data.append({
            "TEAM MEMBER": name,
            "RELEASE": data["release"],
            "UNRELEASE": data["unrelease"],
            "TRANSFER": data["transfer"],
            "DEFICIT": deficit,
            "PERCENTAGE": perc,
            "STATUS": status
        })
        
    if table_data:
        df = pd.DataFrame(table_data)
        df.sort_values(by="PERCENTAGE", ascending=False, inplace=True)
        df.insert(0, "RANK", range(1, len(df) + 1))
        # Format percentage string for display
        df["PERCENTAGE"] = df["PERCENTAGE"].apply(lambda x: f"{x:.2f}%")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.write("No team members added yet.")

# --- TABS 1+: INDIVIDUAL MEMBERS ---
for idx, member_name in enumerate(st.session_state.members.keys(), start=1):
    with tabs[idx]:
        col_title, col_remove = st.columns([4, 1])
        with col_title:
            st.markdown(f"<h2>{member_name.upper()}</h2>", unsafe_allow_html=True)
        with col_remove:
            if st.button("REMOVE MEMBER", key=f"del_{member_name}", type="primary"):
                del st.session_state.members[member_name]
                CloudSync.save_data(st.session_state.members)
                st.rerun()
        
        m_data = st.session_state.members[member_name]
        perc, deficit, status = calculate_metrics(m_data["release"], m_data["unrelease"])
        
        c1, c2, c3, c4, c5 = st.columns(5)
        
        def update_metric(member, metric, amount):
            st.session_state.members[member][metric] = max(0, st.session_state.members[member][metric] + amount)
            CloudSync.save_data(st.session_state.members)
            st.rerun()

        # Release
        with c1:
            st.markdown(f"<div class='metric-card'><div class='metric-title' style='color:#22C55E;'>RELEASE</div><div class='metric-value'>{m_data['release']}</div></div>", unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            if cc1.button("−", key=f"sub_rel_{member_name}", use_container_width=True): update_metric(member_name, "release", -1)
            if cc2.button("➕", key=f"add_rel_{member_name}", use_container_width=True): update_metric(member_name, "release", 1)
            
        # Unrelease
        with c2:
            st.markdown(f"<div class='metric-card'><div class='metric-title' style='color:#EF4444;'>UNRELEASE</div><div class='metric-value'>{m_data['unrelease']}</div></div>", unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            if cc1.button("−", key=f"sub_unrel_{member_name}", use_container_width=True): update_metric(member_name, "unrelease", -1)
            if cc2.button("➕", key=f"add_unrel_{member_name}", use_container_width=True): update_metric(member_name, "unrelease", 1)

        # Transfer
        with c3:
            st.markdown(f"<div class='metric-card'><div class='metric-title' style='color:#FACC15;'>TRANSFER</div><div class='metric-value'>{m_data['transfer']}</div></div>", unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            if cc1.button("−", key=f"sub_trans_{member_name}", use_container_width=True): update_metric(member_name, "transfer", -1)
            if cc2.button("➕", key=f"add_trans_{member_name}", use_container_width=True): update_metric(member_name, "transfer", 1)
            
        # Deficit (Auto)
        with c4:
            st.markdown(f"<div class='metric-card'><div class='metric-title' style='color:#EF4444;'>DEFICIT</div><div class='metric-value'>{deficit}</div><div style='font-size:10px; color:#71717A;'>AUTO</div></div>", unsafe_allow_html=True)

        # Percentage (Auto)
        with c5:
            st.markdown(f"<div class='metric-card'><div class='metric-title' style='color:#A78BFA;'>PERCENTAGE</div><div class='metric-value'>{perc:.2f}%</div><div style='font-size:10px; color:#71717A;'>AUTO</div></div>", unsafe_allow_html=True)

        # Status & Motivation
        status_color = "#22C55E" if status == "PASSING" else "#EF4444" if status == "BELOW TARGET" else "#71717A"
        st.markdown(f"**CURRENT PERFORMANCE STATUS:** <span style='color:{status_color}; font-size:20px; font-weight:bold;'>{status}</span>", unsafe_allow_html=True)
        st.info(random.choice(MOTIVATIONAL_PHRASES))

st.markdown("</div>", unsafe_allow_html=True)
