import streamlit as st
import requests
import os

# your deployed fastapi backend (render). can be overridden with a secret/env var
# if you ever move the backend somewhere else, just change this one line.
try:
    API_URL = st.secrets["API_URL"]
except Exception:
    API_URL = os.environ.get("API_URL", "https://churnpredict-1.onrender.com")

st.set_page_config(page_title="Customer Churn Prediction", page_icon="📉", layout="centered")

st.markdown("""
<style>
.big-title { font-size: 2rem; font-weight: 700; margin-bottom: 0; }
.small-sub { color: gray; margin-top: 0; margin-bottom: 1.5rem; }
.result-box {
    padding: 1.2rem 1.5rem;
    border-radius: 10px;
    margin-top: 1rem;
}
.churn { background-color: #3a1a1a; border: 1px solid #ff4b4b; }
.stay { background-color: #10321a; border: 1px solid #21c354; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">📉 Customer Churn Prediction</p>', unsafe_allow_html=True)
st.markdown('<p class="small-sub">Fill in the customer details and check if they are likely to churn.</p>', unsafe_allow_html=True)

# note: render free tier spins down when idle, first request can take 30-50s to wake up
with st.sidebar:
    st.subheader("API status")
    if st.button("Check backend"):
        try:
            r = requests.get(f"{API_URL}/health", timeout=60)
            if r.ok:
                st.success("Backend is up")
                st.json(r.json())
            else:
                st.warning(f"Backend returned {r.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Backend unreachable: {e}")
    st.caption("First request after inactivity can be slow (Render free tier cold start).")

col1, col2 = st.columns(2)

with col1:
    geography = st.selectbox('Geography', ['France', 'Germany', 'Spain'])
    gender = st.selectbox('Gender', ['Male', 'Female'])
    age = st.slider('Age', 18, 92, 35)
    tenure = st.slider('Tenure (years with bank)', 0, 10, 3)
    num_of_products = st.slider('Number of Products', 1, 4, 1)

with col2:
    credit_score = st.number_input('Credit Score', min_value=350, max_value=850, value=650)
    balance = st.number_input('Account Balance', min_value=0.0, value=50000.0, step=1000.0)
    estimated_salary = st.number_input('Estimated Salary', min_value=0.0, value=60000.0, step=1000.0)
    has_cr_card = st.selectbox('Has Credit Card', ['Yes', 'No'])
    is_active_member = st.selectbox('Is Active Member', ['Yes', 'No'])

st.write("")
predict_clicked = st.button('🔮 Predict', use_container_width=True)

if predict_clicked:
    payload = {
        'CreditScore': credit_score,
        'Geography': geography,
        'Gender': gender,
        'Age': age,
        'Tenure': tenure,
        'Balance': balance,
        'NumOfProducts': num_of_products,
        'HasCrCard': 1 if has_cr_card == 'Yes' else 0,
        'IsActiveMember': 1 if is_active_member == 'Yes' else 0,
        'EstimatedSalary': estimated_salary
    }

    with st.spinner('Talking to the model (can take a bit if it just woke up)...'):
        try:
            res = requests.post(f'{API_URL}/predict', json=payload, timeout=60)
        except requests.exceptions.RequestException as e:
            st.error(f"Could not reach the API: {e}")
            st.stop()

    if res.status_code != 200:
        st.error(f"API error ({res.status_code}): {res.text}")
        st.stop()

    data = res.json()
    prob = data['churn_probability']
    will_churn = data['prediction'] == 1

    box_class = "churn" if will_churn else "stay"
    emoji = "⚠️" if will_churn else "✅"

    st.markdown(f"""
    <div class="result-box {box_class}">
        <h3>{emoji} {data['result']}</h3>
        <p>Churn probability: <b>{prob*100:.1f}%</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.progress(min(max(prob, 0.0), 1.0))