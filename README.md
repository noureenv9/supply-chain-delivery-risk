# 📦 Supply Chain Late-Delivery Risk Predictor

An end-to-end Machine Learning web application built with **Streamlit** to predict the risk of late shipments in supply chain operations. This tool helps logistics and operations teams proactively identify high-risk orders and mitigate delivery delays before they impact customers.

---

## 🚀 Live App
Check out the live interactive web application here:  
👉 **[Launch Supply Chain Risk Predictor App](https://supply-chain-delivery-risk-iw6ruobvizzykxsifqqrol.streamlit.app)**

---

## 📸 App Preview
> *(Optional: To add a screenshot of your running app, take a picture of your browser, save it in this folder as `app_screenshot.png`, and it will render automatically!)*

---

## 📊 Results & Model Performance

The classification model evaluates key order attributes—such as shipping mode, scheduled vs. actual transit parameters, and order characteristics—to calculate real-time delivery risk probabilities.

| Metric / Parameter | Details |
| :--- | :--- |
| **Model Type** | Machine Learning Classifier (`model.joblib`) |
| **Interface** | Streamlit Web Framework (`app.py`) |
| **Target Variable** | Late Delivery Risk (Binary Classification) |
| **Deployment** | Streamlit Community Cloud |

---

## 🛠️ How to Run Locally

To run this application on your local machine, follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/noureenv9/supply-chain-delivery-risk.git](https://github.com/noureenv9/supply-chain-delivery-risk.git)
cd supply-chain-delivery-risk