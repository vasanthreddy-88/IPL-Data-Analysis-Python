# 🏏 IPL Data Analysis & Geospatial Visualization (Python)

An end-to-end Exploratory Data Analysis (EDA) project on the Indian Premier League (IPL) dataset using **Python**. This project cleans match and delivery-level data, extracts statistical insights on players and teams, analyzes season trends, and generates an interactive map of match venues.

---

## 📌 Project Overview

This script processes two primary datasets (`matches.csv` and `deliveries.csv`) to provide comprehensive insights at both the **match level** and **ball-by-ball level**:
* Data cleaning, missing value imputation, and column standardization.
* Feature engineering (calculating boundaries, dot balls, strike rates, economy rates, and win conditions).
* Statistical analysis of top batsmen, bowlers, team wins, and toss impacts.
* Trend analysis across seasons (average runs per match, Orange/Purple Cap holders).
* Geospatial visual mapping of match distribution across host cities using **Folium**.

---

## 🛠️ Tools & Libraries Used

* **Pandas & NumPy:** Data loading, transformation, feature engineering, and aggregations.
* **Matplotlib & Seaborn:** Static statistical charts, trend lines, and bar charts.
* **Folium:** Interactive map generation using geographical coordinates.

---

## 🔑 Key Features & Insights Covered

### 1. Data Cleaning & Feature Engineering
* Handled missing values in `city` and `winner` columns.
* Standardized column headers (`lowercase` and `stripped spaces`).
* Derived metrics: `win_by_runs`, `win_by_wickets`, `is_boundary`, `is_dot_ball`, `strike_rate`, and `economy_rate`.

### 2. Match & Team Level Analysis
* **Matches per Season:** Historical trend of matches played each season.
* **Top 10 Successful Teams:** Bar chart analysis of most wins.
* **Toss Impact:** Evaluated if winning the toss correlates directly with winning the match.
* **Toss Decision Strategy:** Total runs scored categorized by decision to bat or field first.

### 3. Ball-Level & Player Metrics
* **Top Batsmen:** Ranked by overall runs scored and strike rate (filtered for minimum balls faced).
* **Top Bowlers:** Ranked by total wickets, economy rates, and dot ball percentages.
* **Orange & Purple Cap Holders:** Automatically derived seasonal leaders for total runs and wickets.

### 4. Geospatial Mapping
* Mapped venue cities using `Folium` with dynamically sized circle markers based on total match counts.
* Exported map output directly to `ipl_map.html`.

---

## 📁 How to Run the Code

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
