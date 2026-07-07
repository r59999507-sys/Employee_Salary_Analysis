import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="Employee Salary Analysis",
    page_icon="💼",
    layout="wide"
)

# =====================================
# Load Dataset
# =====================================

df = pd.read_csv("employee_salary_analysis.csv")

# Create Tax Column
df["Tax"] = df["Total_Salary"] * 0.10

# =====================================
# Sidebar
# =====================================

st.sidebar.title("💼 Employee Salary Dashboard")

page = st.sidebar.radio(

    "Choose Section",

    [

        "🏠 Home",

        "📋 Dataset",

        "📊 Statistics",

        "🔍 Filtering",

        "📈 Charts",

        "ℹ️ About"

    ]

)

# =====================================
# HOME
# =====================================

if page == "🏠 Home":

    st.title("💼 Employee Salary Analysis Dashboard")

    st.markdown("---")

    st.write("""
Welcome to the **Employee Salary Analysis Dashboard**.

This dashboard allows you to explore employee salary data,
analyze departments, compare salaries,
filter employees, and visualize workforce insights.
""")

    st.image(
        "https://images.unsplash.com/photo-1521791136064-7986c2920216?w=1200",
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("📊 Quick Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "Employees",

            len(df)

        )

    with col2:

        st.metric(

            "Departments",

            df["Department"].nunique()

        )

    with col3:

        st.metric(

            "Average Salary",

            f"${df['Total_Salary'].mean():,.0f}"

        )

    with col4:

        st.metric(

            "Highest Salary",

            f"${df['Total_Salary'].max():,.0f}"

        )

    st.markdown("---")

    st.subheader("Dataset Preview")

    st.dataframe(

        df.head(),

        use_container_width=True

    )

# =====================================
# DATASET
# =====================================

elif page == "📋 Dataset":

    st.title("📋 Employee Dataset")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Show First 10 Rows"):

            st.dataframe(

                df.head(10),

                use_container_width=True

            )

    with col2:

        if st.button("Show Last 10 Rows"):

            st.dataframe(

                df.tail(10),

                use_container_width=True

            )

    st.markdown("---")

    if st.button("Show Entire Dataset"):

        st.dataframe(

            df,

            use_container_width=True

        )

    st.markdown("---")

    st.subheader("Dataset Information")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Rows",

            df.shape[0]

        )

    with col2:

        st.metric(

            "Columns",

            df.shape[1]

        )

    st.markdown("---")

    if st.checkbox("Show Columns"):

        st.write(df.columns.tolist())

    if st.checkbox("Show Data Types"):

        st.dataframe(

            df.dtypes.astype(str),

            use_container_width=True

        )

    if st.checkbox("Show Statistical Summary"):

        st.dataframe(

            df.describe(),

            use_container_width=True

        )
# =====================================
# STATISTICS
# =====================================

elif page == "📊 Statistics":

    st.title("📊 Employee Statistics")

    st.subheader("Salary Statistics")

    salary = df["Total_Salary"].to_numpy()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Maximum Salary",
            f"${np.max(salary):,.0f}"
        )

        st.metric(
            "Mean Salary",
            f"${np.mean(salary):,.2f}"
        )

    with col2:

        st.metric(
            "Minimum Salary",
            f"${np.min(salary):,.0f}"
        )

        st.metric(
            "Total Salaries",
            f"${np.sum(salary):,.0f}"
        )

    st.markdown("---")

    st.subheader("GroupBy Analysis")

    option = st.selectbox(

        "Choose Analysis",

        [

            "Average Salary by Department",

            "Average Performance Rating by Gender",

            "Maximum Salary by Department",

            "Minimum Experience by Department",

            "Employee Count by Department"

        ]

    )

    if option == "Average Salary by Department":

        result = df.groupby(
            "Department"
        )["Total_Salary"].mean()

        st.dataframe(result)

    elif option == "Average Performance Rating by Gender":

        result = df.groupby(
            "Gender"
        )["Performance_Rating"].mean()

        st.dataframe(result)

    elif option == "Maximum Salary by Department":

        result = df.groupby(
            "Department"
        )["Salary"].max()

        st.dataframe(result)

    elif option == "Minimum Experience by Department":

        result = df.groupby(
            "Department"
        )["Experience_Years"].min()

        st.dataframe(result)

    elif option == "Employee Count by Department":

        result = df.groupby(
            "Department"
        )["Employee_ID"].count()

        st.dataframe(result)

# =====================================
# FILTERING
# =====================================

