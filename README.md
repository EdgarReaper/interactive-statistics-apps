![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red)
![SciPy](https://img.shields.io/badge/SciPy-1.17-green)
![NumPy](https://img.shields.io/badge/NumPy-2.4-orange)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10-yellow)

# 📊 Interactive Statistics Apps

A collection of interactive statistical applications developed in Python with Streamlit for the **Statistics Labs II** course at the University of Minho.

This project combines theoretical probability concepts with practical exploratory data analysis through two web applications:

- 📈 **Beta Distribution Explorer**
- 🧬 **Obesity Dataset Exploratory Analysis**

> University project focused on probability distributions, statistical simulations, exploratory data analysis, confidence intervals, and interactive data visualization.

---

## 🌐 Live Applications

- Beta Distribution App:  
  [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://beta-app-h44xtkwzokiwkmcwpn7s7q.streamlit.app)

- Obesity Analysis App:  
  [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://obesity-app-goql8zqwhqrbsngv43wvaw.streamlit.app)

---

## 🚀 Applications

### 📈 Beta Distribution Explorer

Interactive application for exploring the properties of the Beta distribution.

#### Features

- Dynamic Beta PDF and CDF visualization
- Real-time parameter adjustment with sliders
- Statistical properties calculation:
  - Mean
  - Variance
  - Standard deviation
  - Mode
- Law of Large Numbers simulation
- Central Limit Theorem simulation
- Interactive graphical visualizations

---

### 🧬 Obesity Dataset Exploratory Analysis

Interactive exploratory analysis tool based on the **Obesity Levels Dataset** from the UCI Machine Learning Repository.

#### Features

- Descriptive statistics computation
- Histograms with KDE estimation
- Boxplots and comparative visualizations
- Confidence intervals for population means
- Group comparison by obesity level
- Interactive filtering and variable selection

Dataset includes:
- 2111 observations
- 17 variables
- Data from Mexico, Peru, and Colombia

---

## 📸 Preview

### Beta Distribution App

![Beta App Screenshot](images/beta_app.png)

### Obesity Analysis App

![Obesity App Screenshot](images/obesity_app.png)

---

## 🛠 Technologies Used

- Python
- Streamlit
- NumPy
- SciPy
- Matplotlib
- Pandas

---

## 🧠 What I Learned

- How to build and deploy interactive data applications using **Streamlit**
- Deep understanding of the **Beta distribution** - how shape parameters control the distribution and how to interpret PDF, CDF and quantiles
- Practical verification of the **Law of Large Numbers** and the **Central Limit Theorem** through simulation
- How to perform **exploratory data analysis** on a real-world dataset - descriptive statistics, histogram interpretation, boxplots and outlier detection
- How to compute and interpret **confidence intervals** for the mean using the t-Student distribution
- Working with **SciPy**, **NumPy** and **Matplotlib** for statistical computing and data visualisation
- Structuring a Python project for **GitHub** and deploying apps with **Streamlit Community Cloud**

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/EdgarReaper/interactive-statistics-apps.git
cd interactive-statistics-apps
pip install -r requirements.txt
streamlit run beta-app.py
streamlit run obesity-app.py
```

---

## 📁 Project Structure

```
interactive-statistics-apps/
│
├── apps/
│   ├── beta-app.py
│   └── obesity-app.py
│
├── data/
│   └── Obesity.csv
│
├── images/
│   ├── beta_app.png
│   └── obesity_app.png
│
├── requirements.txt
├── README.md
├── .gitattributes
└── .gitignore
```
