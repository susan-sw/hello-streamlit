# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit.hello.utils import show_code


def issue_analysis_demo() -> None:
    # Load data
    file_path = '../data/MON_WEEK.csv'
    data = pd.read_csv(file_path)

    # Clean and preprocess data
    data.columns = ["Issue key", "Summary", "Priority","Custom field (Bundle Version)", "Custom field (Linked LSTI/DVTI)"]
    data.rename(columns={"Issue key":"MON.ID",
                         "Summary":"MON.summary",
                         "Priority":"MON.priority",
                         "Custom field (Bundle Version)":"bundle",
                         "Custom field (Linked LSTI/DVTI)":"LSTI.ID"})
    data["Priority"] = data["Priority"].str.strip()  # Remove extra spaces
    data["Linked LSTI"] = data["Linked LSTI"].fillna("Unlinked")  # Fill NaN values

    # Set page title and sidebar
    st.title("Moment Analysis Dashboard")
    st.sidebar.header("Analysis Options")
    option = st.sidebar.selectbox("Select Analysis Type", ["MON Priority Distribution", "Linked LSTI Distribution"])

    if option == "Priority Distribution":
        st.header("Priority Distribution")

        # Group by priority and count
        priority_counts = data["MON.priority"].value_counts()

        # Plot pie chart
        fig, ax = plt.subplots()
        ax.pie(priority_counts, labels=priority_counts.index, autopct="%.1f%%", startangle=90,
               colors=plt.cm.Pastel1.colors)
        ax.set_title("Priority Distribution")
        st.pyplot(fig)

        # Show details for selected priority
        selected_priority = st.selectbox("Select Priority to View Details", priority_counts.index)
        filtered_data = data[data["Priority"] == selected_priority]
        st.write(filtered_data)

    elif option == "Linked LSTI Distribution":
        st.header("Linked LSTI Distribution")

        # Group by LSTI and count
        lsti_counts = data["LSTI.ID"].value_counts()

        # Plot bar chart
        fig, ax = plt.subplots()
        ax.bar(lsti_counts.index, lsti_counts.values, color=plt.cm.Pastel1.colors)
        ax.set_title("Linked LSTI Distribution")
        ax.set_xlabel("LSTI")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

        # Show details for selected LSTI
        selected_lsti = st.selectbox("Select Linked LSTI to View Details", lsti_counts.index)
        filtered_data = data[data["LSTI"] == selected_lsti]
        st.write(filtered_data)


st.set_page_config(page_title="Issue Analysis Demo", page_icon="📊")
st.markdown("# Issue Analysis Demo")
st.sidebar.header("Issue Analysis")
st.write(
    """This app provides a dashboard for analyzing issue data.
It displays distributions by priority and linked LSTI with interactive details."""
)

issue_analysis_demo()

show_code(issue_analysis_demo)
