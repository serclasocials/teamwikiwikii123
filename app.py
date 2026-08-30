import streamlit as st
import json
import urllib.request
import urllib.error
import random
import pandas as pd

# ============================================================
# PAGE CONFIG & STATE INITIALIZATION
# ============================================================
st.set_page_config(
    page_title="CLUSTER ARLEN | TEAM REEYAAA", 
    page_icon="🔥", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

JSONBIN_BIN_ID = "6a94bc25da38895dfe243f0a"
JSONBIN_MASTER_KEY = "$2a$10$1hHtPNPdRRPEIe3x2xb8DO/ARn1rKBfCaBk2aRg.mAdgJsK7aEDlu"
ACCESS_PASSWORD = "wikiwiki"

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
# CLOUD CONFIGURATION & SECURITY
# ============================================================
class CloudSync:
    @staticmethod
    def load_data():
        if not JSONBIN_BIN_ID:
            return {}
        try:
            url = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}/latest"
            # Removed the headers completely for loading since the bin is Public
            req = urllib.request.Request(url)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                res = json.loads(response.read().decode())
                return res.get("record", {})
        except Exception as e:
            st.toast(f"Cloud load error: {e}", icon="⚠️")
            return {}

    @staticmethod
    def save_data(data):
        if not JSONBIN_BIN_ID or not JSONBIN_MASTER_KEY:
            return False
        try:
            url = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}"
            req_data = json.dumps(data).encode("utf-8")
            
            # Saving still requires the Master Key, even for a Public bin
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
            st.toast(f"Cloud save error: {e}", icon="⚠️")
            return False
