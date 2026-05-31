import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="IITM BS GPA Calculator", layout="wide")
st.title("IITM BS CGPA & Grade Calculator")

# ---  CSS  ---
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"] p {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #1e293b !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #3b82f6 !important;
    }
    .stButton > button p {
        font-weight: bold !important;
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA DICTIONARIES ---
LEVELS = ["Foundation", "Diploma", "Degree"]

SUBJECT_DATABASE = {
    "Foundation": {
        "Mathematics I": 4, "English I": 4, "Computational Thinking": 4, "Statistics I": 4,
        "Mathematics II": 4, "English II": 4, "Python": 4, "Statistics II": 4
    },
    "Diploma": {
        "PDSA": 4, "DBMS": 4, "MLF": 4, "App Development 1": 4, "App Development 2": 4,
        "Java": 4, "System Commands": 4, "MLT": 4, "MLP": 4, "BDM": 4, "BA": 4, "TDS": 4
    },
    "Degree": {
        "Software Testing": 4, "Software Engineering": 4, "Deep Learning": 4, 
        "AI: Search Methods for Problem Solving": 4, "Strategies for Professional Growth": 4, 
        "Programming in C": 4, "Deep Learning for CV": 4, "Large Language Models": 4, 
        "Deep Learning Practice": 4, "Data Science and AI Lab": 4, "Application Development Lab": 4, 
        "Algorithmic Thinking in Bioinformatics": 4, "Market Research": 4, "Managerial Economics": 4, 
        "MLOps (Machine Learning Operations)": 4, "Mathematical Foundations of Generative AI": 4, 
        "Data Visualization Design": 4, "Design Thinking for Data-Driven App Development": 4, 
        "Privacy & Security in Online Social Media": 4, "Computer Systems Design": 4, 
        "Game Theory and Strategy": 4, "Algorithms for Data Science (ADS)": 4, 
        "Discrete Mathematics": 4, "Compiler Design": 4, "Theory of Computation": 4
    }
}

def get_letter_grade(t_score):
    t_score = min(t_score, 100.0)
    if t_score >= 90: return "S", 10, True
    elif t_score >= 80: return "A", 9, True
    elif t_score >= 70: return "B", 8, True
    elif t_score >= 60: return "C", 7, True
    elif t_score >= 50: return "D", 6, True
    elif t_score >= 40: return "E", 4, True
    else: return "U", 0, False

# --- INITIALIZE SESSION STATE ---
if "term_grades" not in st.session_state:
    st.session_state.term_grades = {}

# --- CONFIGURATION ---
st.header("Step 1: Term Configuration")
col1, col2 = st.columns(2)

with col1:
    selected_level = st.selectbox("Select your current program level:", LEVELS)

max_allowed = len(SUBJECT_DATABASE[selected_level])
with col2:
    num_subjects = st.number_input("How many subjects are you taking this term?", min_value=1, max_value=max_allowed, value=min(4, max_allowed))

st.markdown("---")

# --- SUBJECT SELECTION ---
st.header("Step 2: Select Your Subjects")
chosen_subjects = []

sub_cols = st.columns(num_subjects)
available_options = list(SUBJECT_DATABASE[selected_level].keys())

for i in range(num_subjects):
    with sub_cols[i]:
        default_idx = min(i, len(available_options) - 1)
        sub_name = st.selectbox(f"Subject {i+1}:", options=available_options, index=default_idx, key=f"sub_select_{i}")
        if sub_name not in chosen_subjects:
            chosen_subjects.append(sub_name)

st.markdown("---")

# --- MARKS FILLING DASHBOARD ---
st.header("Step 3: Score Entry Dashboard")

if chosen_subjects:
    tabs = st.tabs(chosen_subjects)
    
    for idx, subject in enumerate(chosen_subjects):
        with tabs[idx]:
            st.subheader(f"Assessment Scores for {subject}")
            t_score = 0.0
            
            # ==========================================
            # FOUNDATION LEVEL FORMULAS
            # ==========================================
            if subject in ["Mathematics I", "English I", "Computational Thinking", "English II"]:
                c1, c2, c3 = st.columns(3)
                qz1 = c1.number_input("Quiz 1", 0.0, 100.0, 0.0, key=f"q1_{subject}")
                qz2 = c2.number_input("Quiz 2", 0.0, 100.0, 0.0, key=f"q2_{subject}")
                f = c3.number_input("End Term", 0.0, 100.0, 0.0, key=f"f_{subject}")
                t_score = max((0.6 * f) + (0.3 * max(qz1, qz2)), (0.45 * f) + (0.25 * qz1) + (0.3 * qz2))

            elif subject in ["Statistics I", "Statistics II"]:
                c1, c2, c3, c4 = st.columns(4)
                qz1 = c1.number_input("Quiz 1", 0.0, 100.0, 0.0, key=f"q1_{subject}")
                qz2 = c2.number_input("Quiz 2", 0.0, 100.0, 0.0, key=f"q2_{subject}")
                f = c3.number_input("End Term", 0.0, 100.0, 0.0, key=f"f_{subject}")
                bonus_input = c4.number_input("Extra Activity Bonus (out of 5)", 0.0, 5.0, 0.0, key=f"b_{subject}")
                t_score = max((0.6 * f) + (0.3 * max(qz1, qz2)), (0.45 * f) + (0.25 * qz1) + (0.3 * qz2)) + bonus_input

            elif subject == "Mathematics II":
                c1, c2, c3, c4 = st.columns(4)
                qz1 = c1.number_input("Quiz 1", 0.0, 100.0, 0.0, key=f"q1_{subject}")
                qz2 = c2.number_input("Quiz 2", 0.0, 100.0, 0.0, key=f"q2_{subject}")
                f = c3.number_input("End Term", 0.0, 100.0, 0.0, key=f"f_{subject}")
                bonus_input = c4.number_input("Bonus (out of 6)", 0.0, 6.0, 0.0, key=f"b_{subject}")
                t_score = max((0.6 * f) + (0.3 * max(qz1, qz2)), (0.45 * f) + (0.25 * qz1) + (0.3 * qz2)) + bonus_input

            elif subject == "Python":
                c1, c2, c3, c4 = st.columns(4)
                qz1 = c1.number_input("Quiz 1", 0.0, 100.0, 0.0, key=f"q1_{subject}")
                pe1 = c2.number_input("OPPE 1", 0.0, 100.0, 0.0, key=f"pe1_{subject}")
                pe2 = c3.number_input("OPPE 2", 0.0, 100.0, 0.0, key=f"pe2_{subject}")
                f = c4.number_input("End Term", 0.0, 100.0, 0.0, key=f"f_{subject}")
                t_score = (0.15 * qz1) + (0.40 * f) + (0.25 * max(pe1, pe2)) + (0.20 * min(pe1, pe2))

            # ==========================================
            # DIPLOMA LEVEL FORMULAS
            # ==========================================
            elif subject == "PDSA":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA Score", 0.0, 100.0, 0.0, key="pdsa_gaa")
                pe = c2.number_input("OPPE Score", 0.0, 100.0, 0.0, key="pdsa_op")
                qz1 = c3.number_input("Quiz 1", 0.0, 100.0, 0.0, key="pdsa_qz1")
                qz2 = c4.number_input("Quiz 2", 0.0, 100.0, 0.0, key="pdsa_qz2")
                f = c5.number_input("End Term", 0.0, 100.0, 0.0, key="pdsa_f")
                bonus_input = st.number_input("Bonus Marks (out of 5)", 0.0, 5.0, 0.0, key="pdsa_bonus")
                t_score = (0.05 * gaa) + (0.2 * pe) + (0.45 * f) + max(0.2 * max(qz1, qz2), ((0.10 * qz1) + (0.20 * qz2))) + bonus_input

            elif subject in ["App Development 1", "App Development 2"]:
                c1, c2, c3, c4 = st.columns(4)
                gla = c1.number_input("GLA/GAA Score", 0.0, 100.0, 0.0, key=f"gla_{subject}")
                qz1 = c2.number_input("Quiz 1", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c3.number_input("Quiz 2", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                f = c4.number_input("End Term F", 0.0, 100.0, 0.0, key=f"f_{subject}")
                t_score = (0.05 * gla) + max(((0.6 * f) + (0.25 * max(qz1, qz2))), ((0.4 * f) + (0.25 * qz1) + (0.3 * qz2)))

            elif subject == "DBMS":
                c1, c2, c3, c4, c5, c6 = st.columns(6)
                gaa2 = c1.number_input("GAA2 W2-3", 0.0, 100.0, 0.0, key="dbms_gaa2")
                gaa3 = c2.number_input("GAA3 W7", 0.0, 100.0, 0.0, key="dbms_gaa3")
                pe = c3.number_input("OPPE Score", 0.0, 100.0, 0.0, key="dbms_opppe")
                qz1 = c4.number_input("Quiz 1", 0.0, 100.0, 0.0, key="dbms_qz1")
                qz2 = c5.number_input("Quiz 2", 0.0, 100.0, 0.0, key="dbms_qz2")
                f = c6.number_input("End Term", 0.0, 100.0, 0.0, key="dbms_f")
                bonus_input = st.number_input("Bonus Marks (out of 5)", 0.0, 5.0, 0.0, key="dbms_bonus")
                t_score = (0.03 * gaa2) + (0.02 * gaa3) + (0.2 * pe) + (0.45 * f) + max(0.2 * max(qz1, qz2), ((0.10 * qz1) + (0.20 * qz2))) + bonus_input

            elif subject == "Java":
                c1, c2, c3, c4, c5, c6 = st.columns(6)
                qz1 = c1.number_input("Quiz 1", 0.0, 100.0, 0.0, key=f"q1_{subject}")
                qz2 = c2.number_input("Quiz 2", 0.0, 100.0, 0.0, key=f"q2_{subject}")
                pe1 = c3.number_input("OPPE 1", 0.0, 100.0, 0.0, key=f"pe1_{subject}")
                pe2 = c4.number_input("OPPE 2", 0.0, 100.0, 0.0, key=f"pe2_{subject}")
                f = c5.number_input("End Term", 0.0, 100.0, 0.0, key=f"f_{subject}")
                gaa = c6.number_input("Average GrPA score", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                bonus_input = st.number_input("Bonus Marks (out of 10)", 0.0, 10.0, 0.0, key=f"bonus_{subject}")
                t_score = (0.05 * gaa) + (0.2 * max(pe1, pe2)) + (0.45 * f) + max((0.2 * max(qz1, qz2)), ((0.10 * qz1) + (0.20 * qz2))) + bonus_input

            elif subject == "System Commands":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA Score", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz1 = c2.number_input("Quiz 1", 0.0, 100.0, 0.0, key=f"q1_{subject}")
                f = c3.number_input("End Term", 0.0, 100.0, 0.0, key=f"f_{subject}")
                pe = c4.number_input("OPPE", 0.0, 100.0, 0.0, key=f"pe_{subject}")
                bpta = c5.number_input("BPTA Marks", 0.0, 100.0, 0.0, key=f"bpta_{subject}")
                t_score = (0.05 * gaa) + (0.25 * qz1) + (0.3 * pe) + (0.3 * f) + (0.1 * bpta)

            elif subject in ["MLF", "MLT"]:
                c1, c2, c3, c4 = st.columns(4)
                gaa = c1.number_input("GAA Score", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz1 = c2.number_input("Quiz 1", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c3.number_input("Quiz 2", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                f = c4.number_input("End Term", 0.0, 100.0, 0.0, key=f"f_{subject}")
                bonus_input = 0.0
                if subject == "MLF":
                    bonus_input = st.number_input("Bonus Marks (out of 5)", 0.0, 5.0, 0.0, key="mlf_bonus")
                t_score = (0.05 * gaa) + max((0.6 * f) + (0.25 * max(qz1, qz2)), (0.4 * f) + (0.25 * qz1) + (0.3 * qz2)) + bonus_input

            elif subject == "MLP":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA Score", 0.0, 100.0, 0.0, key="mlp_gaa")
                f = c2.number_input("End Term", 0.0, 100.0, 0.0, key="mlp_f")
                pe1 = c3.number_input("OPPE 1", 0.0, 100.0, 0.0, key="mlp_pe1")
                pe2 = c4.number_input("OPPE 2", 0.0, 100.0, 0.0, key="mlp_pe2")
                ka = c5.number_input("Average KA score", 0.0, 100.0, 0.0, key="mlp_ka")
                t_score = (0.1 * gaa) + (0.3 * f) + (0.20 * pe1) + (0.20 * pe2) + (0.20 * ka)

            elif subject == "BDM":
                c1, c2, c3, c4 = st.columns(4)
                gaa = c1.number_input("GAA Score", 0.0, 100.0, 0.0, key="bdm_gaa")
                qz1 = c2.number_input("Quiz 1", 0.0, 100.0, 0.0, key="bdm_qz1")
                qz2 = c3.number_input("Quiz 2", 0.0, 100.0, 0.0, key="bdm_qz2")
                f = c4.number_input("End Term", 0.0, 100.0, 0.0, key="bdm_f")
                t_score = (0.1 * gaa) + (0.5 * f) + (0.2 * qz1) + (0.2 * qz2)

            elif subject == "BA":
                c1, c2, c3, c4 = st.columns(4)
                gaa = c1.number_input("GAA Score (out of 20)", 0.0, 20.0, 0.0, key="ba_gaa")
                qz1 = c2.number_input("Quiz 1 (out of 20)", 0.0, 20.0, 0.0, key="ba_qz1")
                qz2 = c2.number_input("Quiz 2 (out of 20)", 0.0, 20.0, 0.0, key="ba_qz2")
                f = c4.number_input("End Term (out of 40)", 0.0, 40.0, 0.0, key="ba_f")
                t_score = gaa + 2 * (0.7 * max(qz1, qz2) + 0.3 * min(qz1, qz2)) + f

            elif subject == "TDS":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA Score", 0.0, 100.0, 0.0, key="tds_gaa")
                p1 = c1.number_input("Project 1 Score", 0.0, 100.0, 0.0, key="tds_p1")
                p2 = c2.number_input("Project 2 Score", 0.0, 100.0, 0.0, key="tds_p2")
                f = c3.number_input("End Term", 0.0, 100.0, 0.0, key="tds_f")
                roe = c4.number_input("ROE Score", 0.0, 100.0, 0.0, key="tds_roe")
                t_score = (0.2 * gaa) + (0.2 * roe) + (0.2 * p1) + (0.2 * p2) + (0.2 * f)

            # ==========================================
            # DEGREE LEVEL FORMULAS
            # ==========================================
            elif subject in ["Software Testing", "Managerial Economics", "Game Theory and Strategy", "Discrete Mathematics", "Compiler Design", "Theory of Computation"]:
                c1, c2, c3, c4 = st.columns(4)
                gaa_label = "GAA (Best 8 of 9)" if subject == "Managerial Economics" else ("GAA (First 9 Weeks)" if subject == "Theory of Computation" else "GAA (First 10 Weeks)")
                gaa = c1.number_input(gaa_label, 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz1 = c2.number_input("Quiz 1 Score", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c3.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                f = c4.number_input("End Term Score", 0.0, 100.0, 0.0, key=f"f_{subject}")
                t_score = (0.1 * gaa) + (0.4 * f) + (0.25 * qz1) + (0.25 * qz2)

            elif subject == "Software Engineering":
                c1, c2, c3 = st.columns(3)
                gaa = c1.number_input("GAA (10 Weekly Assgn)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz2 = c2.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                f = c3.number_input("End Term Score", 0.0, 100.0, 0.0, key=f"f_{subject}")
                
                c4, c5, c6, c7 = st.columns(4)
                gp1 = c4.number_input("Group Project M1-M2", 0.0, 100.0, 0.0, key=f"gp1_{subject}")
                gp2 = c5.number_input("Group Project M3-M5", 0.0, 100.0, 0.0, key=f"gp2_{subject}")
                pp = c6.number_input("Project Presentation (PP)", 0.0, 100.0, 0.0, key=f"pp_{subject}")
                cp = c7.number_input("Course Participation (CP)", 0.0, 100.0, 0.0, key=f"cp_{subject}")
                t_score = (0.05 * gaa) + (0.2 * qz2) + (0.4 * f) + (0.1 * gp1) + (0.1 * gp2) + (0.1 * pp) + (0.05 * cp)

            elif subject == "Deep Learning":
                c1, c2, c3, c4 = st.columns(4)
                gaa = c1.number_input("GAA (First 10 Weeks)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz1 = c2.number_input("Quiz 1 Score", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c3.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                f = c4.number_input("End Term Score", 0.0, 100.0, 0.0, key=f"f_{subject}")
                t_score = (0.05 * gaa) + (0.25 * qz1) + (0.25 * qz2) + (0.45 * f)

            elif subject == "AI: Search Methods for Problem Solving":
                c1, c2, c3, c4 = st.columns(4)
                gaa = c1.number_input("GAA (First 10 Weeks)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz1 = c2.number_input("Quiz 1 Score", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c3.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                f = c4.number_input("End Term Score", 0.0, 100.0, 0.0, key=f"f_{subject}")
                bonus = st.checkbox("Passed programming assignment for 5 bonus marks?", key=f"bonus_{subject}")
                
                base_score = (0.1 * gaa) + (0.4 * f) + (0.25 * qz1) + (0.25 * qz2)
                t_score = base_score + (5.0 if (bonus and base_score >= 40.0) else 0.0)

            elif subject == "Strategies for Professional Growth":
                c1, c2, c3, c4 = st.columns(4)
                gaa = c1.number_input("GAA (First 10 Weeks)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                gp = c2.number_input("Group Project Score", 0.0, 100.0, 0.0, key=f"gp_{subject}")
                qz2 = c3.number_input("Quiz 2 (Subj + Obj)", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                f = c4.number_input("Final Exam Score", 0.0, 100.0, 0.0, key=f"f_{subject}")
                t_score = (0.15 * gaa) + (0.25 * gp) + (0.25 * qz2) + (0.35 * f)

            elif subject == "Programming in C":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA (GA + GrPAs)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz1 = c2.number_input("Quiz 1 (In-Centre)", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                oppe1 = c3.number_input("OPPE 1 Score", 0.0, 100.0, 0.0, key=f"oppe1_{subject}")
                oppe2 = c4.number_input("OPPE 2 Score", 0.0, 100.0, 0.0, key=f"oppe2_{subject}")
                f = c5.number_input("Final End Term", 0.0, 100.0, 0.0, key=f"f_{subject}")
                t_score = (0.10 * gaa) + (0.20 * qz1) + (0.20 * oppe1) + (0.20 * oppe2) + (0.30 * f)

            elif subject == "Deep Learning for CV":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA (First 10 Weeks)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz1 = c2.number_input("Quiz 1 Score", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c3.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                f = c4.number_input("Final Exam Score", 0.0, 100.0, 0.0, key=f"f_{subject}")
                bonus = c5.number_input("Optional Project Bonus", 0.0, 5.0, 0.0, key=f"bonus_{subject}")
                t_score = (0.1 * gaa) + (0.4 * f) + (0.25 * qz1) + (0.25 * qz2) + bonus

            elif subject == "Large Language Models":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA (7 Assgn to W9)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz1 = c2.number_input("Quiz 1 Score", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c3.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                f = c4.number_input("End Term Score", 0.0, 100.0, 0.0, key=f"f_{subject}")
                prog_bonus = c5.number_input("Prog Assignment Average (Max 5)", 0.0, 5.0, 0.0, key=f"bonus_{subject}")
                
                base_score = (0.05 * gaa) + (0.35 * f) + (0.3 * qz1) + (0.3 * qz2)
                t_score = base_score + (prog_bonus if base_score >= 40.0 else 0.0)

            elif subject == "Deep Learning Practice":
                c1, c2, c3, c4 = st.columns(4)
                gaa = c1.number_input("GAA (Best 10 of 11)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz1 = c2.number_input("Quiz 1 Score", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c3.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                qz3 = c4.number_input("Quiz 3 Score", 0.0, 100.0, 0.0, key=f"qz3_{subject}")
                
                c5, c6, c7, c8 = st.columns(4)
                nppe1 = c5.number_input("NPPE 1 Score", 0.0, 100.0, 0.0, key=f"nppe1_{subject}")
                nppe2 = c6.number_input("NPPE 2 Score", 0.0, 100.0, 0.0, key=f"nppe2_{subject}")
                nppe3 = c7.number_input("NPPE 3 Score", 0.0, 100.0, 0.0, key=f"nppe3_{subject}")
                viva = c8.number_input("Viva Score", 0.0, 100.0, 0.0, key=f"viva_{subject}")
                
                nppe_avg = (nppe1 + nppe2 + nppe3) / 3.0
                t_score = (0.05 * gaa) + (0.15 * qz1) + (0.15 * qz2) + (0.15 * qz3) + (0.25 * nppe_avg) + (0.25 * viva)

            elif subject == "Data Science and AI Lab":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA (First 10 Weeks)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                quiz = c2.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"quiz_{subject}")
                p = c3.number_input("Project (Pres + Miles)", 0.0, 100.0, 0.0, key=f"p_{subject}")
                viva = c4.number_input("Viva Score", 0.0, 100.0, 0.0, key=f"viva_{subject}")
                bonus = c5.number_input("Bonus Assignments", 0.0, 5.0, 0.0, key=f"bonus_{subject}")
                t_score = (0.05 * gaa) + (0.25 * quiz) + (0.4 * p) + (0.3 * viva) + bonus

            elif subject == "Application Development Lab":
                c1, c2, c3 = st.columns(3)
                gaa = c1.number_input("GAA (First 10 Weeks)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz2 = c2.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                viva = c3.number_input("Project Viva Score", 0.0, 100.0, 0.0, key=f"viva_{subject}")
                t_score = (0.30 * gaa) + (0.20 * qz2) + (0.50 * viva)

            elif subject == "Algorithmic Thinking in Bioinformatics":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA (First 10 Weeks)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                grpa = c2.number_input("GRPA (3 Prog Assgn)", 0.0, 100.0, 0.0, key=f"grpa_{subject}")
                qz1 = c3.number_input("Quiz 1 (W1-4)", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c4.number_input("Quiz 2 (W5-8)", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                f = c5.number_input("Final Exam (W1-12)", 0.0, 100.0, 0.0, key=f"f_{subject}")
                t_score = (0.075 * gaa) + (0.025 * grpa) + (0.25 * qz1) + (0.25 * qz2) + (0.4 * f)

            elif subject == "Market Research":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA (First 10 Weeks)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz1 = c2.number_input("Quiz 1 Score", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c3.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                p = c4.number_input("Open Project Score", 0.0, 100.0, 0.0, key=f"p_{subject}")
                f = c5.number_input("Final Exam Score", 0.0, 100.0, 0.0, key=f"f_{subject}")
                t_score = (0.1 * gaa) + (0.2 * qz1) + (0.2 * qz2) + (0.25 * p) + (0.25 * f)

            elif subject == "MLOps (Machine Learning Operations)":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA (Best 9 of 11)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                oppe1 = c2.number_input("OPPE 1 Score", 0.0, 100.0, 0.0, key=f"oppe1_{subject}")
                oppe2 = c3.number_input("OPPE 2 Score", 0.0, 100.0, 0.0, key=f"oppe2_{subject}")
                f = c4.number_input("Final Exam Score", 0.0, 100.0, 0.0, key=f"f_{subject}")
                bonus = c5.number_input("Course Participation Bonus", 0.0, 5.0, 0.0, key=f"bonus_{subject}")
                t_score = (0.2 * gaa) + (0.3 * f) + (0.25 * oppe1) + (0.25 * oppe2) + bonus

            elif subject == "Mathematical Foundations of Generative AI":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA (Best 10 Assignments)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz1 = c2.number_input("Quiz 1 Score", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c3.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                nppe = c4.number_input("NPPE Prog Assignment", 0.0, 100.0, 0.0, key=f"nppe_{subject}")
                f = c5.number_input("Final Exam Score", 0.0, 100.0, 0.0, key=f"f_{subject}")
                t_score = (0.05 * gaa) + (0.35 * f) + (0.2 * qz1) + (0.2 * qz2) + (0.2 * nppe)

            elif subject == "Data Visualization Design":
                c1, c2, c3, c4, c5 = st.columns(5)
                ga = c1.number_input("GA (Sum of Best 3 of 5)", 0.0, 100.0, 0.0, key=f"ga_{subject}")
                qz1 = c2.number_input("Quiz 1 Score", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c3.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                p = c4.number_input("Project + Presentation", 0.0, 100.0, 0.0, key=f"p_{subject}")
                bonus = c5.number_input("Bonus Marks (Max 5)", 0.0, 5.0, 0.0, key=f"bonus_{subject}")
                t_score = (0.3 * ga) + max(0.2 * qz1 + 0.2 * qz2, 0.3 * max(qz1, qz2)) + (0.3 * p) + bonus

            elif subject == "Design Thinking for Data-Driven App Development":
                c1, c2, c3 = st.columns(3)
                gaa = c1.number_input("GAA (First 10 Weeks)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz2 = c2.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                f = c3.number_input("Final Exam Score", 0.0, 100.0, 0.0, key=f"f_{subject}")
                
                c4, c5, c6 = st.columns(3)
                gp1 = c4.number_input("Group Project GP1", 0.0, 100.0, 0.0, key=f"gp1_{subject}")
                gp2 = c5.number_input("Group Project GP2", 0.0, 100.0, 0.0, key=f"gp2_{subject}")
                gp3 = c6.number_input("Group Project GP3", 0.0, 100.0, 0.0, key=f"gp3_{subject}")
                t_score = (0.1 * gaa) + (0.1 * gp1) + (0.1 * gp2) + (0.2 * gp3) + (0.2 * qz2) + (0.3 * f)

            elif subject == "Privacy & Security in Online Social Media":
                c1, c2, c3, c4 = st.columns(4)
                gaa = c1.number_input("GAA (Best 10 Weekly)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz1 = c2.number_input("Quiz 1 Score", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c3.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                f = c4.number_input("End Term Exam", 0.0, 100.0, 0.0, key=f"f_{subject}")
                t_score = (0.2 * gaa) + (0.3 * f) + (0.25 * qz1) + (0.25 * qz2)

            elif subject == "Computer Systems Design":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA (10 Weekly Assgn)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                qz1 = c2.number_input("Quiz 1 Score", 0.0, 100.0, 0.0, key=f"qz1_{subject}")
                qz2 = c3.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                cv_assign = c4.number_input("CircuitVerse Assignment", 0.0, 100.0, 0.0, key=f"cv_{subject}")
                f = c5.number_input("Final Exam Score", 0.0, 100.0, 0.0, key=f"f_{subject}")
                t_score = (0.1 * gaa) + (0.4 * f) + (0.2 * qz1) + (0.25 * qz2) + (0.05 * cv_assign)

            elif subject == "Algorithms for Data Science (ADS)":
                c1, c2, c3, c4, c5 = st.columns(5)
                gaa = c1.number_input("GAA (W2,4,6,8,10)", 0.0, 100.0, 0.0, key=f"gaa_{subject}")
                paa = c2.number_input("PAA (PA1 + PA2 Avg)", 0.0, 100.0, 0.0, key=f"paa_{subject}")
                qz2 = c3.number_input("Quiz 2 Score", 0.0, 100.0, 0.0, key=f"qz2_{subject}")
                f = c4.number_input("Final Exam Score", 0.0, 100.0, 0.0, key=f"f_{subject}")
                bonus = c5.number_input("Quiz Bonus Questions", 0.0, 4.0, 0.0, key=f"bonus_{subject}")
                t_score = (0.1 * gaa) + (0.1 * paa) + (0.45 * f) + (0.35 * qz2) + bonus
            
            else:
                c1, c2, c3 = st.columns(3)
                gaa = c1.number_input("Assignment Average", 0.0, 100.0, 0.0, key=f"g_{idx}")
                qz = c2.number_input("Quiz Average", 0.0, 100.0, 0.0, key=f"q_{idx}")
                f = c3.number_input("Final Exam", 0.0, 100.0, 0.0, key=f"f_{idx}")
                t_score = (0.1 * gaa) + (0.3 * qz) + (0.6 * f)

            # Grade prediction logic
            # Evaluate Grades & Credit Eligibility
            letter, pts, is_passed = get_letter_grade(t_score)
            subject_credits = SUBJECT_DATABASE[selected_level].get(subject, 4)
            earned_credits = subject_credits if is_passed else 0
            
            # 1. Clicking the button saves the LATEST entered scores into Session State
            if st.button(f"✨ Calculate Grade for {subject}", key=f"calc_btn_{subject}"):
                st.session_state.term_grades[subject] = {
                    "t_score": t_score,
                    "grade": letter, 
                    "points": pts, 
                    "total_credits": subject_credits, 
                    "earned_credits": earned_credits,
                    "weighted_points": pts * subject_credits,
                    "is_passed": is_passed
                }
            
            # 2. This renders the results and STICKS around even when switching tabs!
            if subject in st.session_state.term_grades:
                cached = st.session_state.term_grades[subject]
                
                st.metric(label="Calculated Total Score", value=f"{round(min(cached['t_score'], 100.0), 2)}%")
                if cached["is_passed"]:
                    st.success(f"Predicted Final Grade: **{cached['grade']}** ({cached['points']} Points)")
                else:
                    st.error(f"❌ Predicted Grade: **{cached['grade']}** (Course Repeat Required)")
            

# --- OVERALL CUMULATIVE CGPA CALCULATOR ---
st.markdown("---")
st.header("Lifetime CGPA Tracker")
st.markdown("*Add your past terms data to see how your are actually performing right now.*")

col_prev_gpa, col_prev_credits = st.columns(2)
with col_prev_gpa:
    prev_cgpa = st.number_input("Your Cumulative CGPA prior to this term:", min_value=0.0, max_value=10.0, value=0.0, step=0.01)
with col_prev_credits:
    prev_credits = st.number_input("Total credits earned prior to this term:", min_value=0, max_value=120, value=0, step=4)

# Summary calculation
if st.button("🚀 Calculate Term & Total GPA"):
    if not st.session_state.term_grades:
        st.warning("Please click 'Calculate Grade' inside your subject tabs before analyzing total term distributions.")
    else:
        total_term_weighted_points = 0
        total_term_registered_credits = 0
        total_term_earned_credits = 0
        summary_data = []
        
        for sub in chosen_subjects:
            if sub in st.session_state.term_grades:
                data = st.session_state.term_grades[sub]
                total_term_weighted_points += data["weighted_points"]
                total_term_registered_credits += data["total_credits"]
                total_term_earned_credits += data["earned_credits"]
                
                summary_data.append({
                    "Subject": sub, 
                    "Registered Credits": data["total_credits"], 
                    "Predicted Grade": data["grade"],
                    "Earned Credits": data["earned_credits"]
                })
        
        if total_term_registered_credits > 0:
            term_gpa = round(total_term_weighted_points / total_term_registered_credits, 2)
            st.subheader("📋 Current Term Distribution Table")
            st.table(summary_data)
            
            # Lifetime Math integration logic
            past_weighted_points = prev_cgpa * prev_credits
            global_total_points = past_weighted_points + total_term_weighted_points
            global_total_credits = prev_credits + total_term_registered_credits
            
            overall_cgpa = round(global_total_points / global_total_credits, 2) if global_total_credits > 0 else 0.0
            
            # Final Report
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(label="Calculated Term GPA", value=f"{term_gpa} / 10.0")
            with m2:
                st.metric(label="Total Lifetime CGPA (All Terms Integrated)", value=f"{overall_cgpa} / 10.0", delta=round(overall_cgpa - prev_cgpa, 2) if prev_cgpa > 0 else None)
            with m3:
                st.metric(label="Total Program Credits", value=f"{prev_credits + total_term_earned_credits} Credits")
