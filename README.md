# 📦 Supply Chain Late-Delivery Risk Predictor

Late deliveries cost a distributor customer trust and money, and the team usually finds out after the package has already arrived. This project predicts, **before an order ships**, how likely it is to arrive late, and ships the model as a web app that a logistics team can use without writing any code.

**Live app: [Launch Supply Chain Risk Predictor App](https://supply-chain-delivery-risk-iw6ruobvizzykxsifqqrol.streamlit.app)**

## 📸 App Preview

| Input & Form View | Prediction Results View |
| :---: | :---: |
| ![App View 1](app_screenshot_1.png) | ![App View 2](app_screenshot_2.png) |

---

## Results

Scores on a held-out test set of 35,869 order rows, evaluated once after all choices were made on the training data.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Baseline: always predict "late" | 0.548 | 0.548 | 1.000 | 0.708 | 0.500 |
| Shipping mode only (logistic regression) | 0.694 | 0.845 | 0.541 | 0.660 | 0.725 |
| **Gradient boosting (final model)** | **0.716** | **0.850** | **0.585** | **0.693** | **0.770** |

- When the model flags an order as late, it is right **85%** of the time.
- Test scores match cross-validation (ROC-AUC 0.770 vs 0.769), so the model generalizes.
- The "always late" baseline reaches recall 1.0 only by flagging every order (ROC-AUC 0.5), which is why recall is always read together with precision.

**Risk tiers on the test set**

| Risk tier | Model probability | Share of orders actually late |
| :--- | :---: | :---: |
| Lower | below 0.50 | 36.6% |
| High | 0.50 to 0.80 | 74.5% |
| Very high | 0.80 and above | 93.6% |

The riskiest 10% of orders were **100% late**, and the riskiest 30% were 89.2% late (the overall late rate is 54.8%). This makes the model most useful for deciding which orders to look at first.

---

## Project at a glance

| Metric / Parameter | Details |
| :--- | :--- |
| **Problem** | Predict late delivery at order time (binary classification, 1 = late) |
| **Data** | DataCo Smart Supply Chain: 180,519 order rows, 65,752 orders, 53 columns |
| **Features used** | 21, after removing leakage, personal data, IDs, empty, redundant and duplicate columns |
| **Final model** | Gradient boosting classifier in a scikit-learn pipeline, saved as `model.joblib` |
| **Validation** | 3-fold stratified cross-validation, grouped by order |
| **Metric that matters** | Precision and recall for late orders, with ROC-AUC for ranking |
| **Interface** | Streamlit web app (`app.py`) |
| **Deployment** | Streamlit Community Cloud |

---

## What the data showed

**Shipping mode drives lateness.**

| Shipping mode | Late rate (train) | Promised days | Typical actual days |
| :--- | :---: | :---: | :---: |
| First Class | 95.3% | 1 | 2.0 |
| Second Class | 76.8% | 2 | 3.99 |
| Same Day | 46.5% | 0 | 0.49 |
| Standard Class | 38.0% | 4 | 3.99 |

- Faster modes are late mostly because of the delivery times they promise: Second Class takes about as long as Standard Class (about 4 days) but promises 2. This comes from averages, so it is a hypothesis, not proof.
- Market, customer segment, month and weekday carry almost no signal (late rates stay between about 0.54 and 0.56).
- A rule using only shipping mode already reaches 0.696 accuracy. The other columns add a small but consistent gain (ROC-AUC 0.725 to 0.770 on the test set).

---

## The leakage audit

The model must only use information known when the order is placed. Several columns break that rule, and a model that uses them looks perfect but is useless in practice.

| Column | Decision | Evidence |
| :--- | :--- | :--- |
| `Delivery Status` | Dropped | Separates the target perfectly (it is the target in disguise) |
| `Days for shipping (real)` | Dropped | Every late order took longer than scheduled; a rule on these columns scores about 97.5% accuracy |
| `shipping date` | Dropped | Equals the order date plus the real shipping days in 97.4% of rows |
| `Order Status` | Dropped | Describes what happened after the order was placed |
| Customer personal data and IDs | Dropped | No predictive value, privacy |
| `Product Description`, `Order Zipcode`, `Product Image`, `Product Status` | Dropped | Empty, 86% missing, a link, or constant |
| Price duplicates, city and state columns | Dropped | Redundant or too many categories; covered by region, country and market |
| `Days for shipment (scheduled)` | Dropped | Identical to `Shipping Mode` |

**Split by order:** the data has about 2.7 rows per order, so train and test were split by `Order Id`. This stops the same order from appearing in both sets (overlap = 0).

The honest model scores 0.77 ROC-AUC. A leaky model would report about 97%.

---

## How it was built

1. **Problem framing:** the logistics team, the decision (warn the customer or review the order before it ships), the target and the metric.
2. **Data understanding:** size, column dictionary, missing values and class balance (54.8% late).
3. **EDA:** univariate, bivariate and multivariate analysis, ending with written insights.
4. **Preprocessing:** imputation, one-hot encoding with rare categories grouped, and date features, all inside a scikit-learn `Pipeline`. The data was split before anything was fitted.
5. **Modeling:** a majority-class baseline plus logistic regression, random forest and gradient boosting.
6. **Tuning and validation:** grouped, stratified cross-validation and randomized hyperparameter search on the training data only.
7. **Evaluation:** one pass on the untouched test set, with a confusion matrix, precision/recall/F1, ROC-AUC and error analysis.
8. **Business insight:** what the results mean and what to do next (below).
9. **Web app:** the saved pipeline served through a Streamlit app.

| Model (cross-validation, training data) | Accuracy | Precision | Recall | F1 | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Logistic regression (all features) | 0.702 | 0.826 | 0.578 | 0.680 | 0.740 |
| Random forest (untuned) | 0.719 | 0.855 | 0.587 | 0.696 | 0.755 |
| Gradient boosting (untuned) | 0.716 | 0.838 | 0.597 | 0.697 | 0.767 |
| Random forest (tuned) | 0.719 | 0.854 | 0.587 | 0.696 | 0.770 |
| Gradient boosting (tuned) | 0.719 | 0.854 | 0.587 | 0.696 | 0.769 |

The two tuned models performed the same, and gradient boosting was chosen for its more stable scores across folds. Tuning used a limited randomized search.

**Final confusion matrix (test set):** 14,176 on-time orders correctly left alone, 2,024 false alarms, 8,170 late orders missed, 11,499 late orders caught.

---

## Business recommendation

1. **Fix the promises first.** First Class (95% late) and Second Class (77% late) miss their promised delivery times far more often than Standard Class. Review whether those promises are achievable, or quote a longer window.
2. **Warn customers on flagged orders.** Orders in the high and very high tiers were late 75% and 94% of the time.
3. **Use the model to prioritize.** If the team can only review a fraction of orders, start with the riskiest 10 to 30%.
4. **Do not rely on it for Standard Class.** All 8,170 missed late orders in the test set were Standard Class (38% late, but flagged only 0.2% of the time).

If a missed late order costs about the same as a false alarm, the best cutoff is around 0.5 to 0.61. If a miss costs twice as much or more, the cheapest policy is to warn on nearly every order. The cost ratio is a business assumption, not something measured in the data.

---

## Limitations

- The data has no carrier, weather, distance or warehouse information, so even the lowest-risk tier is about 37% late.
- The overall late rate (about 55%) is nearly the same across markets, customer segments and months, and the labels could not be checked against source records. Results apply to this dataset and may not transfer to another company.
- The label comes from after-the-fact information (actual vs. scheduled days), and canceled shipments are labeled "not late". Cancellation cannot be known at order time, so these rows act as label noise.
- The model uses one company's data from a single time period.

---

## Run it yourself

**Requirements:** Python 3.11 or newer (developed with Python 3.13).

```bash
# 1. Get the code
git clone [https://github.com/noureenv9/supply-chain-delivery-risk.git](https://github.com/noureenv9/supply-chain-delivery-risk.git)
cd supply-chain-delivery-risk

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate       # Mac / Linux

# 3. Install the dependencies
pip install -r requirements.txt

# 4. Start the app (uses the included model.joblib)
streamlit run app.py