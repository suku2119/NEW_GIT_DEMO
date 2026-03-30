import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

st.set_page_config(
    page_title="RVS MIS Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Helper Functions
# -----------------------------
def safe_percentage(numerator, denominator):
    if denominator == 0:
        return 0
    return round((numerator / denominator) * 100, 2)

def format_inr(value):
    return f"₹{value:,.2f}"

def traffic_light(value, green_condition, amber_condition):
    if green_condition(value):
        return "🟢 Good"
    elif amber_condition(value):
        return "🟠 Attention"
    return "🔴 Critical"

# -----------------------------
# Title
# -----------------------------
st.title("📊 RVS Land Surveyors MIS Dashboard")
st.caption("KPI + CRM + Accounts + Project Monitoring Dashboard")

# -----------------------------
# Sidebar
# -----------------------------
page = st.sidebar.radio(
    "Select Module",
    ["Dashboard", "KPI", "CRM", "Accounts", "Projects"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

selected_month = st.sidebar.selectbox(
    "Reporting Month",
    ["April", "May", "June", "July", "August", "September",
     "October", "November", "December", "January", "February", "March"]
)

selected_branch = st.sidebar.selectbox(
    "Branch",
    ["All", "Coimbatore", "Salem", "Madurai"]
)

# -----------------------------
# Sample Data
# -----------------------------
crm_data = pd.DataFrame({
    "Lead ID": [101, 102, 103, 104, 105, 106, 107],
    "Date": pd.to_datetime([
        "2026-04-01", "2026-04-03", "2026-04-05",
        "2026-04-07", "2026-04-09", "2026-04-10", "2026-04-12"
    ]),
    "Client Name": [
        "ABC Builders", "Green Infra", "Skyline Homes",
        "Metro Developers", "Sun Power Ltd", "Urban Estates", "Agri Land Corp"
    ],
    "Service": [
        "Topographic Survey", "Boundary Survey", "Drone Survey",
        "LiDAR Survey", "GIS Mapping", "Construction Setting Out", "As-Built Survey"
    ],
    "Branch": [
        "Coimbatore", "Salem", "Madurai",
        "Coimbatore", "Salem", "Madurai", "Coimbatore"
    ],
    "Lead Source": [
        "Website", "Referral", "LinkedIn", "Google", "WhatsApp", "Referral", "Website"
    ],
    "Stage": [
        "New", "Qualified", "Proposal Sent", "Negotiation", "Won", "Lost", "Follow-up"
    ],
    "Lead Value": [50000, 120000, 175000, 300000, 250000, 90000, 130000],
    "Sales Person": ["Kunal", "Arun", "Kunal", "Ravi", "Arun", "Kunal", "Ravi"],
    "Next Follow-up": pd.to_datetime([
        "2026-04-14", "2026-04-15", "2026-04-16",
        "2026-04-17", "2026-04-18", "2026-04-19", "2026-04-20"
    ])
})

accounts_data = pd.DataFrame({
    "Invoice No": ["INV001", "INV002", "INV003", "INV004", "INV005", "INV006"],
    "Client Name": [
        "ABC Builders", "Green Infra", "Skyline Homes",
        "Metro Developers", "Sun Power Ltd", "Urban Estates"
    ],
    "Branch": ["Coimbatore", "Salem", "Madurai", "Coimbatore", "Salem", "Madurai"],
    "Invoice Date": pd.to_datetime([
        "2026-04-02", "2026-04-04", "2026-04-06",
        "2026-04-08", "2026-04-10", "2026-04-12"
    ]),
    "Invoice Amount": [150000, 220000, 180000, 300000, 250000, 100000],
    "Received Amount": [100000, 220000, 50000, 0, 150000, 100000],
    "Payment Status": ["Partial", "Paid", "Partial", "Pending", "Partial", "Paid"],
    "Due Date": pd.to_datetime([
        "2026-04-20", "2026-04-21", "2026-04-22",
        "2026-04-23", "2026-04-24", "2026-04-25"
    ])
})

projects_data = pd.DataFrame({
    "Project ID": ["P001", "P002", "P003", "P004", "P005", "P006"],
    "Project Name": [
        "DMart Site Survey", "Solar Farm Mapping", "Township Layout Survey",
        "Factory GIS Mapping", "Highway LiDAR Scan", "Villa As-Built Survey"
    ],
    "Client Name": [
        "DMart", "Sun Power Ltd", "Urban Estates",
        "ABC Manufacturing", "Infra Roads", "Skyline Homes"
    ],
    "Branch": ["Coimbatore", "Salem", "Madurai", "Coimbatore", "Salem", "Madurai"],
    "Project Manager": ["Manikandan", "Sijo", "Parthiban", "Manikandan", "Sijo", "Parthiban"],
    "Start Date": pd.to_datetime([
        "2026-04-01", "2026-04-03", "2026-04-05",
        "2026-04-07", "2026-04-09", "2026-04-10"
    ]),
    "End Date": pd.to_datetime([
        "2026-04-15", "2026-04-18", "2026-04-20",
        "2026-04-22", "2026-04-25", "2026-04-27"
    ]),
    "Status": ["In Progress", "Completed", "Delayed", "In Progress", "Completed", "Not Started"],
    "Completion %": [60, 100, 40, 75, 100, 0],
    "Project Value": [200000, 500000, 350000, 250000, 600000, 150000]
})

kpi_data = pd.DataFrame({
    "Department": ["Marketing", "Sales", "Operations", "Accounts", "HR", "R&D"],
    "KPI": [
        "Leads Generated", "Lead Conversion %", "On-time Delivery %",
        "Collection Efficiency %", "Attendance %", "Innovation Tasks Completed"
    ],
    "Target": [50, 25, 90, 85, 95, 4],
    "Actual": [42, 18, 82, 78, 92, 3]
})

# -----------------------------
# Apply Branch Filter
# -----------------------------
if selected_branch != "All":
    crm_filtered = crm_data[crm_data["Branch"] == selected_branch].copy()
    accounts_filtered = accounts_data[accounts_data["Branch"] == selected_branch].copy()
    projects_filtered = projects_data[projects_data["Branch"] == selected_branch].copy()
else:
    crm_filtered = crm_data.copy()
    accounts_filtered = accounts_data.copy()
    projects_filtered = projects_data.copy()

# -----------------------------
# Dashboard Page
# -----------------------------
if page == "Dashboard":
    total_leads = len(crm_filtered)
    won_leads = len(crm_filtered[crm_filtered["Stage"] == "Won"])
    total_pipeline = crm_filtered["Lead Value"].sum()
    conversion_rate = safe_percentage(won_leads, total_leads)

    total_invoiced = accounts_filtered["Invoice Amount"].sum()
    total_received = accounts_filtered["Received Amount"].sum()
    outstanding = total_invoiced - total_received
    collection_efficiency = safe_percentage(total_received, total_invoiced)

    active_projects = len(projects_filtered[projects_filtered["Status"].isin(["In Progress", "Delayed", "Not Started"])])
    completed_projects = len(projects_filtered[projects_filtered["Status"] == "Completed"])
    avg_completion = round(projects_filtered["Completion %"].mean(), 2) if not projects_filtered.empty else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Leads", total_leads)
    col2.metric("Won Leads", won_leads)
    col3.metric("Pipeline Value", format_inr(total_pipeline))
    col4.metric("Conversion Rate", f"{conversion_rate}%")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Total Invoiced", format_inr(total_invoiced))
    col6.metric("Total Received", format_inr(total_received))
    col7.metric("Outstanding", format_inr(outstanding))
    col8.metric("Collection Efficiency", f"{collection_efficiency}%")

    st.markdown("---")

    col9, col10, col11 = st.columns(3)
    col9.metric("Active Projects", active_projects)
    col10.metric("Completed Projects", completed_projects)
    col11.metric("Avg Project Completion", f"{avg_completion}%")

    st.markdown("### Lead Stage Overview")
    stage_summary = crm_filtered.groupby("Stage", as_index=False)["Lead ID"].count()
    stage_summary.columns = ["Stage", "Count"]
    st.bar_chart(stage_summary.set_index("Stage"))

    st.markdown("### Accounts Overview")
    accounts_summary = accounts_filtered.groupby("Payment Status", as_index=False)["Invoice Amount"].sum()
    accounts_summary.columns = ["Payment Status", "Invoice Amount"]
    st.bar_chart(accounts_summary.set_index("Payment Status"))

    st.markdown("### Project Completion Overview")
    project_chart = projects_filtered[["Project Name", "Completion %"]].set_index("Project Name")
    st.bar_chart(project_chart)

# -----------------------------
# KPI Page
# -----------------------------
elif page == "KPI":
    st.subheader("📌 KPI Monitoring")

    editable_kpi = st.data_editor(
        kpi_data,
        use_container_width=True,
        num_rows="dynamic"
    )

    editable_kpi["Achievement %"] = np.where(
        editable_kpi["Target"] == 0,
        0,
        round((editable_kpi["Actual"] / editable_kpi["Target"]) * 100, 2)
    )

    def kpi_status(value):
        if value >= 90:
            return "🟢 Good"
        elif value >= 70:
            return "🟠 Attention"
        return "🔴 Critical"

    editable_kpi["Status"] = editable_kpi["Achievement %"].apply(kpi_status)

    st.dataframe(editable_kpi, use_container_width=True)

    st.markdown("### KPI Achievement %")
    chart_data = editable_kpi[["Department", "Achievement %"]].set_index("Department")
    st.bar_chart(chart_data)

# -----------------------------
# CRM Page
# -----------------------------
elif page == "CRM":
    st.subheader("📞 CRM Lead Tracker")

    crm_stage_filter = st.multiselect(
        "Filter by Lead Stage",
        options=sorted(crm_filtered["Stage"].unique()),
        default=sorted(crm_filtered["Stage"].unique())
    )

    crm_source_filter = st.multiselect(
        "Filter by Lead Source",
        options=sorted(crm_filtered["Lead Source"].unique()),
        default=sorted(crm_filtered["Lead Source"].unique())
    )

    crm_view = crm_filtered[
        (crm_filtered["Stage"].isin(crm_stage_filter)) &
        (crm_filtered["Lead Source"].isin(crm_source_filter))
    ].copy()

    edited_crm = st.data_editor(
        crm_view,
        use_container_width=True,
        num_rows="dynamic"
    )

    total_leads = len(edited_crm)
    won_leads = len(edited_crm[edited_crm["Stage"] == "Won"])
    lost_leads = len(edited_crm[edited_crm["Stage"] == "Lost"])
    followup_leads = len(edited_crm[edited_crm["Stage"] == "Follow-up"])
    conversion_rate = safe_percentage(won_leads, total_leads)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Leads", total_leads)
    col2.metric("Won Leads", won_leads)
    col3.metric("Lost Leads", lost_leads)
    col4.metric("Conversion Rate", f"{conversion_rate}%")

    st.markdown("### Lead Value by Stage")
    crm_chart = edited_crm.groupby("Stage", as_index=False)["Lead Value"].sum()
    st.bar_chart(crm_chart.set_index("Stage"))

    st.markdown("### Upcoming Follow-ups")
    today = pd.Timestamp(date.today())
    upcoming = edited_crm[edited_crm["Next Follow-up"] >= today].sort_values("Next Follow-up")
    st.dataframe(upcoming, use_container_width=True)

# -----------------------------
# Accounts Page
# -----------------------------
elif page == "Accounts":
    st.subheader("💰 Accounts Dashboard")

    edited_accounts = st.data_editor(
        accounts_filtered,
        use_container_width=True,
        num_rows="dynamic"
    )

    total_invoiced = edited_accounts["Invoice Amount"].sum()
    total_received = edited_accounts["Received Amount"].sum()
    outstanding = total_invoiced - total_received
    collection_efficiency = safe_percentage(total_received, total_invoiced)

    pending_count = len(edited_accounts[edited_accounts["Payment Status"] == "Pending"])
    partial_count = len(edited_accounts[edited_accounts["Payment Status"] == "Partial"])
    paid_count = len(edited_accounts[edited_accounts["Payment Status"] == "Paid"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Invoiced", format_inr(total_invoiced))
    col2.metric("Total Received", format_inr(total_received))
    col3.metric("Outstanding", format_inr(outstanding))
    col4.metric("Collection Efficiency", f"{collection_efficiency}%")

    col5, col6, col7 = st.columns(3)
    col5.metric("Paid Invoices", paid_count)
    col6.metric("Partial Invoices", partial_count)
    col7.metric("Pending Invoices", pending_count)

    st.markdown("### Invoice Status Summary")
    invoice_status = edited_accounts.groupby("Payment Status", as_index=False)["Invoice Amount"].sum()
    st.bar_chart(invoice_status.set_index("Payment Status"))

    st.markdown("### Outstanding Amount by Client")
    edited_accounts["Outstanding Amount"] = edited_accounts["Invoice Amount"] - edited_accounts["Received Amount"]
    outstanding_client = edited_accounts.groupby("Client Name", as_index=False)["Outstanding Amount"].sum()
    st.bar_chart(outstanding_client.set_index("Client Name"))

    st.markdown("### Collection Health")
    health = traffic_light(
        collection_efficiency,
        green_condition=lambda x: x >= 85,
        amber_condition=lambda x: 70 <= x < 85
    )
    st.info(f"Collection Status: {health}")

# -----------------------------
# Projects Page
# -----------------------------
elif page == "Projects":
    st.subheader("🏗️ Project Monitoring")

    project_status_filter = st.multiselect(
        "Filter by Project Status",
        options=sorted(projects_filtered["Status"].unique()),
        default=sorted(projects_filtered["Status"].unique())
    )

    project_view = projects_filtered[
        projects_filtered["Status"].isin(project_status_filter)
    ].copy()

    edited_projects = st.data_editor(
        project_view,
        use_container_width=True,
        num_rows="dynamic"
    )

    total_projects = len(edited_projects)
    completed_projects = len(edited_projects[edited_projects["Status"] == "Completed"])
    delayed_projects = len(edited_projects[edited_projects["Status"] == "Delayed"])
    avg_completion = round(edited_projects["Completion %"].mean(), 2) if not edited_projects.empty else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Projects", total_projects)
    col2.metric("Completed", completed_projects)
    col3.metric("Delayed", delayed_projects)
    col4.metric("Average Completion", f"{avg_completion}%")

    st.markdown("### Project Completion %")
    project_chart = edited_projects[["Project Name", "Completion %"]].set_index("Project Name")
    st.bar_chart(project_chart)

    st.markdown("### Project Value by Status")
    project_value_status = edited_projects.groupby("Status", as_index=False)["Project Value"].sum()
    st.bar_chart(project_value_status.set_index("Status"))

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("RVS MIS Dashboard | Streamlit prototype for KPI, CRM, Accounts, and Project tracking")