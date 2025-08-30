import
import pandas as pd
from datetime import datetime
import calendar

st.set_page_config(page_title="Monthly SEO Report Generator", layout="centered")
st.title("📊 Monthly SEO Report Generator")

# --- PROJECT NAME ---
project_name = st.text_input("Project Name", placeholder="Example: Sai Furniture Art")

# --- MONTH SELECTOR ---
months_list = list(calendar.month_name)[1:]
selected_month = st.selectbox("Select Reporting Month (2025)", months_list, index=6)
year = 2025

# Calculate start & end date
month_index = months_list.index(selected_month) + 1
start_date = datetime(year, month_index, 1)
end_day = calendar.monthrange(year, month_index)[1]
end_date = datetime(year, month_index, end_day)
st.info(f"**Selected Period:** {start_date.strftime('%d %B %Y')} to {end_date.strftime('%d %B %Y')} ({end_day} days)")

# Next month
next_month_name = months_list[0] if month_index == 12 else months_list[month_index]

# --- KEYWORD TABLE ---
st.markdown("### Keyword Rankings")
if "rows" not in st.session_state:
    st.session_state.rows = 5

keywords = []
for i in range(st.session_state.rows):
    cols = st.columns(3)
    kw = cols[0].text_input(f"Keyword {i+1}", key=f"kw_{i}", placeholder="Example: Sofa Set Manufacturers")
    curr = cols[1].text_input(f"Current Rank {i+1}", key=f"cr_{i}", placeholder="Example: 2")
    prev = cols[2].text_input(f"Previous Rank {i+1}", key=f"pr_{i}", placeholder="Example: 3")
    keywords.append((kw, curr, prev))

if st.button("➕ Add Row"):
    st.session_state.rows += 1
    st.rerun()

# --- METRICS ---
organic_traffic = st.text_input("Organic Traffic (number only)", placeholder="Example: 1.8K")
new_users = st.text_input("New Users (number only)", placeholder="Example: 1.7K")
event_count = st.text_input("Event Count", placeholder="Example: 12.4K")

cols_bounce = st.columns(2)
prev_bounce = cols_bounce[0].number_input("Previous Bounce Rate (%)", value=0.0, step=0.01, format="%.2f")
curr_bounce = cols_bounce[1].number_input("Current Bounce Rate (%)", value=0.0, step=0.01, format="%.2f")
bounce_text = (
    f"<b>Decrease</b> from {prev_bounce}% to {curr_bounce}%" if prev_bounce > curr_bounce
    else f"<b>Increase</b> from {prev_bounce}% to {curr_bounce}%"
)

backlinks = st.text_input("Backlinks Acquired (number only)", placeholder="Example: 34")
site_speed = st.text_input("Site Speed Optimization (%)", placeholder="Example: 95")
mobile_usability = st.text_input("Mobile Usability (%)", placeholder="Example: 76")

next_month_plan = st.text_area("Next Month Improvement (Each point on a new line)", 
placeholder="""Example:
Improve Internal Linking Structure...
Build High-Quality Backlinks...
Optimize Core Web Vitals...""")

submitted_by = st.text_input("Submitted By", placeholder="Example: Harinder Baweja")

# --- GENERATE ---
if st.button("Generate Report"):
    # Create keyword table with borders
    keyword_df = pd.DataFrame(
        [(kw, curr, prev) for kw, curr, prev in keywords if kw],
        columns=["Keywords", "Current Rank", "Previous Rank"]
    )
    keyword_html = keyword_df.to_html(index=False, border=1, justify="center")

    # Format Next Month Improvement into bullet points
    bullet_points = "".join([f"<li>{point.strip()}</li>" for point in next_month_plan.split("\n") if point.strip()])

    # --- HTML Report with Styling ---
    report_html = f"""
    <div style="font-family:Arial; font-size:14px; line-height:1.6;">
    <p>Dear Sir/Ma'am,</p>
    <p>I hope this message finds you well.</p>

    <p>We are pleased to present you with the monthly SEO working report for <b>{project_name}</b>, 
    covering the period from <b>{start_date.strftime('%d %B %Y')}</b> to <b>{end_date.strftime('%d %B %Y')}</b>. 
    This report outlines the significant progress and strategic initiatives we have undertaken 
    to enhance your online presence and improve your website's performance.</p>

    <h3>Executive Summary:</h3>
    <p>Our focused efforts this month have yielded notable improvements in various key performance indicators, 
    reinforcing our commitment to driving measurable results for your business.</p>

    <h3>Key Highlights:</h3>
    <h4>1. Keyword Rankings:</h4>
    {keyword_html}

    <h4>2. Traffic Metrics:</h4>
    <ul>
        <li><b>Organic Traffic:</b> {organic_traffic} Users</li>
        <li><b>New Users:</b> {new_users} Users</li>
        <li><b>Event Count:</b> {event_count}</li>
        <li><b>Bounce Rate:</b> {bounce_text}</li>
    </ul>

    <h4>3. Off-Page Activities:</h4>
    <ul>
        <li><b>Backlinks Acquired:</b> {backlinks} Backlinks from high-authority domains</li>
    </ul>

    <h4>4. Technical SEO:</h4>
    <ul>
        <li><b>Site Speed Optimization:</b> Reduced load times by {site_speed}%</li>
        <li><b>Mobile Usability:</b> Enhanced mobile experience, achieving a {mobile_usability}% increase in mobile traffic</li>
        <li><b>Indexing Improvements:</b> Ensured prompt and efficient indexing of new and updated pages</li>
    </ul>

    <h3>{next_month_name} Month Planning for Improvement:</h3>
    <ul>
        {bullet_points}
    </ul>

    <p>Attached, you will find a detailed report that includes all relevant metrics, charts, and analyses 
    to provide a clear and comprehensive view of our SEO efforts and their impact on your website's performance.</p>

    <p>We value your continued partnership and are dedicated to achieving exceptional results for <b>{project_name}</b>. 
    Should you have any questions or require further clarification, please do not hesitate to reach out.</p>

    <p>Thank you for your trust and collaboration.</p>
    <p>Best regards,<br><b>{submitted_by}</b></p>
    </div>
    """

    # --- Show output ---
    st.markdown("### ✉️ Final Report Preview")
    st.components.v1.html(report_html, height=800, scrolling=True)

    # --- Download ---
    st.download_button(
        "📥 Download Report (HTML File)",
        data=report_html,
        file_name=f"{project_name}_SEO_Report_{selected_month}_2025.html",
        mime="text/html"
    )
