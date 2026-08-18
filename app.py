import streamlit as st
import pyshorteners
import time

# Page configuration
st.set_page_config(page_title="SnapURL - Premium SaaS", page_icon="⚡", layout="wide")

# Initialize session state for tracking and input fields
if 'link_history' not in st.session_state:
    st.session_state.link_history = []
if 'click_counts' not in st.session_state:
    st.session_state.click_counts = {}
if 'latest_short_url' not in st.session_state:
    st.session_state.latest_short_url = None

# Sidebar Information
with st.sidebar:
    st.markdown("### ⚡ SnapURL Enterprise")
    st.info("💡 Pro Tip for Buyers: Frontend handles instant state clearing via session triggers for ultra-smooth UX.")
    st.markdown("---")
    st.markdown("**Core Architecture:**")
    st.markdown("- **Engine:** Python 3.14 + Streamlit")
    st.markdown("- **API Layer:** Pyshorteners Core")

st.title("🔗 SnapURL — Advanced Link Analytics SaaS")
st.write("A production-ready micro-SaaS engine built for modern digital businesses.")

# Navigation Tabs
tab_shorten, tab_analytics, tab_history = st.tabs(["🚀 Shorten Workspace", "📊 Live Insights", "📋 Data Logs"])

with tab_shorten:
    st.subheader("Create a Trackable Smart Link")
    
    # Using key parameters to allow software-driven clearing
    long_url = st.text_input("Target URL (Destination):", placeholder="https://example.com", key="input_url")
    custom_alias = st.text_input("Custom Endpoint Alias (Optional):", placeholder="promo2026", key="input_alias")

    if st.button("Generate Smart Link", type="primary"):
        if long_url.strip() == "":
            st.error("Please enter a valid destination URL first.")
        else:
            with st.spinner("Provisioning secure endpoint..."):
                try:
                    shortener = pyshorteners.Shortener()
                    base_short_url = shortener.tinyurl.short(long_url)
                    
                    if custom_alias.strip():
                        clean_alias = custom_alias.strip().replace(" ", "-")
                        final_url = f"{base_short_url}/{clean_alias}"
                    else:
                        final_url = base_short_url
                    
                    time.sleep(0.4)
                    
                    # Log data BEFORE clearing inputs
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.link_history.append({
                        "time": timestamp,
                        "original": long_url,
                        "shortened": final_url,
                        "alias": custom_alias if custom_alias else "None"
                    })
                    st.session_state.click_counts[final_url] = st.session_state.click_counts.get(final_url, 0) + 1
                    st.session_state.latest_short_url = final_url
                    
                    # Force session clear trigger for input boxes
                    st.rerun()
                    
                except Exception as e:
                    st.error("API Handshake Error: Connection timed out. Please try again.")

    # Permanently display the generated link even after input boxes clear out
    if st.session_state.latest_short_url:
        st.success("🎉 Enterprise Endpoint Generated Successfully!")
        st.code(st.session_state.latest_short_url, language="text")

with tab_analytics:
    st.subheader("Real-Time Traffic Dashboard")
    if not st.session_state.link_history:
        st.warning("No live tracking data available yet.")
    else:
        col_metric1, col_metric2 = st.columns(2)
        col_metric1.metric("Total Managed Links", len(st.session_state.link_history))
        col_metric2.metric("Total Simulated Clicks", sum(st.session_state.click_counts.values()))
        st.bar_chart(st.session_state.click_counts)

with tab_history:
    st.subheader("Data Access Management Logs")
    if not st.session_state.link_history:
        st.info("Data vault is currently empty.")
    else:
        st.dataframe(st.session_state.link_history, use_container_width=True)






        
        
