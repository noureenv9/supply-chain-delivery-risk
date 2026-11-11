import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Late-Delivery Risk | Supply Chain Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Professional navy supply-chain theme ────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

:root {
    --navy-900: #0A1628;
    --navy-800: #0F2744;
    --navy-700: #163A5F;
    --navy-600: #1E4D7B;
    --navy-500: #2A6AA5;
    --accent:   #3B82F6;
    --accent-soft: #60A5FA;
    --surface:  #F4F7FB;
    --card:     #FFFFFF;
    --border:   #D6E0EF;
    --text:     #0F172A;
    --muted:    #64748B;
    --success:  #059669;
    --warning:  #D97706;
    --danger:   #DC2626;
}

html, body, [class*="css"] {
    font-family: 'Inter', 'IBM Plex Sans', system-ui, sans-serif;
}

/* Page background */
.stApp {
    background: linear-gradient(160deg, #0A1628 0%, #0F2744 35%, #163A5F 100%);
    background-attachment: fixed;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

/* Main content container */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1100px;
}

/* Hero header */
.hero {
    background: linear-gradient(135deg, rgba(15,39,68,0.95) 0%, rgba(22,58,95,0.9) 100%);
    border: 1px solid rgba(96,165,250,0.25);
    border-radius: 16px;
    padding: 1.75rem 2rem 1.5rem;
    margin-bottom: 1.75rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
}
.hero-badge {
    display: inline-block;
    background: rgba(59,130,246,0.15);
    color: #93C5FD;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.3rem 0.7rem;
    border-radius: 999px;
    border: 1px solid rgba(96,165,250,0.35);
    margin-bottom: 0.75rem;
}
.hero h1 {
    color: #F8FAFC !important;
    font-size: 1.85rem !important;
    font-weight: 700 !important;
    margin: 0 0 0.4rem 0 !important;
    letter-spacing: -0.02em;
    line-height: 1.25;
}
.hero p {
    color: #94A3B8 !important;
    font-size: 0.98rem !important;
    margin: 0 !important;
    line-height: 1.5;
}

/* Section cards */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.5rem 1.2rem;
    box-shadow: 0 4px 20px rgba(10,22,40,0.08);
    margin-bottom: 1.25rem;
}
.card-title {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--navy-600);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.45rem;
}
.card-title::before {
    content: "";
    width: 4px;
    height: 14px;
    background: var(--accent);
    border-radius: 2px;
}

/* Form labels */
label, .stSelectbox label, .stNumberInput label, .stSlider label {
    color: var(--navy-800) !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
}

/* Inputs */
div[data-baseweb="select"] > div,
.stNumberInput input {
    border-radius: 8px !important;
}

/* Slider – navy theme */
div[data-testid="stSlider"] {
    padding-top: 0.35rem;
    padding-bottom: 0.5rem;
}
div[data-testid="stSlider"] label,
div[data-testid="stSlider"] label p,
div[data-testid="stSlider"] [data-testid="stTickBarMin"],
div[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    color: #E2E8F0 !important;
}
div[data-testid="stSlider"] [data-baseweb="slider"] {
    margin-top: 0.4rem;
}
/* Unfilled slider track */
div[data-testid="stSlider"] [data-baseweb="slider"] [role="presentation"] {
    background-color: #35526E !important;
}
div[data-testid="stSlider"] div[role="slider"] {
    background-color: #E0F2FE !important;
    border: 3px solid #38BDF8 !important;
    box-shadow: 0 0 0 5px rgba(56, 189, 248, 0.28),
                0 0 16px rgba(56, 189, 248, 0.65) !important;
}
/* Filled track portion and tick marks */
div[data-testid="stSlider"] [data-baseweb="slider"] [role="presentation"] div {
    background-color: #38BDF8 !important;
}
div[data-testid="stSlider"] [data-testid="stTickBar"] {
    background: transparent !important;
}
/* Slider value label */
div[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #F8FAFC !important;
    font-weight: 600 !important;
    background: #163A5F !important;
    border: 1px solid #38BDF8 !important;
    border-radius: 6px !important;
    padding: 2px 8px !important;
}
/* Min / max labels */
div[data-testid="stSlider"] [data-testid="stTickBarMin"],
div[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    color: #CBD5E1 !important;
    font-size: 0.8rem !important;
}

/* Primary button */
.stButton > button {
    background: linear-gradient(135deg, #1E4D7B 0%, #2A6AA5 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.5rem !important;
    width: 100%;
    letter-spacing: 0.01em;
    box-shadow: 0 4px 14px rgba(30,77,123,0.35);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(30,77,123,0.45) !important;
}
.stButton > button:active {
    transform: translateY(0);
}

/* Metric styling */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0F2744 0%, #163A5F 100%);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    border: 1px solid rgba(96,165,250,0.3);
}
[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}
[data-testid="stMetricValue"] {
    color: #F1F5F9 !important;
    font-size: 2.1rem !important;
    font-weight: 700 !important;
}

