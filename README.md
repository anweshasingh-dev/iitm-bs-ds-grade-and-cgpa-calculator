# IITM BS Grade & CGPA Calculator

## Project Overview
During my term break, I wanted to challenge myself and build something meaningful using what I’ve learned so far. Like every student after end-term exams, I was curious about my marks and GPA. I noticed everyone was either doing tedious manual calculations with complex formulas or hunting for online calculators. 

However, the existing calculators had a few frustrating gaps:
1. **Limited Scope:** Most of them only included Foundation level subjects, completely leaving out Diploma courses.
2. **Fragmented Experience:** Students had to use one tool to calculate individual grades, then switch to a completely different site to figure out their term GPA.
3. **No Lifetime Tracking:** There wasn't an easy way to combine new term grades with historical data to see an overall, cumulative CGPA.

I stumbled upon **Streamlit** while browsing for solutions and realized it was the exact tool I needed. I dove into tutorials, gathered the official grading policies for all levels (Foundation, Diploma, and Degree), and built an all-in-one, neat interface to solve these problems.

---

## Approach & Logic Blueprint

The core architecture of the application relies on a linear, top-to-bottom dependency chain where the input of one stage dynamically determines the output of the next.

[Level Selection] ➔ [Subject Selection] ➔ [Grade Calculation] ➔ [CGPA Calculation]


### PHASE 1: Pre-Preparation
* **Static Data Loading:** Pre-configured the application with official IITM grading formulas and credit allocations for every single subject across all tiers.

### PHASE 2: The 4-STAGE State Pipeline
* **STAGE 1: Level Selection**
  * *Input:* User selects their current academic tier (Foundation / Diploma / Degree).
  * *Output:* Filters the database and unlocks the corresponding subject pool.
* **STAGE 2: Subject Selection**
  * *Input:* User selects the specific subjects they are tracking this term.
  * *Output:* Dynamically generates customized entry forms and tabs for those exact subjects.
* **STAGE 3: Grade Calculation**
  * *Input:* User inputs component marks (Quizzes, End-Terms, Assignments, and Bonus marks).
  * *Logic:* Automatically applies specialized formulas to calculate `Final Score ➔ Letter Grade ➔ Grade Points`.
  * *Output:* Commits calculated metrics into a global tracker.
* **STAGE 4: CGPA Calculation**
  * *Input:* Pulls the freshly calculated term grades and combines them with the user's past CGPA and historical credits.
  * *Logic:* Computes total weighted points against cumulative registered credits.
  * *Output:* Displays a clean dashboard showing both the **Current Term GPA** and **Integrated Lifetime CGPA**.

### PHASE 3: State & Data Architecture
* **Centralized State Management:** Streamlit naturally reruns scripts on user interaction. To prevent data from wiping out, I implemented a centralized session state to ensure scores entered in Stage 3 accurately flow into Stage 4 without getting lost during UI updates.

---

## Hurdles Faced & How I Solved Them

* **UI Readability & Styling**
  * *Problem:* The default font styling for the subject sliders was easy to accidentally overlook. 
  * *Solution:* Researched Streamlit's capabilities and injected custom CSS tweaks to make the key interactive elements stand out clearly.
* **The "Resetting" Bug (State Management)**
  * *Problem:* Every time I finished calculating a grade for one subject and hopped over to the next tab, the previous tab's data would wipe out and reset to 0.
  * *Solution:* Learned how Streamlit handles data persistence. I refactored the logic using session state adjustments and careful loop tracking so variables remain securely stored throughout the user session.
