import streamlit as st
import pandas as pd
import requests
from datetime import date, datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Backend API base URL
API_BASE = "http://localhost:8000"

# Config
st.set_page_config(
    page_title="iCardio Dashboard", 
    layout="wide",
    page_icon="🩺"
)

# API Wrapper Functions
@st.cache_data(ttl=300)
def get_enhanced_metric_data(endpoint):
    """Fetch enhanced metric data with flexible response handling"""
    try:
        r = requests.get(f"{API_BASE}{endpoint}")
        data = r.json()
        
        if isinstance(data, dict):
            if "total_all_time" in data:
                return data
            elif "total_users" in data:
                return {"total_all_time": data["total_users"], "current_week": data.get("current_week", 0)}
            elif "total_studies" in data:
                return {"total_all_time": data["total_studies"], "current_week": data.get("current_week", 0)}
            elif "total_dicoms" in data:
                return {"total_all_time": data["total_dicoms"], "current_week": data.get("current_week", 0)}
            elif "total_frames" in data:
                return {"total_all_time": data["total_frames"], "current_week": data.get("current_week", 0)}
            elif "total_segmentations" in data:
                return {"total_all_time": data["total_segmentations"], "current_week": data.get("current_week", 0)}
            elif "total" in data:
                return {"total_all_time": data["total"], "current_week": data.get("current_week", 0)}
            elif "count" in data:
                return {"total_all_time": data["count"], "current_week": data.get("current_week", 0)}
            elif len(data) == 1:
                key = list(data.keys())[0]
                return {"total_all_time": data[key], "current_week": 0}
            else:
                return data
        elif isinstance(data, (int, float)):
            return {"total_all_time": data, "current_week": 0}
        else:
            st.error(f"Unexpected response format from {endpoint}: {type(data)}")
            return None
            
    except Exception as e:
        st.error(f"Failed to fetch data from {endpoint}: {e}")
        return None

@st.cache_data(ttl=300)
def get_label_counts(group_by, user_filter, view_filter, time_range):
    try:
        params = {
            "group_by": group_by,
            "user_filter": user_filter or [],
            "view_filter": view_filter or [],
        }
        if time_range:
            params["time_range"] = time_range
        r = requests.get(f"{API_BASE}/api/labels/counts", params=params)
        return r.json()
    except Exception as e:
        st.error(f"Failed to fetch label counts: {e}")
        return None

@st.cache_data(ttl=300)
def get_distinct_users():
    try:
        r = requests.get(f"{API_BASE}/api/users/distinct")
        return r.json()
    except Exception as e:
        st.error(f"Failed to fetch users: {e}")
        return {"users": []}

@st.cache_data(ttl=300)
def get_distinct_view_classes():
    try:
        r = requests.get(f"{API_BASE}/api/views/distinct")
        return r.json()
    except Exception as e:
        st.error(f"Failed to fetch view classes: {e}")
        return {"view_classes": []}

@st.cache_data(ttl=300)
def get_review_data(endpoint, params=None):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", params=params or {})
        return r.json()
    except Exception as e:
        st.error(f"Failed to fetch review data from {endpoint}: {e}")
        return None

@st.cache_data(ttl=300)
def get_dicom_filter_options():
    try:
        r = requests.get(f"{API_BASE}/api/dicoms/filter-options")
        return r.json()
    except Exception as e:
        st.error(f"Failed to fetch filter options: {e}")
        return {}

def display_metric(title, data, is_percentage=False):
    """Display a simple metric"""
    if data is None:
        st.metric(title, "N/A")
        return
    
    if isinstance(data, dict):
        total_all_time = data.get("total_all_time", 0)
        current_week = data.get("current_week", 0)
    elif isinstance(data, (int, float)):
        total_all_time = data
        current_week = 0
    else:
        total_all_time = 0
        current_week = 0
    
    if isinstance(total_all_time, str) and "%" in str(total_all_time):
        try:
            total_all_time = float(str(total_all_time).replace("%", ""))
            is_percentage = True
        except (ValueError, TypeError):
            total_all_time = 0
    
    if isinstance(current_week, str):
        try:
            current_week = float(current_week)
        except (ValueError, TypeError):
            current_week = 0
    
    if is_percentage:
        value = f"{total_all_time:.1f}%"
    elif isinstance(total_all_time, (int, float)):
        value = f"{total_all_time:,}" if total_all_time >= 1 else str(total_all_time)
    else:
        value = str(total_all_time)
    
    delta = f"{current_week:,} this week" if current_week > 0 else None
    st.metric(title, value, delta=delta)

