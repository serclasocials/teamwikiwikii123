import json
import random
import urllib.error
import urllib.request
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="CLUSTER ARLEN | TEAM REEYAAA", page_icon="📊", layout="wide"
)

# ============================================================
# CLOUD CONFIGURATION (JSONBin.io) & SECURITY
# ============================================================
JSONBIN_BIN_ID = "6a939368da38895dfe21c244"
JSONBIN_MASTER_KEY = (
    "$2a$10$N6A/7tTzu0bIYUNeer5RveMMym14VTQdspb2Rd64c80KH3WZVKIXa"
)
ACCESS_PASSWORD = "wikiwiki123"

class CloudSync:
    @staticmethod
    def load_data():
        if not JSONBIN_BIN_ID or not JSONBIN_MASTER_KEY:
            return None
        try:
            url = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}/latest"
            req = urllib.request.Request(
                url,
                headers={"X-Master-Key": JSONBIN_MASTER_KEY}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                res = json.loads(response.read().decode())
                return res.get("record", {})
        except Exception:
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
        except Exception:
            return False

# ============================================================
# CUSTOM STYLING & PHRASES
# ============================================================
st.markdown(
    """
    <style>
    .stApp { background-color: #08080D; color: #FFFFFF; }
    .glass-card { background-color: #151520; border: 1px solid #303044; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 5px; }
    .motivation-box { background-color: #1D1D2B; border: 1px solid #5B21B6; padding: 15px; border-radius: 8px; text-align: center; color: #FACC15; font-style: italic; font-weight: bold; font-size: 1.1rem; margin-bottom: 15px; margin-top: 10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

MOTIVATIONAL_PHRASES = [
    "Keep going. Every call is another opportunity to improve.",
    "Progress is built one call at a time.",
    "Wikiiii-wikiiiiiiiiiiiiii.",
    "Magpag-pag, kung maraming DROP!",
    "Stay calm, stay focused, and keep improving.",
]

# ============================================================
# SESSION STATE INIT & CALLBACKS (THE FIX FOR SYNCING)
# ============================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "members" not in st.session_state:
    cloud_data = CloudSync.load_data()
    st.session_state.members = cloud_data if cloud_data is not None else {}

if "current_motivation" not in st.session_state:
    st.session_state.current_motivation = random.choice(MOTIVATIONAL_PHRASES)

def modify_stat(member_name, stat_type, amount):
    # Always pull the freshest data right before modifying to prevent overwriting
    latest_data = CloudSync.load_data()
    if latest_data is not None:
        st.session_state.members = latest_data
        
    if member_name in st.session_state.members:
        current_val = st.session_state.members[member_name][stat_type]
        st.session_state.members[member_name][stat_type] = max(0, current_val + amount)
        st.session_state.current_motivation = random.choice(MOTIVATIONAL_PHRASES)
        CloudSync.save_data(st.session_state.members)

def remove_member(member_name):
    latest_data = CloudSync.load_data()
    if latest_data is not None:
        st.session_state.members = latest_data
        
    if member_name in st.session_state.members:
        del st.session_state.members[member_name]
        CloudSync.save_data(st.session_state.members)

# ============================================================
# AUTHENTICATION SCREEN
# ============================================================
if not st.session_state.authenticated:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown(
            """<div style="background-color: #151520; border: 1px solid #303044; padding: 30px; border-radius: 12px; text-align: center;">
            <h2 style="color: #FFFFFF; margin-bottom: 0px;">CLUSTER ARLEN</h2>
            <p style="color: #A1A1AA; font-size: 0.9rem;">Enter Password to Access System</p></div>""",
            unsafe_allow_html=True,
        )
        pass_input = st.text_input("Password", type="password", label_visibility="collapsed")
        if st.button("LOGIN", use_container_width=True):
            if pass_input == ACCESS_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect Password. Please try again.")
    st.stop()

# ============================================================
# MAIN HEADER & CONTROLS
# ============================================================
st.markdown(
    """<div style="text-align: center; margin-bottom: 10px;">
    <h1 style="color: #FFFFFF; font-size: 2.3rem; margin-bottom: 0px;">CLUSTER ARLEN</h1>
    <h3 style="color: #A78BFA; font-size: 1.2rem; margin-top: 0px;">TEAM REEYAAA WIKI-WIKIIIIII</h3>
    <p style="color: #A1A1AA; font-size: 0.85rem;">Programmed by: @CLA TECHFORGE | Clarence Gabriel Obida</p>
    </div>""",
    unsafe_allow_html=True,
)

ctrl_col1, ctrl_col_sync, ctrl_col2, ctrl_col3 = st.columns([4, 1.5, 1.5, 2])
with ctrl_col_sync:
    if st.button("🔄 SYNC CLOUD", use_container_width=True):
        latest = CloudSync.load_data()
        if latest is not None:
            st.session_state.members = latest
            st.success("Synced!")
with ctrl_col2:
    if st.button("RESET ALL", use_container_width=True):
        confirm_wipe = st.checkbox("Check to confirm full reset")
        if confirm_wipe:
            CloudSync.save_data({})
            st.session_state.members = {}
            st.rerun()
with ctrl_col3:
    new_member_name = st.text_input("New Member", placeholder="Enter name...", label_visibility="collapsed")
    if st.button("+ COUNT ME IN", use_container_width=True):
        if new_member_name:
            clean = new_member_name.strip()
            latest = CloudSync.load_data()
            if latest is not None: st.session_state.members = latest
            if clean not in st.session_state.members:
                st.session_state.members[clean] = {"release": 0, "unrelease": 0, "transfer": 0}
                CloudSync.save_data(st.session_state.members)
                st.rerun()

st.markdown("<hr style='margin: 10px 0px;'>", unsafe_allow_html=True)

# ============================================================
# TABS SETUP
# ============================================================
def calculate_metrics(release, unrelease):
    total = release + unrelease
    percentage = 0 if total == 0 else (release / total) * 100
    deficit = max(0, (unrelease * 6) - release)
    return percentage, deficit

member_names = list(st.session_state.members.keys())
tab_names = ["LEADER DASHBOARD"] + member_names
tabs = st.tabs(tab_names)

# ============================================================
# TAB 1: LEADER DASHBOARD
# ============================================================
with tabs[0]:
    st.markdown("""<div style="text-align: center;"><h2 style="color: #FFFFFF; margin-bottom: 0px;">TEAM PERFORMANCE DASHBOARD</h2>
    <p style="color: #A78BFA; font-weight: bold; font-size: 0.9rem;">LIVE TEAM METRICS OVERVIEW & RANKINGS</p></div>""", unsafe_allow_html=True)

    tot_rel = sum(d.get("release", 0) for d in st.session_state.members.values())
    tot_unrel = sum(d.get("unrelease", 0) for d in st.session_state.members.values())
    
    member_stats, tot_deficit = [], 0
    for name, data in st.session_state.members.items():
        perc, df = calculate_metrics(data.get("release", 0), data.get("unrelease", 0))
        tot_deficit += df
        status = "NO DATA" if data.get("release",0)==0 and data.get("unrelease",0)==0 else "PASSING" if perc >= 85 else "BELOW TARGET"
        member_stats.append({"name": name, "release": data.get("release",0), "unrelease": data.get("unrelease",0), "transfer": data.get("transfer",0), "deficit": df, "percentage": perc, "status": status})

    group_perc = 0 if (tot_rel + tot_unrel) == 0 else (tot_rel / (tot_rel + tot_unrel)) * 100

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(f'<div class="glass-card"><p style="color:#A1A1AA;font-size:0.75rem;margin:0;">MEMBERS</p><h3 style="color:#A78BFA;margin:0;">{len(member_names)}</h3></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="glass-card"><p style="color:#A1A1AA;font-size:0.75rem;margin:0;">RELEASE</p><h3 style="color:#22C55E;margin:0;">{tot_rel}</h3></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="glass-card"><p style="color:#A1A1AA;font-size:0.75rem;margin:0;">UNRELEASE</p><h3 style="color:#EF4444;margin:0;">{tot_unrel}</h3></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="glass-card"><p style="color:#A1A1AA;font-size:0.75rem;margin:0;">DEFICIT</p><h3 style="color:#FACC15;margin:0;">{tot_deficit}</h3></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="glass-card"><p style="color:#A1A1AA;font-size:0.75rem;margin:0;">GROUP %</p><h3 style="color:#A78BFA;margin:0;">{group_perc:.2f}%</h3></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="motivation-box">{st.session_state.current_motivation}</div>', unsafe_allow_html=True)

    st.markdown("### 📋 Team Member Rankings")
    if member_stats:
        member_stats.sort(key=lambda x: x["percentage"], reverse=True)
        table_data = [{"Rank": f"#{r}","Team Member": s["name"],"Release": s["release"],"Unrelease": s["unrelease"],"Transfer": s["transfer"],"Deficit": s["deficit"],"Percentage": f"{s['percentage']:.2f}%","Status": s["status"]} for r, s in enumerate(member_stats, 1)]
        st.dataframe(table_data, use_container_width=True, hide_index=True)
    else:
        st.info("No team members added yet. Use '+ COUNT ME IN' to add team members.")

# ============================================================
# INDIVIDUAL MEMBER TABS
# ============================================================
for idx, name in enumerate(member_names):
    with tabs[idx + 1]:
        col_title, col_del = st.columns([6, 1])
        col_title.markdown(f"<h2 style='color:#FFFFFF;margin-bottom:0px;'>{name.upper()}</h2>", unsafe_allow_html=True)
        col_del.button("REMOVE", key=f"del_{name}", on_click=remove_member, args=(name,))

        st.markdown("<br>", unsafe_allow_html=True)
        
        m1, m2, m3, m4, m5 = st.columns(5)
        member_data = st.session_state.members.get(name, {"release": 0, "unrelease": 0, "transfer": 0})

        with m1:
            st.markdown(f'<div class="glass-card"><p style="color:#22C55E;font-weight:bold;font-size:0.9rem;">RELEASE</p><h2 style="color:#FFFFFF;margin:0;">{member_data["release"]}</h2></div>', unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            b1.button("−", key=f"r_sub_{name}", use_container_width=True, on_click=modify_stat, args=(name, "release", -1))
            b2.button("+", key=f"r_add_{name}", use_container_width=True, on_click=modify_stat, args=(name, "release", 1))

        with m2:
            st.markdown(f'<div class="glass-card"><p style="color:#EF4444;font-weight:bold;font-size:0.9rem;">UNRELEASE</p><h2 style="color:#FFFFFF;margin:0;">{member_data["unrelease"]}</h2></div>', unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            b1.button("−", key=f"u_sub_{name}", use_container_width=True, on_click=modify_stat, args=(name, "unrelease", -1))
            b2.button("+", key=f"u_add_{name}", use_container_width=True, on_click=modify_stat, args=(name, "unrelease", 1))

        with m3:
            st.markdown(f'<div class="glass-card"><p style="color:#FACC15;font-weight:bold;font-size:0.9rem;">TRANSFER</p><h2 style="color:#FFFFFF;margin:0;">{member_data["transfer"]}</h2></div>', unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            b1.button("−", key=f"t_sub_{name}", use_container_width=True, on_click=modify_stat, args=(name, "transfer", -1))
            b2.button("+", key=f"t_add_{name}", use_container_width=True, on_click=modify_stat, args=(name, "transfer", 1))

        perc, dfc = calculate_metrics(member_data["release"], member_data["unrelease"])
        
        m4.markdown(f'<div class="glass-card"><p style="color:#EF4444;font-weight:bold;font-size:0.9rem;">DEFICIT</p><h2 style="color:#FFFFFF;margin:0;">{dfc}</h2><p style="color:#A1A1AA;font-size:0.7rem;margin:0;">AUTO</p></div>', unsafe_allow_html=True)
        m5.markdown(f'<div class="glass-card"><p style="color:#A78BFA;font-weight:bold;font-size:0.9rem;">PERCENTAGE</p><h2 style="color:#FFFFFF;margin:0;">{perc:.2f}%</h2><p style="color:#A1A1AA;font-size:0.7rem;margin:0;">AUTO</p></div>', unsafe_allow_html=True)

        status_txt, status_clr = ("NO DATA", "#A1A1AA") if member_data["release"]==0 and member_data["unrelease"]==0 else ("PASSING", "#22C55E") if perc >= 85 else ("BELOW TARGET", "#EF4444")
        st.markdown(f'<div style="background-color: #151520; border: 1px solid #303044; padding: 12px; border-radius: 8px; text-align: center; margin-top: 15px;"><p style="color: #A1A1AA; font-size: 0.8rem; margin-bottom: 2px;">CURRENT PERFORMANCE STATUS</p><h2 style="color: {status_clr}; margin-top: 0px; margin-bottom: 0px;">{status_txt}</h2></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="motivation-box">{st.session_state.current_motivation}</div>', unsafe_allow_html=True)
