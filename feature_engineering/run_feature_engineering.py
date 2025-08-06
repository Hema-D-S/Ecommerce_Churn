from feature_engineering.compute_rfm import compute_rfm
from feature_engineering.compute_features import compute_additional_features
from feature_engineering.decision_checks import apply_decision_checks
from feature_engineering.label_churn import label_churn, save_features

INPUT_CSV = "feature_engineering/raw_customer_data.csv"
CUTOFF_DATE = "2023-12-31"  # Change this to your desired cutoff date

# 1) RFM
rfm_df = compute_rfm(INPUT_CSV, CUTOFF_DATE)

# 2) Additional features
features_df = compute_additional_features(INPUT_CSV, CUTOFF_DATE)

# 3) Decision checks
merged_df = apply_decision_checks(rfm_df, features_df)

# 4) Label churn + save
final_df = label_churn(merged_df)
save_features(final_df, output_file='feature_engineering/engineered_features.csv')
