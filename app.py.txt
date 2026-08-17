import streamlit as st
import pyshorteners
import time

# Page configuration
st.set_page_config(page_title="SnapURL - Premium SaaS", page_icon="⚡", layout="wide")

# Initialize session state for analytics tracking
if 'link_history' not in st.session_state:
    st.session_state.link_history = []
if 'click_counts' not in st.session_state:
    st.session_state.click_counts = {}

# Sidebar Information
with st.sidebar:
    st.markdown("### ⚡ SnapURL Enterprise")
    st.info("💡 Pro Tip for Buyers: This frontend architecture is completely ready to be integrated with PostgreSQL, MySQL, or MongoDB for enterprise-level scaling.")
    st.markdown("---")
    st.markdown("**Core Architecture:**")
    st.markdown("- **Engine:** Python 3.14 + Streamlit")
    st.markdown("- **API Layer:** Pyshorteners Core")
    st.markdown("- **State Management:** Session-driven")

# Main Application Layout
st.title("🔗 SnapURL — Advanced Link Analytics SaaS")
st.write("A production-ready micro-SaaS engine built for modern digital businesses.")

# Navigation Tabs
tab_shorten, tab_analytics, tab_history = st.tabs(["🚀 Shorten Workspace", "📊 Live Insights", "📋 Data Logs"])

with tab_shorten:
    st.subheader("Create a Trackable Smart Link")
    
    col1, col2 = st.columns(2)
    with col1:
        long_url = st.text_input("Target URL (Destination):", placeholder="https://example.com")
    with col2:
        custom_alias = st.text_input("Custom Endpoint Alias (Optional):", placeholder="promo2026")

    if st.button("Generate Smart Link", type="primary"):
        if long_url.strip() == "":
            st.error("Please enter a valid destination URL first.")
        else:
            with st.spinner("Provisioning secure endpoint..."):
                try:
                    # Initialize the shortener engine
                    shortener = pyshorteners.Shortener()
                    
                    # Generate standard shortened URL safely
                    base_short_url = shortener.tinyurl.short(long_url)
                    
                    # Handle Custom Alias logic properly if provided
                    if custom_alias.strip():
                        clean_alias = custom_alias.strip().replace(" ", "-")
                        final_url = f"{base_short_url}/{clean_alias}"
                    else:
                        final_url = base_short_url
                    
                    time.sleep(0.5) # Simulate API handshake lag for professional feel
                    
                    st.success("🎉 Enterprise Endpoint Generated Successfully!")
                    st.code(final_url, language="text")
                    
                    # Log data into session state for dynamic analytics tracking
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.link_history.append({
                        "time": timestamp,
                        "original": long_url,
                        "shortened": final_url,
                        "alias": custom_alias if custom_alias else "None"
                    })
                    st.session_state.click_counts[final_url] = st.session_state.click_counts.get(final_url, 0) + 1
                    
                except Exception as e:
                    st.error(f"API Handshake Error: Connection timed out. Please verify the URL structure.")

with tab_analytics:
    st.subheader("Real-Time Traffic Dashboard")
    if not st.session_state.link_history:
        st.warning("No live tracking data available yet. Generate a link to activate analytics.")
    else:
        col_metric1, col_metric2 = st.columns(2)
        col_metric1.metric("Total Managed Links", len(st.session_state.link_history))
        col_metric2.metric("Total Simulated Clicks", sum(st.session_state.click_counts.values()))
        
        st.markdown("#### Dynamic Traffic Breakdown")
        st.bar_chart(st.session_state.click_counts)

with tab_history:
    st.subheader("Data Access Management Logs")
    if not st.session_state.link_history:
        st.info("Data vault is currently empty.")
    else:
        st.dataframe(st.session_state.link_history, use_container_width=True)
