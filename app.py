import streamlit as st
import pandas as pd
import requests
from datetime import date, datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 🌐 Backend API base URL
API_BASE = "http://localhost:8000"

# ----------- ⚙️ Config -----------
st.set_page_config(
    page_title="iCardio Dashboard", 
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🩺"
)

# Custom CSS for dark theme and professional styling
st.markdown("""
<style>
    .main {
        background-color: #000000;
        color: #ffffff;
    }
    
    .stApp {
        background-color: #000000;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #374151;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: #4b5563;
        transform: translateY(-2px);
    }
    
    .metric-title {
        color: #9ca3af;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        color: #3b82f6;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    
    .metric-trend {
        color: #10b981;
        font-size: 0.875rem;
        display: flex;
        align-items: center;
        margin-top: 0.5rem;
    }
    
    .metric-trend.negative {
        color: #ef4444;
    }
    
    .metric-trend.neutral {
        color: #6b7280;
    }
    
    .main-header {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    
    .sub-header {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    .chart-container {
        background-color: #1f2937;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #374151;
        margin-bottom: 1rem;
    }
    
    .chart-title {
        color: #ffffff;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    .filter-container {
        background-color: #1f2937;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #374151;
        margin-bottom: 2rem;
    }
    
    .filter-title {
        color: #ffffff;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .stSelectbox > div > div {
        background-color: #374151;
        color: #ffffff;
        border: 1px solid #4b5563;
    }
    
    .stMultiSelect > div > div {
        background-color: #374151;
        color: #ffffff;
        border: 1px solid #4b5563;
    }
    
    /* Enhanced Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #111827;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #374151;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 12px 24px;
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border: 1px solid #374151;
        border-radius: 8px;
        color: #9ca3af;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #374151 0%, #1f2937 100%);
        border-color: #4b5563;
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        border-color: #2563eb !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    .stTabs [aria-selected="true"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #60a5fa, #3b82f6, #1d4ed8);
        border-radius: 4px 4px 0 0;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding: 0;
        background: transparent;
    }
    
    /* Tab Icons Enhancement */
    .stTabs [data-baseweb="tab"] span {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Active Tab Glow Effect */
    .stTabs [aria-selected="true"] {
        position: relative;
    }
    
    .stTabs [aria-selected="true"]::after {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #3b82f6, #1d4ed8, #3b82f6);
        border-radius: 10px;
        z-index: -1;
        opacity: 0.3;
        filter: blur(8px);
    }
    
    /* Tab container enhancement */
    .tab-container {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 1rem;
        border-radius: 16px;
        border: 1px solid #374151;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .tab-header {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ----------- 🔗 API Wrapper Functions -----------
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_enhanced_metric_data(endpoint):
    """
    Fetch enhanced metric data with flexible response handling
    """
    try:
        r = requests.get(f"{API_BASE}{endpoint}")
        data = r.json()
        
        # Handle different response formats
        if isinstance(data, dict):
            # Case 1: Already has the expected format
            if "total_all_time" in data:
                return data
            # Case 2: Has different field names - try to map them
            elif "total_users" in data:
                return {
                    "total_all_time": data["total_users"],
                    "current_week": data.get("current_week", 0)
                }
            elif "total_studies" in data:
                return {
                    "total_all_time": data["total_studies"],
                    "current_week": data.get("current_week", 0)
                }
            elif "total_dicoms" in data:
                return {
                    "total_all_time": data["total_dicoms"],
                    "current_week": data.get("current_week", 0)
                }
            elif "total_frames" in data:
                return {
                    "total_all_time": data["total_frames"],
                    "current_week": data.get("current_week", 0)
                }
            elif "total_segmentations" in data:
                return {
                    "total_all_time": data["total_segmentations"],
                    "current_week": data.get("current_week", 0)
                }
            # Case 3: Has a single numeric field - try common field names
            elif "total" in data:
                return {
                    "total_all_time": data["total"],
                    "current_week": data.get("current_week", 0)
                }
            elif "count" in data:
                return {
                    "total_all_time": data["count"],
                    "current_week": data.get("current_week", 0)
                }
            # Case 4: Has only one key-value pair, assume it's the total
            elif len(data) == 1:
                key = list(data.keys())[0]
                return {
                    "total_all_time": data[key],
                    "current_week": 0
                }
            else:
                # Fallback: return as is and let create_enhanced_metric_card handle it
                return data
        elif isinstance(data, (int, float)):
            # Case 5: Direct numeric response
            return {
                "total_all_time": data,
                "current_week": 0
            }
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

# ----------- 📊 Components -----------
def create_enhanced_metric_card(title, data, color="#3b82f6", is_percentage=False):
    """
    Create metric card with weekly growth indicator
    data should contain: {"total_all_time": int/float, "current_week": int/float}
    is_percentage: if True, formats the total_all_time value as a percentage
    """
    if data is None:
        total = "N/A"
        trend_html = '<div class="metric-trend neutral">📊 Data unavailable</div>'
        color = "#6b7280"
    else:
        # Handle different data formats more robustly
        if isinstance(data, dict):
            total_all_time = data.get("total_all_time", 0)
            current_week = data.get("current_week", 0)
        elif isinstance(data, (int, float)):
            total_all_time = data
            current_week = 0
        else:
            total_all_time = 0
            current_week = 0
        
        # Convert string percentages back to numeric if needed
        if isinstance(total_all_time, str) and "%" in str(total_all_time):
            try:
                total_all_time = float(str(total_all_time).replace("%", ""))
                is_percentage = True
            except (ValueError, TypeError):
                total_all_time = 0
        
        # Convert current_week to numeric if it's a string
        if isinstance(current_week, str):
            try:
                current_week = float(current_week)
            except (ValueError, TypeError):
                current_week = 0
        
        # Format the total value
        if is_percentage:
            total = f"{total_all_time:.1f}%"
        elif isinstance(total_all_time, (int, float)):
            total = f"{total_all_time:,}" if total_all_time >= 1 else str(total_all_time)
        else:
            total = str(total_all_time)
        
        # Calculate trend information (only for non-percentage metrics)
        if not is_percentage and isinstance(total_all_time, (int, float)) and isinstance(current_week, (int, float)):
            if total_all_time > 0 and current_week > 0:
                percentage = round((current_week / total_all_time) * 100, 1)
                trend_class = "metric-trend"
                trend_icon = "📈"
                trend_text = f"↑ {current_week:,} this week ({percentage}%)"
            elif current_week > 0:
                trend_class = "metric-trend"
                trend_icon = "📈"
                trend_text = f"↑ {current_week:,} this week"
            else:
                trend_class = "metric-trend neutral"
                trend_icon = "📊"
                trend_text = "No activity this week"
        else:
            # For percentages or when we can't calculate trends
            trend_class = "metric-trend neutral"
            trend_icon = "📊"
            trend_text = "Current period metric"
        
        trend_html = f'<div class="{trend_class}">{trend_icon} {trend_text}</div>'
    
    card_html = f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value" style="color: {color};">{total}</div>
        {trend_html}
    </div>
    """
    return card_html

# ----------- 🎯 Main App -----------
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        🩺 iCardio.ai Dashboard
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics - Enhanced with Weekly Growth
    st.markdown("### 📈 Key Metrics")
    
    # Metric Cards with Enhanced Data
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Define metrics with their endpoints and colors
    metrics = [
        ("Total Studies", "/api/summary/total-studies", "#3b82f6"),
        ("Active Users", "/api/metrics/total-users", "#10b981"),
        ("Total DICOMs", "/api/metrics/total-dicoms", "#8b5cf6"),
        ("Total Frames", "/api/metrics/total-frames", "#ef4444"),
        ("Segmentations", "/api/metrics/total-segmentations", "#f59e0b")
    ]
    
    cols = [col1, col2, col3, col4, col5]
    for i, (title, endpoint, color) in enumerate(metrics):
        with cols[i]:
            data = get_enhanced_metric_data(endpoint)
            st.markdown(create_enhanced_metric_card(title, data, color=color), unsafe_allow_html=True)

    st.markdown("---")

    # Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Labeler Analytics", 
        "✅ Reviewer Dashboard", 
        "🗺️ Atlas Explorer", 
        "🧠 Encephalon AI"
    ])

    # Tab 1: Labeling Activity  
    with tab1:
        st.markdown("### 📝 Labeling Performance Analytics")
        
        # Labeler-specific filters
        st.markdown('<div class="filter-title">🔍 Filter Controls</div>', unsafe_allow_html=True)
        
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
        
        with filter_col1:
            all_users = get_distinct_users().get("users", [])
            user_filter = st.multiselect("👥 Filter by User", options=all_users)
        
        with filter_col2:
            all_views = get_distinct_view_classes().get("view_classes", [])
            view_filter = st.multiselect("👁️ Filter by View Type", options=all_views)
        
        with filter_col3:
            group_by_option = st.selectbox("📊 Group By", ["User", "Date", "User + Date"])
            group_by_map = {
                "User": "user",
                "Date": "date", 
                "User + Date": "user_and_date"
            }
            group_by_key = group_by_map[group_by_option]
        
        with filter_col4:
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
                    # Labels by User Chart
                    st.markdown('<h3 class="chart-title">👥 Labels by User</h3>', unsafe_allow_html=True)
                    
                    if group_by_key == "user":
                        fig_bar = px.bar(df, x="group_key", y="label_count",
                                       color_discrete_sequence=['#3b82f6'])
                    elif group_by_key == "user_and_date":
                        df_grouped = df.groupby("user_name")["label_count"].sum().reset_index()
                        fig_bar = px.bar(df_grouped, x="user_name", y="label_count",
                                       color_discrete_sequence=['#3b82f6'])
                    else:
                        fig_bar = px.bar(x=["All Users"], y=[df["label_count"].sum()],
                                       color_discrete_sequence=['#3b82f6'])
                    
                    fig_bar.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white',
                        xaxis=dict(gridcolor='#374151'),
                        yaxis=dict(gridcolor='#374151')
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)

                with col_right:
                    # Daily Activity Line Chart
                    st.markdown('<h3 class="chart-title">📈 Labeling Trends</h3>', unsafe_allow_html=True)
                    
                    # Get time series data by fetching with date grouping
                    activity_result = get_label_counts(
                        group_by="date",
                        user_filter=user_filter if user_filter else None,
                        view_filter=view_filter if view_filter else None,
                        time_range=time_key
                    )
                    
                    if activity_result:
                        activity_df = pd.DataFrame(activity_result.get("data", []))
                        
                        if not activity_df.empty and 'group_key' in activity_df.columns:
                            # Convert group_key to datetime if it's a date string
                            try:
                                activity_df['Date'] = pd.to_datetime(activity_df['group_key'])
                                activity_df = activity_df.sort_values('Date')
                                
                                fig_line = px.line(activity_df, x='Date', y='label_count',
                                                 color_discrete_sequence=['#10b981'])
                                fig_line.update_layout(
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    font_color='white',
                                    xaxis=dict(gridcolor='#374151'),
                                    yaxis=dict(gridcolor='#374151')
                                )
                                fig_line.update_traces(line=dict(width=3), marker=dict(size=8))
                                st.plotly_chart(fig_line, use_container_width=True)
                            except Exception as e:
                                st.info("📊 Unable to parse date data for activity chart.")
                        else:
                            st.info("📊 No activity data available for selected period.")
                    else:
                        st.info("📊 Unable to load activity data.")

                # User Performance Table
                st.markdown('<h3 class="chart-title">👤 User Performance</h3>', unsafe_allow_html=True)
                
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
        st.markdown("### ✅ Reviewer Dashboard")
        
        # Period Selection
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

        # Review Metrics Cards
        col1, col2, col3, col4 = st.columns(4)
        
        pending_vs_completed = get_review_data("/api/review/pending-vs-completed", params)
        
        if pending_vs_completed:
            breakdown = pending_vs_completed.get("breakdown", [])
            
            pending = next((item["value"] for item in breakdown if item["group_key"] == "Pending"), 0)
            completed = next((item["value"] for item in breakdown if item["group_key"] == "Completed"), 0)
            total_reviews = pending + completed
            completion_rate = round((completed / total_reviews) * 100, 1) if total_reviews > 0 else 0
            
            with col1:
                st.markdown(create_enhanced_metric_card("Pending Reviews", {"total_all_time": pending, "current_week": 0}, color="#f59e0b"), unsafe_allow_html=True)
            with col2:
                st.markdown(create_enhanced_metric_card("Completed Reviews", {"total_all_time": completed, "current_week": 0}, color="#10b981"), unsafe_allow_html=True)
            with col3:
                st.markdown(create_enhanced_metric_card("Total Reviews", {"total_all_time": total_reviews, "current_week": 0}, color="#3b82f6"), unsafe_allow_html=True)
            with col4:
                st.markdown(create_enhanced_metric_card("Completion Rate", {"total_all_time": completion_rate, "current_week": 0}, color="#8b5cf6", is_percentage=True), unsafe_allow_html=True)
        else:
            for col in [col1, col2, col3, col4]:
                with col:
                    st.markdown(create_enhanced_metric_card("N/A", None), unsafe_allow_html=True)

        # Review Charts
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<h3 class="chart-title">📊 Review Status</h3>', unsafe_allow_html=True)
            
            data = get_review_data("/api/review/pending-vs-completed", params)
            
            if data:
                breakdown = data.get("breakdown", [])
                
                if breakdown:
                    df = pd.DataFrame(breakdown)
                    fig_pie = px.pie(df, values='value', names='group_key',
                                   color_discrete_sequence=['#10b981', '#f59e0b'])
                    fig_pie.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("📊 No review data for the selected period.")
            else:
                st.info("📊 Unable to load review data.")

        with col_right:
            st.markdown('<h3 class="chart-title">📊 Acceptance Rate by Reviewer</h3>', unsafe_allow_html=True)
            
            data = get_review_data("/api/review/acceptance-rate", {"interval_days": interval_days})
            
            if data:
                acceptance_data = data.get("breakdown", [])
                
                if acceptance_data:
                    df = pd.DataFrame(acceptance_data)
                    fig_bar = px.bar(df, x="group_key", y="value", color="sub_group",
                                   color_discrete_map={"Accepted": "#10b981", "Rejected": "#ef4444"})
                    fig_bar.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white',
                        xaxis=dict(gridcolor='#374151'),
                        yaxis=dict(gridcolor='#374151')
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("📊 No acceptance data for the selected period.")
            else:
                st.info("📊 Unable to load acceptance data.")

        # Active Reviewers Table
        st.markdown('<h3 class="chart-title">👩‍⚕️ Active Reviewers</h3>', unsafe_allow_html=True)
        
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
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">📊 Reviewer Performance Details</h3>', unsafe_allow_html=True)
        
        data = get_review_data("/api/review/acceptance-rate", {"interval_days": interval_days})
        
        if data:
            acceptance_data = data.get("breakdown", [])
            
            if acceptance_data:
                # Process data for performance table
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
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Tab 2: Reviewer Dashboard
    with tab2:
        st.markdown("### ✅ Reviewer Dashboard")

        st.markdown("""
        #### 🧾 Reviewer Metrics Preview
        - **AI Agreement with Human Reports**  
        Evaluate how closely AI-generated outputs align with expert-written clinical reports.

        - **Time per Review**  
        Monitor average review duration to assess workflow efficiency and identify potential bottlenecks.

        - **Per-Class Correction Trends**  
        Identify which label types (e.g., views, phase, segmentation) are most frequently corrected or rejected by human reviewers.
        """, unsafe_allow_html=True)


    
    # Tab 3: Atlas
    with tab3:
        st.markdown("### 🗺️ Atlas Explorer")

        # Metric Cards
        col1, col2, col3 = st.columns(3)

        with col1:
            data = get_enhanced_metric_data("/api/atlas/dicom-labeled-studies")
            st.markdown(create_enhanced_metric_card("Studies with DICOM Labels", data, color="#3b82f6"), unsafe_allow_html=True)

        with col2:
            data = get_enhanced_metric_data("/api/atlas/predicted-studies")
            st.markdown(create_enhanced_metric_card("Studies with AI Predictions", data, color="#8b5cf6"), unsafe_allow_html=True)

        with col3:
            data = get_enhanced_metric_data("/api/atlas/fully-labeled-summary")
            percent = data.get("percent_fully_labeled", 0) if data else 0
            st.markdown(create_enhanced_metric_card("Fully Labeled Studies", {"total_all_time": percent}, color="#10b981", is_percentage=True), unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📊 Atlas Overview")
        st.markdown(
            """
            - **Studies with DICOMs labeled**: At least one segmentation, keypoint, or phase label exists for a frame in the study.
            - **Studies with AI Predictions**: At least one view or quality prediction exists for a DICOM in the study.
            - **Fully Labeled Studies**: Must have a perspective label, a segmentation label, and at least one human review on segmentation.
            """,
            unsafe_allow_html=True
        )


    # Tab 4: Encephalon
    with tab4:
        st.markdown("### 🧠 Encephalon Dashboard")

        st.markdown("""
        #### 🧪 Encephalon Metrics Preview
        - **Number of DICOMs processed**
        - **Number of measurements taken**
        - **Number of reports created**
        - **Success/failure rates of AI pipelines**
        - **Which AI models ran (segmentation, pathology, diameter), and how long each took**
        - **% of studies returning complete measurements (e.g., LV diameter, EF)**
        """, unsafe_allow_html=True)

        st.info("Note: This is a demo preview. Actual charts and data will be integrated soon.")

if __name__ == "__main__":
    main()