def main():
    # Header
    st.title("🩺 iCardio.ai Dashboard")
    
    # Key Metrics
    st.header("📈 Key Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        ("Total Studies", "/api/summary/total-studies"),
        ("Active Users", "/api/metrics/total-users"),
        ("Total DICOMs", "/api/metrics/total-dicoms"),
        ("Total Frames", "/api/metrics/total-frames"),
        ("Segmentations", "/api/metrics/total-segmentations")
    ]
    
    cols = [col1, col2, col3, col4, col5]
    for i, (title, endpoint) in enumerate(metrics):
        with cols[i]:
            data = get_enhanced_metric_data(endpoint)
            display_metric(title, data)

    st.divider()

    # Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Labeler Analytics", 
        "✅ Reviewer Dashboard", 
        "🗺️ Atlas Explorer", 
        "🧠 Dicoms"
    ])

    # Tab 1: Labeling Activity  
    with tab1:
        st.header("📝 Labeling Performance Analytics")
        
        st.subheader("🔍 Filter Controls")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            all_users = get_distinct_users().get("users", [])
            user_filter = st.multiselect("👥 Filter by User", options=all_users)
        
        with col2:
            all_views = get_distinct_view_classes().get("view_classes", [])
            view_filter = st.multiselect("👁️ Filter by View Type", options=all_views)
        
        with col3:
            group_by_option = st.selectbox("📊 Group By", ["User", "Date", "User + Date"])
            group_by_map = {
                "User": "user",
                "Date": "date", 
                "User + Date": "user_and_date"
            }
            group_by_key = group_by_map[group_by_option]
        
        with col4:
            time_range = st.selectbox("⏰ Time Range", [
                "All Time", "Past 1 Week", "Past 2 Weeks", "Past 1 Month", 
                "Past 6 Months", "Past 1 Year", "Past 5 Years"
            ])
            time_range_map = {
                "Past 1 Week": "1w",
                "Past 2 Weeks": "2w", 
                "Past 1 Month": "1m",
                "Past 6 Months": "6m",
                "Past 1 Year": "1y",
                "Past 5 Years": "5y",
                "All Time": None
            }
            time_key = time_range_map[time_range]
        
        result = get_label_counts(
            group_by=group_by_key,
            user_filter=user_filter if user_filter else None,
            view_filter=view_filter if view_filter else None,
            time_range=time_key
        )
        
        if result is None:
            st.error("❌ Unable to load labeling data")
        else:
            df = pd.DataFrame(result.get("data", []))

            if df.empty:
                st.info("📊 No data available for selected filters.")
            else:
                col_left, col_right = st.columns(2)

                with col_left:
                    st.subheader("👥 Labels by User")
                    
                    if group_by_key == "user":
                        fig_bar = px.bar(df, x="group_key", y="label_count")
                    elif group_by_key == "user_and_date":
                        df_grouped = df.groupby("user_name")["label_count"].sum().reset_index()
                        fig_bar = px.bar(df_grouped, x="user_name", y="label_count")
                    else:
                        fig_bar = px.bar(x=["All Users"], y=[df["label_count"].sum()])
                    
                    st.plotly_chart(fig_bar, use_container_width=True)

                with col_right:
                    st.subheader("📈 Labeling Trends")
                    
                    activity_result = get_label_counts(
                        group_by="date",
                        user_filter=user_filter if user_filter else None,
                        view_filter=view_filter if view_filter else None,
                        time_range=time_key
                    )
                    
                    if activity_result:
                        activity_df = pd.DataFrame(activity_result.get("data", []))
                        
                        if not activity_df.empty and 'group_key' in activity_df.columns:
                            try:
                                activity_df['Date'] = pd.to_datetime(activity_df['group_key'])
                                activity_df = activity_df.sort_values('Date')
                                
                                fig_line = px.line(activity_df, x='Date', y='label_count')
                                st.plotly_chart(fig_line, use_container_width=True)
                            except Exception as e:
                                st.info("📊 Unable to parse date data for activity chart.")
                        else:
                            st.info("📊 No activity data available for selected period.")
                    else:
                        st.info("📊 Unable to load activity data.")

                st.subheader("👤 User Performance")
                
                if group_by_key == "user":
                    display_df = df.rename(columns={
                        "group_key": "User", 
                        "label_count": "Total Labels"
                    })
                    st.dataframe(display_df, use_container_width=True)
                else:
                    st.dataframe(df, use_container_width=True)

    # Tab 2: Review Status
    with tab2:
        st.header("✅ Reviewer Dashboard")
        
        period_options = {
            "Past 7 Days": 7,
            "Past 30 Days": 30,
            "Past 90 Days": 90,
            "Past 1 Year": 365,
            "All Time": None
        }
        selected_period_label = st.selectbox("📅 Select Review Period", list(period_options.keys()))
        interval_days = period_options[selected_period_label]

        params = {}
        if interval_days:
            today = datetime.utcnow().date()
            start_date = today - timedelta(days=interval_days)
            params["start_date"] = start_date.isoformat()
            params["end_date"] = today.isoformat()

        # Review Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        pending_vs_completed = get_review_data("/api/review/pending-vs-completed", params)
        
        if pending_vs_completed:
            breakdown = pending_vs_completed.get("breakdown", [])
            
            pending = next((item["value"] for item in breakdown if item["group_key"] == "Pending"), 0)
            completed = next((item["value"] for item in breakdown if item["group_key"] == "Completed"), 0)
            total_reviews = pending + completed
            completion_rate = round((completed / total_reviews) * 100, 1) if total_reviews > 0 else 0
            
            with col1:
                st.metric("Pending Reviews", pending)
            with col2:
                st.metric("Completed Reviews", completed)
            with col3:
                st.metric("Total Reviews", total_reviews)
            with col4:
                st.metric("Completion Rate", f"{completion_rate}%")
        else:
            for col in [col1, col2, col3, col4]:
                with col:
                    st.metric("N/A", "N/A")

        # Review Charts
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📊 Review Status")
            
            data = get_review_data("/api/review/pending-vs-completed", params)
            
            if data:
                breakdown = data.get("breakdown", [])
                
                if breakdown:
                    df = pd.DataFrame(breakdown)
                    fig_pie = px.pie(df, values='value', names='group_key')
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("📊 No review data for the selected period.")
            else:
                st.info("📊 Unable to load review data.")

        with col_right:
            st.subheader("📊 Acceptance Rate by Reviewer")
            
            data = get_review_data("/api/review/acceptance-rate", {"interval_days": interval_days})
            
            if data:
                acceptance_data = data.get("breakdown", [])
                
                if acceptance_data:
                    df = pd.DataFrame(acceptance_data)
                    fig_bar = px.bar(df, x="group_key", y="value", color="sub_group")
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("📊 No acceptance data for the selected period.")
            else:
                st.info("📊 Unable to load acceptance data.")

        # Active Reviewers Table
        st.subheader("👩‍⚕️ Active Reviewers")
        
        reviewers_data = get_review_data("/api/review/active-reviewers", {"activity_interval_days": interval_days})
        
        if reviewers_data:
            reviewers = reviewers_data.get("reviewers", [])
            
            if reviewers:
                df = pd.DataFrame(reviewers)
                df = df.rename(columns={
                    "group_key": "Reviewer", 
                    "value": "Review Count", 
                    "last_review_time": "Last Activity"
                })
                st.dataframe(df, use_container_width=True)
            else:
                st.info("👥 No active reviewers in selected period.")
        else:
            st.info("👥 Unable to load reviewer data.")

        # Reviewer Performance Table
        st.subheader("📊 Reviewer Performance Details")
        
        data = get_review_data("/api/review/acceptance-rate", {"interval_days": interval_days})
        
        if data:
            acceptance_data = data.get("breakdown", [])
            
            if acceptance_data:
                reviewers = {}
                for item in acceptance_data:
                    reviewer = item["group_key"]
                    if reviewer not in reviewers:
                        reviewers[reviewer] = {"Accepted": 0, "Rejected": 0}
                    reviewers[reviewer][item["sub_group"]] = item["value"]
                
                perf_data = []
                for reviewer, stats in reviewers.items():
                    accepted = stats["Accepted"]
                    rejected = stats["Rejected"]
                    total = accepted + rejected
                    acceptance_rate = round((accepted / total) * 100, 1) if total > 0 else 0
                    
                    perf_data.append({
                        "Reviewer": reviewer,
                        "Accepted": accepted,
                        "Rejected": rejected,
                        "Acceptance Rate": f"{acceptance_rate}%",
                        "Total Reviews": total
                    })
                
                perf_df = pd.DataFrame(perf_data)
                st.dataframe(perf_df, use_container_width=True)
            else:
                st.info("📊 No performance data available.")
        else:
            st.info("📊 Unable to load performance data.")

        st.subheader("🧾 Reviewer Metrics Preview")
        st.markdown("""
        - **AI Agreement with Human Reports**: Evaluate how closely AI-generated outputs align with expert-written clinical reports.
        - **Time per Review**: Monitor average review duration to assess workflow efficiency and identify potential bottlenecks.
        - **Per-Class Correction Trends**: Identify which label types (e.g., views, phase, segmentation) are most frequently corrected or rejected by human reviewers.
        """)

    # Tab 3: Atlas
    with tab3:
        st.header("🗺️ Atlas Explorer")

        col1, col2, col3 = st.columns(3)

        with col1:
            data = get_enhanced_metric_data("/api/atlas/dicom-labeled-studies")
            display_metric("Studies with DICOM Labels", data)

        with col2:
            data = get_enhanced_metric_data("/api/atlas/predicted-studies")
            display_metric("Studies with AI Predictions", data)

        with col3:
            data = get_enhanced_metric_data("/api/atlas/fully-labeled-summary")
            percent = data.get("percent_fully_labeled", 0) if data else 0
            display_metric("Fully Labeled Studies", {"total_all_time": percent}, is_percentage=True)

        st.divider()
        st.subheader("📊 Atlas Overview")
        st.markdown("""
        - **Studies with DICOMs labeled**: At least one segmentation, keypoint, or phase label exists for a frame in the study.
        - **Studies with AI Predictions**: At least one view or quality prediction exists for a DICOM in the study.
        - **Fully Labeled Studies**: Must have a perspective label, a segmentation label, and at least one human review on segmentation.
        """)

    # Tab 4: DICOMs
    with tab4:
        st.header("📦 DICOM Metrics Explorer")
        st.write("Use the filters below to query DICOM volume based on metadata.")

        filter_opts = get_dicom_filter_options()
        datasource_options = filter_opts.get("datasource", [])
        manufacturer_options = filter_opts.get("manufacturer", [])
        model_options = filter_opts.get("model", [])
        type_options = filter_opts.get("type", [])

        col1, col2, col3 = st.columns(3)
        with col1:
            datasource_filter = st.multiselect("📡 Datasource", options=datasource_options)
            type_filter = st.multiselect("🧬 Type", options=type_options)
        with col2:
            manufacturer_filter = st.multiselect("🏭 Manufacturer", options=manufacturer_options)
            flagged_filter = st.selectbox("🚩 Flagged", options=[None, True, False], format_func=lambda x: "All" if x is None else str(x))
        with col3:
            model_filter = st.multiselect("🛠️ Model", options=model_options)
            has_media_filter = st.selectbox("🎞️ Has Media", options=[None, True, False], format_func=lambda x: "All" if x is None else str(x))

        params = {
            "datasource": datasource_filter,
            "manufacturer": manufacturer_filter,
            "model": model_filter,
            "type": type_filter,
            "has_media": has_media_filter,
            "flagged": flagged_filter
        }
        clean_params = {k: v for k, v in params.items() if v not in [None, [], ""]}

        if st.button("📊 Run Query"):
            try:
                response = requests.get(f"{API_BASE}/api/dicoms/breakdown", params=clean_params)
                data = response.json().get("data", [])
                df = pd.DataFrame(data)

                if df.empty:
                    st.warning("No results found for the selected filters.")
                else:
                    total = df["count"].sum()
                    st.metric("📦 Total DICOMs (Filtered)", f"{total:,}")

                    st.subheader("📋 Breakdown Table")
                    st.dataframe(df, use_container_width=True)

                    if "date" in df.columns:
                        df["date"] = pd.to_datetime(df["date"])
                        df_sorted = df.groupby("date")["count"].sum().reset_index()
                        st.subheader("📈 DICOMs Over Time")
                        fig = px.line(df_sorted, x="date", y="count", markers=True)
                        st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Error fetching data: {e}")

if __name__ == "__main__":
    main()