
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- Page Config ---
st.set_page_config(
    page_title="Competitor Finder",
    page_icon="🔍",
    layout="centered"
)

# --- Optional Background Styling ---
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1532619675605-59f9e86ba24f");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}
[data-testid="stHeader"] {
    background: rgba(255,255,255,0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- Title Section ---
st.title("🔍 Competitor Finder Tool")
st.markdown("Find top competitor websites by entering any domain below. Built using `similarsites.com` data.")

st.divider()

# --- Input Section ---
domain = st.text_input("🌐 Enter Website Domain (e.g., flipkart.com):", "")

# --- Find Competitors Function ---
def find_competitors(domain):
    url = f"https://www.similarsites.com/site/{domain}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    competitors = soup.find_all("a", class_="similar-site-link")
    return [site.text.strip() for site in competitors[:20]]

# --- Button + Output ---
if st.button("Find Competitors"):
    if domain:
        with st.spinner("🔍 Searching for competitors..."):
            try:
                competitors = find_competitors(domain)
                if competitors:
                    st.success(f"✅ {len(competitors)} Competitors found for `{domain}`")
                    df = pd.DataFrame(competitors, columns=["Competitor Websites"])
                    st.dataframe(df, use_container_width=True)

                    # Download button
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="⬇️ Download as CSV",
                        data=csv,
                        file_name=f"{domain}_competitors.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No competitors found. Try a different domain.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a valid domain.")

# --- Footer ---
st.markdown("---")
st.caption("Made with ❤️ using Streamlit · Free data via similarsites.com")