/* Alert boxes */
.stAlert {
    border-radius: 10px !important;
    border-left-width: 5px !important;
}

/* Expander */
.streamlit-expanderHeader {
    font-weight: 600 !important;
    color: #F8FAFC !important;
    background: var(--navy-700) !important;
    border-radius: 10px !important;
    padding: 0.9rem 1rem !important;
    min-height: 3.25rem;
}
.streamlit-expanderContent {
    background: var(--navy-800) !important;
    color: #E2E8F0 !important;
    border: 1px solid rgba(96,165,250,0.3);
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 0.75rem 1rem !important;
}
.streamlit-expanderContent p,
.streamlit-expanderContent strong,
[data-testid="stExpander"] [data-testid="stExpanderDetails"] p,
[data-testid="stExpander"] [data-testid="stExpanderDetails"] strong {
    color: #E2E8F0 !important;
}
[data-testid="stExpander"] {
    width: 100%;
}
[data-testid="stExpander"] details > summary {
    color: #F8FAFC !important;
    background: var(--navy-700) !important;
    border: 1px solid rgba(96,165,250,0.45) !important;
    border-radius: 10px !important;
    padding: 0.9rem 1rem !important;
    min-height: 3.25rem;
    font-size: 1rem !important;
    font-weight: 600 !important;
}
[data-testid="stExpander"] details > summary p,
[data-testid="stExpander"] details > summary span {
    color: #F8FAFC !important;
}
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: var(--navy-800) !important;
    border: 1px solid rgba(96,165,250,0.45) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px;
    padding: 1rem 1.25rem !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
}

/* Footer note */
.footer-note {
    text-align: center;
    color: #64748B;
    font-size: 0.8rem;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(148,163,184,0.25);
}

