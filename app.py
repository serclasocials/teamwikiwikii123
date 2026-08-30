import json
import math
import random
import time
import urllib.error
import urllib.request
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(page_title="CLUSTER ARLEN | TEAM REEYAAA", page_icon="📊", layout="wide")

# ============================================================
# CLOUD CONFIGURATION (JSONBin.io) & SECURITY
# ============================================================
JSONBIN_BIN_ID = "6a939368da38895dfe21c244"
JSONBIN_MASTER_KEY = ("$2a$10$N6A/7tTzu0bIYUNeer5RveMMym14VTQdspb2Rd64c80KH3WZVKIXa")
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
          headers={
              "X-Master-Key": JSONBIN_MASTER_KEY,
              "X-Access-Key": "",
          },
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
# CUSTOM STYLING (MATCHING ORIGINAL DARK GLASS DESIGN)
# ============================================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #08080D;
        color: #FFFFFF;
    }
    .glass-card {
        background-color: #151520;
        border: 1px solid #303044;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 5px;
    }
    .motivation-box {
        background-color: #1D1D2B;
        border: 1px solid #5B21B6;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        color: #FACC15;
        font-style: italic;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 15px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
    "Wikiiii-wikiiiiiiiiiiiiii.",
    "Magpag-pag, kung maraming DROP!",
    "Your effort today builds your performance tomorrow.",
    "Do not stop. Keep working toward your target.",
    "One good call can start a better streak.",
    "Wikiiii-wikiiiiiiiiiiiiii.",
    "Magpag-pag, kung maraming DROP!",
    "Keep your momentum going.",
    "Believe in your progress and continue improving.",
]

# ============================================================
# SESSION STATE INITIALIZATION & CLOUD SYNC
# ============================================================
if "authenticated" not in st.session_state:
  st.session_state.authenticated = False

if "members" not in st.session_state:
  cloud_data = CloudSync.load_data()
  st.session_state.members = (
      cloud_data if isinstance(cloud_data, dict) else {}
  )

if "current_motivation" not in st.session_state:
  st.session_state.current_motivation = random.choice(MOTIVATIONAL_PHRASES)

# ============================================================
# AUTHENTICATION SCREEN
# ============================================================
if not st.session_state.authenticated:
  st.markdown("<br><br><br>", unsafe_allow_html=True)
  col1, col2, col3 = st.columns([1, 1.2, 1])
  with col2:
    st.markdown(
        """
            <div style="background-color: #151520; border: 1px solid #303044; padding: 30px; border-radius: 12px; text-align: center;">
                <h2 style="color: #FFFFFF; margin-bottom: 0px;">CLUSTER ARLEN</h2>
                <p style="color: #A1A1AA; font-size: 0.9rem;">Enter Password to Access System</p>
            </div>
            """,
        unsafe_allow_html=True,
    )
    pass_input = st.text_input(
        "Password", type="password", label_visibility="collapsed"
    )
    if st.button("LOGIN", use_container_width=True):
      if pass_input == ACCESS_PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
      else:
        st.error("Incorrect Password. Please try again.")
  st.stop()

# ============================================================
# MAIN HEADER
# ============================================================
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 10px;">
        <h1 style="color: #FFFFFF; font-size: 2.3rem; margin-bottom: 0px;">CLUSTER ARLEN</h1>
        <h3 style="color: #A78BFA; font-size: 1.2rem; margin-top: 0px;">TEAM REEYAAA WIKI-WIKIIIIII</h3>
        <p style="color: #A1A1AA; font-size: 0.85rem;">Programmed by: @CLA TECHFORGE | Clarence Gabriel Obida | @serclasocials</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def calculate_metrics(release, unrelease):
  total = release + unrelease
  percentage = 0 if total == 0 else (release / total) * 100
  deficit = max(0, (unrelease * 6) - release)
  return percentage, deficit


def sync_to_cloud():
  CloudSync.save_data(st.session_state.members)


# ============================================================
# CONTROLS BAR (RESET ALL & ADD MEMBER)
# ============================================================
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([5, 1.3, 1.7])
with ctrl_col2:
  if st.button("RESET ALL", use_container_width=True):
    confirm_wipe = st.checkbox("Check to confirm full reset")
    if confirm_wipe:
      st.session_state.members = {}
      CloudSync.save_data({})
      st.success("All data wiped successfully!")
      st.rerun()

with ctrl_col3:
  new_member_name = st.text_input(
      "New Member Name",
      placeholder="Enter name...",
      label_visibility="collapsed",
  )
if st.button("+ COUNT ME IN"):
  if new_member_name:
    clean_name = new_member_name.strip()
    if clean_name in st.session_state.members:
      st.warning("This team member already exists.")
    else:
      st.session_state.members[clean_name] = {
          "release": 0,
          "unrelease": 0,
          "transfer": 0,
      }
      sync_to_cloud()
      st.rerun()

st.markdown("<hr style='margin: 10px 0px;'>", unsafe_allow_html=True)