# ============================================================
# CUSTOM CSS (Mimics Tkinter's Glassy Dark Mode & Bubbles)
# ============================================================
def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Base Backgrounds */
        .stApp {
            background-color: #08080D;
            background-image: radial-gradient(circle at center, #151520 0%, #08080D 100%);
            color: #FFFFFF;
        }
        
        /* Glassy Containers */
        div[data-testid="stMetric"], .glass-container {
            background-color: #151520 !important;
            border: 1px solid #303044;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            text-align: center;
        }

        /* Typography & Metrics adjustments */
        div[data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-size: 2.2rem !important;
            font-weight: bold !important;
        }
        
        /* Specific metric label colors */
        .metric-RELEASE div[data-testid="stMetricLabel"] label { color: #22C55E !important; font-weight: bold; }
        .metric-UNRELEASE div[data-testid="stMetricLabel"] label { color: #EF4444 !important; font-weight: bold; }
        .metric-TRANSFER div[data-testid="stMetricLabel"] label { color: #FACC15 !important; font-weight: bold; }
        .metric-DEFICIT div[data-testid="stMetricLabel"] label { color: #EF4444 !important; font-weight: bold; }
        .metric-PERCENTAGE div[data-testid="stMetricLabel"] label { color: #A78BFA !important; font-weight: bold; }

        /* Headers */
        h1, h2, h3 { color: #FFFFFF !important; }
        .purple-text { color: #A78BFA; }
        
        /* Status Panels */
        .motivation-panel {
            background-color: #1D1D2B;
            border: 1px solid #5B21B6;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            color: #FACC15;
            font-size: 1.2rem;
            font-style: italic;
            margin-bottom: 20px;
        }

        /* Buttons */
        div[data-testid="stButton"] button {
            background-color: #151520;
            border: 1px solid #303044;
            color: #FFFFFF;
        }
        div[data-testid="stButton"] button:hover {
            border-color: #A78BFA;
            color: #A78BFA;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# APP LOGIC
# ============================================================
def authenticate():
    st.markdown("<h1 style='text-align: center;'>CLUSTER ARLEN | LOGIN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A1A1AA;'>Enter Password to Access System</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Password", type="password", label_visibility="collapsed")
        if st.button("LOGIN", use_container_width=True):
            if password == ACCESS_PASSWORD:
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Incorrect Password. Please try again.")

def fetch_latest_data():
    with st.spinner("Syncing with cloud..."):
        st.session_state['members'] = CloudSync.load_data()

def calculate_metrics(data):
    release = data.get("release", 0)
    unrelease = data.get("unrelease", 0)
    total = release + unrelease
    percentage = (release / total * 100) if total > 0 else 0
    deficit = max(0, (unrelease * 6) - release)
    return percentage, deficit

def render_main_app():
    # Header
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>CLUSTER ARLEN</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #A78BFA; margin-top: 0;'>TEAM REEYAAA WIKI-WIKIIIIII</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #71717A; font-size: 0.8rem;'>Programmed by: @CLA TECHFORGE | Clarence Gabriel Obida | @serclasocials</p>", unsafe_allow_html=True)

    # Top Controls
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col1:
        st.markdown("**TEAM PERFORMANCE SYSTEM**")
    with col2:
        if st.button("🔄 Sync Live Data", use_container_width=True):
            fetch_latest_data()
            st.rerun()
    with col3:
        with st.popover("⚠️ RESET ALL"):
            st.warning("Are you sure you want to remove ALL records completely?")
            if st.button("CONFIRM WIPE EVERYONE", type="primary"):
                st.session_state['members'] = {}
                CloudSync.save_data({})
                st.success("All data wiped.")
                st.rerun()
    with col4:
        with st.popover("➕ COUNT ME IN"):
            new_name = st.text_input("Enter team member name:")
            if st.button("Add Member", type="primary"):
                if new_name and new_name not in st.session_state['members']:
                    st.session_state['members'][new_name] = {"release": 0, "unrelease": 0, "transfer": 0}
                    CloudSync.save_data(st.session_state['members'])
                    st.rerun()

    # Generate Tabs
    member_names = list(st.session_state['members'].keys())
    tabs = st.tabs(["LEADER DASHBOARD"] + member_names)

    # ================== LEADER DASHBOARD ==================
    with tabs[0]:
        st.markdown("### LIVE TEAM METRICS OVERVIEW & RANKINGS")
        
        totals = {"release": 0, "unrelease": 0, "transfer": 0, "deficit": 0}
        leaderboard = []

        for name, data in st.session_state['members'].items():
            perc, df = calculate_metrics(data)
            totals["release"] += data["release"]
            totals["unrelease"] += data["unrelease"]
            totals["transfer"] += data["transfer"]
            totals["deficit"] += df
            
            status = "NO DATA" if data["release"] == 0 and data["unrelease"] == 0 else "PASSING" if perc >= 85 else "BELOW TARGET"
            leaderboard.append({
                "Name": name, "Release": data["release"], "Unrelease": data["unrelease"],
                "Transfer": data["transfer"], "Deficit": df, "Percentage": f"{perc:.2f}%", 
                "Sort_Perc": perc, "Status": status
            })

        t_calls = totals["release"] + totals["unrelease"]
        t_perc = (totals["release"] / t_calls * 100) if t_calls > 0 else 0

        # Summary Cards
        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric("MEMBERS", len(member_names))
        mc2.metric("TOTAL RELEASE", totals["release"])
        mc3.metric("TOTAL UNRELEASE", totals["unrelease"])
        mc4.metric("TOTAL DEFICIT", totals["deficit"])
        mc5.metric("GROUP %", f"{t_perc:.2f}%")

        st.markdown(f"<div class='motivation-panel'>{random.choice(MOTIVATIONAL_PHRASES)}</div>", unsafe_allow_html=True)

        if leaderboard:
            df_leaderboard = pd.DataFrame(leaderboard).sort_values(by="Sort_Perc", ascending=False).reset_index(drop=True)
            df_leaderboard.index += 1
            df_leaderboard["Rank"] = df_leaderboard.index.map(lambda x: f"#{x}")
            
            # Format and display table
            df_display = df_leaderboard[["Rank", "Name", "Release", "Unrelease", "Transfer", "Deficit", "Percentage", "Status"]]
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("No members added yet. Click 'COUNT ME IN' to add members.")

    # ================== MEMBER TABS ==================
    for i, name in enumerate(member_names):
        with tabs[i + 1]:
            col_title, col_remove = st.columns([5, 1])
            with col_title:
                st.markdown(f"<h2>{name.upper()}</h2>", unsafe_allow_html=True)
            with col_remove:
                with st.popover("🗑️ REMOVE"):
                    st.write(f"Remove {name}?")
                    if st.button("Confirm", key=f"del_{name}"):
                        del st.session_state['members'][name]
                        CloudSync.save_data(st.session_state['members'])
                        st.rerun()
            
            data = st.session_state['members'][name]
            perc, df = calculate_metrics(data)
            status = "NO DATA" if data["release"] == 0 and data["unrelease"] == 0 else "PASSING" if perc >= 85 else "BELOW TARGET"
            status_color = "#A1A1AA" if status == "NO DATA" else "#22C55E" if status == "PASSING" else "#EF4444"

            # Metric Cards
            m1, m2, m3, m4, m5 = st.columns(5)
            
            def update_val(n, metric, amount):
                st.session_state['members'][n][metric] = max(0, st.session_state['members'][n][metric] + amount)
                CloudSync.save_data(st.session_state['members'])
            
            # Helper to generate metric card + buttons
            def metric_card(col, css_class, title, metric_key, val):
                with col:
                    st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                    st.metric(title, val)
                    b1, b2 = st.columns(2)
                    if b1.button("−", key=f"min_{name}_{metric_key}", use_container_width=True):
                        update_val(name, metric_key, -1)
                        st.rerun()
                    if b2.button("➕", key=f"plus_{name}_{metric_key}", use_container_width=True):
                        update_val(name, metric_key, 1)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

            metric_card(m1, "metric-RELEASE", "RELEASE", "release", data["release"])
            metric_card(m2, "metric-UNRELEASE", "UNRELEASE", "unrelease", data["unrelease"])
            metric_card(m3, "metric-TRANSFER", "TRANSFER", "transfer", data["transfer"])

            with m4:
                st.markdown('<div class="metric-DEFICIT">', unsafe_allow_html=True)
                st.metric("DEFICIT", df)
                st.markdown("<p style='text-align: center; color: #71717A; font-size: 0.8rem;'>AUTO</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with m5:
                st.markdown('<div class="metric-PERCENTAGE">', unsafe_allow_html=True)
                st.metric("PERCENTAGE", f"{perc:.2f}%")
                st.markdown("<p style='text-align: center; color: #71717A; font-size: 0.8rem;'>AUTO</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Status and Motivation
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="glass-container">
                    <p style='color: #A1A1AA; font-size: 0.9rem; font-weight: bold; margin-bottom: 0;'>CURRENT PERFORMANCE STATUS</p>
                    <h2 style='color: {status_color}; margin-top: 5px;'>{status}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<div class='motivation-panel' style='margin-top: 15px;'>{random.choice(MOTIVATIONAL_PHRASES)}</div>", unsafe_allow_html=True)


# ============================================================
# MAIN EXECUTION
# ============================================================
def main():
    inject_custom_css()
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    if not st.session_state['logged_in']:
        authenticate()
    else:
        if 'members' not in st.session_state:
            fetch_latest_data()
        render_main_app()

if __name__ == "__main__":
    main()