/* Risk result card */
.risk-card {
    border-radius: 14px;
    padding: 1.35rem 1.5rem;
    margin: 1rem 0 0.75rem;
    border: 1px solid;
}
.risk-card.high {
    background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
    border-color: #FECACA;
}
.risk-card.med {
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
    border-color: #FDE68A;
}
.risk-card.low {
    background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
    border-color: #A7F3D0;
}
.risk-title {
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 0.35rem;
}
.risk-card.high .risk-title { color: #991B1B; }
.risk-card.med  .risk-title { color: #92400E; }
.risk-card.low  .risk-title { color: #065F46; }
.risk-body {
    font-size: 0.92rem;
    color: #334155;
    line-height: 1.5;
}
.info-chip {
    display: inline-block;
    background: #EFF6FF;
    color: #1E40AF;
    font-size: 0.85rem;
    padding: 0.45rem 0.85rem;
    border-radius: 8px;
    border: 1px solid #BFDBFE;
    margin-top: 0.6rem;
}
.upgrade-box {
    margin-top: 0.85rem;
    padding: 0.9rem 1.1rem;
    border-radius: 10px;
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border: 1px solid #93C5FD;
    color: #1E3A5F;
    font-size: 0.9rem;
    line-height: 1.45;
}
.upgrade-box strong {
    color: #1E40AF;
}
.upgrade-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #2563EB;
    margin-bottom: 0.3rem;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_bundle():
    return joblib.load("model.joblib")


b = load_bundle()
products, countries, opts = b["products"], b["countries"], b["options"]

PROMISED = {"Same Day": 0, "First Class": 1, "Second Class": 2, "Standard Class": 4}
TYPICAL = {"Same Day": 0.49, "First Class": 2.0, "Second Class": 3.99, "Standard Class": 3.99}
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def format_delivery_note(mode: str) -> str:
    """Human-readable promised vs typical delivery for the info chip."""
    promised = PROMISED[mode]
    typical = TYPICAL[mode]

    if mode == "Same Day":
        promised_txt = "promised same day"
        typical_txt = "typically arrives within ~12 hours"
    else:
        day_word = "day" if promised == 1 else "days"
        promised_txt = f"promised {promised} {day_word}"
        # round to 1 decimal and drop trailing .0
        t = f"{typical:.1f}".rstrip("0").rstrip(".")
        typical_txt = f"typically delivered in ~{t} days"

    return f"{mode}: {promised_txt}, {typical_txt}"


def upgrade_suggestion(mode: str, p: float) -> str | None:
    """Recommend a shipping-mode upgrade when risk is high."""
    if p < 0.50:
        return None

    if mode == "Standard Class":
        return (
            "Consider upgrading from <strong>Standard Class → Second Class</strong> "
            "(or <strong>First Class</strong> for the tightest window). "
            "Warn the customer either way and set a realistic delivery expectation."
        )
    if mode == "Second Class":
        return (
            "Consider upgrading from <strong>Second Class → First Class</strong>. "
            "Also warn the customer — First Class is faster but historically often misses its 1-day promise."
        )
    if mode == "First Class":
        return (
            "Already on <strong>First Class</strong>. Focus on warning the customer and quoting a "
            "longer window — this mode is frequently late relative to its 1-day promise."
        )
    # Same Day
    return (
        "Already on <strong>Same Day</strong>. Prioritize an immediate customer warning and a "
        "clear backup delivery window if the same-day slot cannot be met."
    )

# ── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">Supply Chain Intelligence</div>
    <h1>📦 Late-Delivery Risk Checker</h1>
    <p>Assess the probability of late delivery <strong>before the order ships</strong> — using only information available at order placement.</p>
</div>
""", unsafe_allow_html=True)

# ── Input form ──────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">Order Details</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="large")
with c1:
    product = st.selectbox("Product", list(products.index))
    country = st.selectbox("Destination country", list(countries.index))
    quantity = st.number_input("Quantity", min_value=1, max_value=20, value=1)
    segment = st.selectbox("Customer segment", opts["Customer Segment"])
with c2:
    mode = st.selectbox(
        "Shipping mode",
        opts["Shipping Mode"],
        index=opts["Shipping Mode"].index("Standard Class"),
    )
    pay = st.selectbox("Payment type", opts["Type"])
    month = st.selectbox("Order month", list(range(1, 13)))
    weekday = st.selectbox("Order weekday", DAYS)
    hour = st.slider("Order hour (0–23)", 0, 23, 12)

st.markdown("</div>", unsafe_allow_html=True)

# ── Action ──────────────────────────────────────────────────────────────────
check = st.button("Check late-delivery risk", type="primary", use_container_width=True)

if check:
    try:
        row = dict(b["defaults"])
        row.update(products.loc[product].to_dict())
        row.update(countries.loc[country].to_dict())
        row.update({
            "Product Name": product,
            "Order Country": country,
            "Order Item Quantity": quantity,
            "Customer Segment": segment,
            "Shipping Mode": mode,
            "Type": pay,
            "order_month": month,
            "order_weekday": DAYS.index(weekday),
            "order_hour": hour,
        })
        X_new = pd.DataFrame([row])[b["columns"]]
        p = float(b["model"].predict_proba(X_new)[0, 1])

        st.markdown('<div class="card"><div class="card-title">Risk Assessment</div>', unsafe_allow_html=True)

        m1, m2 = st.columns([1, 1.4])
        with m1:
            st.metric("Estimated probability of late delivery", f"{p:.0%}")

        with m2:
            if p >= 0.80:
                st.markdown("""
                <div class="risk-card high">
                    <div class="risk-title">Very high risk</div>
                    <div class="risk-body">About <strong>94%</strong> of similar past orders were late.
                    Warn the customer and set a longer delivery window.</div>
                </div>
                """, unsafe_allow_html=True)
            elif p >= 0.50:
                st.markdown("""
                <div class="risk-card med">
                    <div class="risk-title">High risk</div>
                    <div class="risk-body">About <strong>75%</strong> of similar past orders were late.
                    Consider warning the customer and adjusting expectations.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="risk-card low">
                    <div class="risk-title">Lower risk</div>
                    <div class="risk-body">Still not risk-free — about <strong>37%</strong> of similar past
                    orders were late. Monitor and communicate proactively.</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(
            f'<div class="info-chip">{format_delivery_note(mode)}</div>',
            unsafe_allow_html=True,
        )

        suggestion = upgrade_suggestion(mode, p)
        if suggestion:
            st.markdown(
                f'<div class="upgrade-box">'
                f'<div class="upgrade-label">Recommended action</div>'
                f'{suggestion}'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Could not compute a prediction: {e}")

# ── Methodology ─────────────────────────────────────────────────────────────
with st.expander("How this works & model limits"):
    st.markdown("""
A **gradient boosting** model trained on ~145,000 historical order rows, using only features
known at the moment the order is placed. Risk percentages reflect the share of test-set orders
in each tier that were actually late.

**Data source:** DataCo Smart Supply Chain (Kaggle).  
**Important limits:** The dataset comes from a single company and contains no weather, carrier,
or distance information — so even “lower-risk” orders are late fairly often in reality.
""")

st.markdown(
    '<div class="footer-note">Supply Chain Late-Delivery Risk · Operational decision support</div>',
    unsafe_allow_html=True,
)