elif page == "🔍 Filtering":

    st.title("🔍 Filter Employees")

    department = st.selectbox(

        "Department",

        ["All"] + sorted(df["Department"].unique())

    )

    gender = st.selectbox(

        "Gender",

        ["All"] + sorted(df["Gender"].unique())

    )

    experience = st.slider(

        "Minimum Experience (Years)",

        int(df["Experience_Years"].min()),

        int(df["Experience_Years"].max()),

        0

    )

    salary = st.slider(

        "Minimum Salary",

        int(df["Total_Salary"].min()),

        int(df["Total_Salary"].max()),

        int(df["Total_Salary"].min())

    )

    rating = st.slider(

        "Minimum Performance Rating",

        float(df["Performance_Rating"].min()),

        float(df["Performance_Rating"].max()),

        float(df["Performance_Rating"].min())

    )

    filtered = df.copy()

    if department != "All":

        filtered = filtered[
            filtered["Department"] == department
        ]

    if gender != "All":

        filtered = filtered[
            filtered["Gender"] == gender
        ]

    filtered = filtered[
        filtered["Experience_Years"] >= experience
    ]

    filtered = filtered[
        filtered["Total_Salary"] >= salary
    ]

    filtered = filtered[
        filtered["Performance_Rating"] >= rating
    ]

    st.success(
        f"Number of Employees: {len(filtered)}"
    )

    st.dataframe(

        filtered,

        use_container_width=True

    )

    st.markdown("---")

    st.subheader("Quick Summary")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Average Salary",

            f"${filtered['Total_Salary'].mean():,.0f}"

            if len(filtered) > 0 else "$0"

        )

    with col2:

        st.metric(

            "Highest Salary",

            f"${filtered['Total_Salary'].max():,.0f}"

            if len(filtered) > 0 else "$0"

        )

    with col3:

        st.metric(

            "Average Rating",

            f"{filtered['Performance_Rating'].mean():.2f}"

            if len(filtered) > 0 else "0"

        )
# =====================================
# CHARTS
# =====================================

elif page == "📈 Charts":

    st.title("📈 Employee Charts")

    chart = st.selectbox(

        "Choose Chart",

        [

            "Average Salary by Department",

            "Salary Histogram",

            "Employee ID vs Salary",

            "Experience vs Salary",

            "Average Salary (Seaborn)",

            "Salary Histogram with KDE"

        ]

    )

    # --------------------------------

    if chart == "Average Salary by Department":

        fig, ax = plt.subplots(figsize=(9,5))

        avg_salary = df.groupby("Department")["Total_Salary"].mean()

        ax.bar(avg_salary.index, avg_salary.values)

        ax.set_title("Average Total Salary by Department")

        ax.set_xlabel("Department")

        ax.set_ylabel("Average Salary")

        st.pyplot(fig)

    # --------------------------------

    elif chart == "Salary Histogram":

        fig, ax = plt.subplots(figsize=(9,5))

        ax.hist(

            df["Total_Salary"],

            bins=15,

            edgecolor="black"

        )

        ax.set_title("Distribution of Total Salary")

        ax.set_xlabel("Total Salary")

        ax.set_ylabel("Frequency")

        st.pyplot(fig)

    # --------------------------------

    elif chart == "Employee ID vs Salary":

        fig, ax = plt.subplots(figsize=(9,5))

        ax.plot(

            df["Employee_ID"].head(20),

            df["Total_Salary"].head(20),

            marker="o"

        )

        ax.set_title("Employee ID vs Total Salary")

        ax.set_xlabel("Employee ID")

        ax.set_ylabel("Total Salary")

        plt.xticks(rotation=45)

        st.pyplot(fig)

    # --------------------------------

    elif chart == "Experience vs Salary":

        fig, ax = plt.subplots(figsize=(9,5))

        sns.scatterplot(

            data=df,

            x="Experience_Years",

            y="Total_Salary",

            hue="Department",

            ax=ax

        )

        ax.set_title("Experience Years vs Total Salary")

        st.pyplot(fig)

    # --------------------------------

    elif chart == "Average Salary (Seaborn)":

        fig, ax = plt.subplots(figsize=(9,5))

        sns.barplot(

            data=df,

            x="Department",

            y="Total_Salary",

            ax=ax

        )

        plt.xticks(rotation=30)

        ax.set_title("Average Salary by Department")

        st.pyplot(fig)

    # --------------------------------

    elif chart == "Salary Histogram with KDE":

        fig, ax = plt.subplots(figsize=(9,5))

        sns.histplot(

            data=df,

            x="Total_Salary",

            kde=True,

            ax=ax

        )

        ax.set_title("Salary Histogram with KDE")

        plt.savefig(

            "employee_salary_histogram.png",

            dpi=300,

            bbox_inches="tight"

        )

        st.pyplot(fig)

        with open(

            "employee_salary_histogram.png",

            "rb"

        ) as file:

            st.download_button(

                "⬇ Download Histogram",

                file,

                file_name="employee_salary_histogram.png",

                mime="image/png"

            )

# =====================================
# ABOUT
# =====================================

elif page == "ℹ️ About":

    st.title("ℹ️ About")

    st.info("""

## Employee Salary Analysis Dashboard

This dashboard was developed using:

✅ Python
✅ NumPy
✅ Pandas
✅ Matplotlib
✅ Seaborn
✅ Streamlit

----------------------------

Dataset:
employee_salary_analysis.csv

----------------------------

### Features

✔ Employee Dataset Preview

✔ Salary Statistics

✔ NumPy Analysis

✔ GroupBy Analysis

✔ Employee Filtering

✔ Interactive Charts

✔ Download Histogram

----------------------------

Developed by **Coding Hub**

© 2026 All Rights Reserved

    """)

    st.markdown("---")

    st.success("Thank you for using Employee Salary Analysis Dashboard 💙")
  