# ============================================================
# TABS SETUP (MATCHING ORIGINAL NOTEBOOK TABS LAYOUT)
# ============================================================
tab_names = ["LEADER DASHBOARD"] + list(st.session_state.members.keys())
tabs = st.tabs(tab_names)

# ============================================================
# TAB 1: LEADER DASHBOARD
# ============================================================
with tabs[0]:
  st.markdown(
      """
        <div style="text-align: center;">
            <h2 style="color: #FFFFFF; margin-bottom: 0px;">TEAM PERFORMANCE DASHBOARD</h2>
            <p style="color: #A78BFA; font-weight: bold; font-size: 0.9rem;">LIVE TEAM METRICS OVERVIEW & RANKINGS</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  total_members = len(st.session_state.members)
  tot_release = sum(d["release"] for d in st.session_state.members.values())
  tot_unrelease = sum(d["unrelease"] for d in st.session_state.members.values())
  tot_transfer = sum(d["transfer"] for d in st.session_state.members.values())

  tot_deficit = 0
  member_stats = []
  for name, data in st.session_state.members.items():
    perc, df = calculate_metrics(data["release"], data["unrelease"])
    tot_deficit += df
    status = (
        "NO DATA"
        if data["release"] == 0 and data["unrelease"] == 0
        else "PASSING"
        if perc >= 85
        else "BELOW TARGET"
    )
    member_stats.append({
        "name": name,
        "release": data["release"],
        "unrelease": data["unrelease"],
        "transfer": data["transfer"],
        "deficit": df,
        "percentage": perc,
        "status": status,
    })

  tot_calls = tot_release + tot_unrelease
  group_percentage = (
      0 if tot_calls == 0 else (tot_release / tot_calls) * 100
  )

  # Summary Cards
  c1, c2, c3, c4, c5 = st.columns(5)
  with c1:
    st.markdown(
        f'<div class="glass-card"><p style="color:#A1A1AA;font-size:0.75rem;margin:0;">MEMBERS</p><h3'
        f' style="color:#A78BFA;margin:0;">{total_members}</h3></div>',
        unsafe_allow_html=True,
    )
  with c2:
    st.markdown(
        f'<div class="glass-card"><p style="color:#A1A1AA;font-size:0.75rem;margin:0;">RELEASE</p><h3'
        f' style="color:#22C55E;margin:0;">{tot_release}</h3></div>',
        unsafe_allow_html=True,
    )
  with c3:
    st.markdown(
        f'<div class="glass-card"><p style="color:#A1A1AA;font-size:0.75rem;margin:0;">UNRELEASE</p><h3'
        f' style="color:#EF4444;margin:0;">{tot_unrelease}</h3></div>',
        unsafe_allow_html=True,
    )
  with c4:
    st.markdown(
        f'<div class="glass-card"><p style="color:#A1A1AA;font-size:0.75rem;margin:0;">DEFICIT</p><h3'
        f' style="color:#FACC15;margin:0;">{tot_deficit}</h3></div>',
        unsafe_allow_html=True,
    )
  with c5:
    st.markdown(
        f'<div class="glass-card"><p style="color:#A1A1AA;font-size:0.75rem;margin:0;">GROUP'
        f' %</p><h3 style="color:#A78BFA;margin:0;">{group_percentage:.2f}%</h3></div>',
        unsafe_allow_html=True,
    )

  # Motivation Panel
  st.markdown(
      f'<div'
      f' class="motivation-box">{st.session_state.current_motivation}</div>',
      unsafe_allow_html=True,
  )

  # Rankings Table
  st.markdown("### 📋 Team Member Rankings")
  if member_stats:
    member_stats.sort(key=lambda x: x["percentage"], reverse=True)
    table_data = []
    for rank, stats in enumerate(member_stats, start=1):
      table_data.append({
          "Rank": f"#{rank}",
          "Team Member": stats["name"],
          "Release": stats["release"],
          "Unrelease": stats["unrelease"],
          "Transfer": stats["transfer"],
          "Deficit": stats["deficit"],
          "Percentage": f"{stats['percentage']:.2f}%",
          "Status": stats["status"],
      })
    st.dataframe(table_data, use_container_width=True, hide_index=True)
  else:
    st.info(
        "No team members added yet. Use '+ COUNT ME IN' to add team members."
    )

# ============================================================
# TABS 2+: INDIVIDUAL MEMBER TABS
# ============================================================
for idx, name in enumerate(st.session_state.members.keys()):
  with tabs[idx + 1]:
    col_title, col_del = st.columns([6, 1])
    with col_title:
      st.markdown(
          f"<h2 style='color:#FFFFFF;margin-bottom:0px;'>{name.upper()}</h2>",
          unsafe_allow_html=True,
      )
    with col_del:
      if st.button("REMOVE", key=f"del_{name}"):
        del st.session_state.members[name]
        sync_to_cloud()
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Metrics Layout & Increment Controls
    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
      st.markdown(
          f'<div class="glass-card"><p'
          f' style="color:#22C55E;font-weight:bold;font-size:0.9rem;">RELEASE</p><h2'
          f' style="color:#FFFFFF;margin:0;">{st.session_state.members[name]["release"]}</h2></div>',
          unsafe_allow_html=True,
      )
      b1, b2 = st.columns(2)
      with b1:
        if st.button("−", key=f"rel_sub_{name}", use_container_width=True):
          st.session_state.members[name]["release"] = max(
              0, st.session_state.members[name]["release"] - 1
          )
          st.session_state.current_motivation = random.choice(
              MOTIVATIONAL_PHRASES
          )
          sync_to_cloud()
          st.rerun()
      with b2:
        if st.button("+", key=f"rel_add_{name}", use_container_width=True):
          st.session_state.members[name]["release"] += 1
          st.session_state.current_motivation = random.choice(
              MOTIVATIONAL_PHRASES
          )
          sync_to_cloud()
          st.rerun()

    with m2:
      st.markdown(
          f'<div class="glass-card"><p'
          f' style="color:#EF4444;font-weight:bold;font-size:0.9rem;">UNRELEASE</p><h2'
          f' style="color:#FFFFFF;margin:0;">{st.session_state.members[name]["unrelease"]}</h2></div>',
          unsafe_allow_html=True,
      )
      b1, b2 = st.columns(2)
      with b1:
        if st.button("−", key=f"unrel_sub_{name}", use_container_width=True):
          st.session_state.members[name]["unrelease"] = max(
              0, st.session_state.members[name]["unrelease"] - 1
          )
          st.session_state.current_motivation = random.choice(
              MOTIVATIONAL_PHRASES
          )
          sync_to_cloud()
          st.rerun()
      with b2:
        if st.button("+", key=f"unrel_add_{name}", use_container_width=True):
          st.session_state.members[name]["unrelease"] += 1
          st.session_state.current_motivation = random.choice(
              MOTIVATIONAL_PHRASES
          )
          sync_to_cloud()
          st.rerun()

    with m3:
      st.markdown(
          f'<div class="glass-card"><p'
          f' style="color:#FACC15;font-weight:bold;font-size:0.9rem;">TRANSFER</p><h2'
          f' style="color:#FFFFFF;margin:0;">{st.session_state.members[name]["transfer"]}</h2></div>',
          unsafe_allow_html=True,
      )
      b1, b2 = st.columns(2)
      with b1:
        if st.button("−", key=f"tr_sub_{name}", use_container_width=True):
          st.session_state.members[name]["transfer"] = max(
              0, st.session_state.members[name]["transfer"] - 1
          )
          st.session_state.current_motivation = random.choice(
              MOTIVATIONAL_PHRASES
          )
          sync_to_cloud()
          st.rerun()
      with b2:
        if st.button("+", key=f"tr_add_{name}", use_container_width=True):
          st.session_state.members[name]["transfer"] += 1
          st.session_state.current_motivation = random.choice(
              MOTIVATIONAL_PHRASES
          )
          sync_to_cloud()
          st.rerun()

    percentage, deficit = calculate_metrics(
        st.session_state.members[name]["release"],
        st.session_state.members[name]["unrelease"],
    )

    with m4:
      st.markdown(
          f'<div class="glass-card"><p'
          f' style="color:#EF4444;font-weight:bold;font-size:0.9rem;">DEFICIT</p><h2'
          f' style="color:#FFFFFF;margin:0;">{deficit}</h2><p'
          f' style="color:#A1A1AA;font-size:0.7rem;margin:0;">AUTO</p></div>',
          unsafe_allow_html=True,
      )

    with m5:
      st.markdown(
          f'<div class="glass-card"><p'
          f' style="color:#A78BFA;font-weight:bold;font-size:0.9rem;">PERCENTAGE</p><h2'
          f' style="color:#FFFFFF;margin:0;">{percentage:.2f}%</h2><p'
          f' style="color:#A1A1AA;font-size:0.7rem;margin:0;">AUTO</p></div>',
          unsafe_allow_html=True,
      )

    # Status Panel
    rel_val = st.session_state.members[name]["release"]
    unrel_val = st.session_state.members[name]["unrelease"]
    if rel_val == 0 and unrel_val == 0:
      status_text, status_color = "NO DATA", "#A1A1AA"
    elif percentage >= 85:
      status_text, status_color = "PASSING", "#22C55E"
    else:
      status_text, status_color = "BELOW TARGET", "#EF4444"

    st.markdown(
        f"""
        <div style="background-color: #151520; border: 1px solid #303044; padding: 12px; border-radius: 8px; text-align: center; margin-top: 15px;">
            <p style="color: #A1A1AA; font-size: 0.8rem; margin-bottom: 2px;">CURRENT PERFORMANCE STATUS</p>
            <h2 style="color: {status_color}; margin-top: 0px; margin-bottom: 0px;">{status_text}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Motivation Panel
    st.markdown(
        f'<div'
        f' class="motivation-box">{st.session_state.current_motivation}</div>',
        unsafe_allow_html=True,
    )