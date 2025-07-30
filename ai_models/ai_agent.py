import pandas as pd
import joblib
from pathlib import Path

# Load models and scalers
model_dir = Path("model")

fraud_model = joblib.load(model_dir / "fraud_model.pkl")
fraud_scaler = joblib.load(model_dir / "fraud_scaler.pkl")

bot_model = joblib.load(model_dir / "bot_model.pkl")
bot_scaler = joblib.load(model_dir / "bot_scaler.pkl")

behavior_model = joblib.load(model_dir / "behavior_model.pkl")
behavior_scaler = joblib.load(model_dir / "behavior_scaler.pkl")

security_model = joblib.load(model_dir / "security_model.pkl")
security_scaler = joblib.load(model_dir / "security_scaler.pkl")

def run_full_predictions(input_dict: dict) -> dict:
    """
    Takes a session dictionary, returns predictions from all models.
    """
    # ---- Fraud Detection ----
    fraud_df = pd.DataFrame([{
        "purchase_amount": input_dict["purchase_amount"],
        "num_items": input_dict["num_items"],
        "account_age_days": input_dict["account_age_days"],
        "session_duration": input_dict["session_duration"]
    }])
    fraud_pred = fraud_model.predict(fraud_scaler.transform(fraud_df))[0]

    # ---- Bot Detection ----
    bot_df = pd.DataFrame([{
        "user_agent_contains_bot": input_dict["user_agent_contains_bot"],
        "navigator_webdriver": input_dict["navigator_webdriver"],
        "js_enabled": input_dict["js_enabled"],
        "cookie_enabled": input_dict["cookie_enabled"],
        "typing_time": input_dict["typing_time"],
        "paste_detected": input_dict["paste_detected"],
        "mouse_moves_per_second": input_dict["mouse_moves_per_second"]
    }])
    bot_pred = bot_model.predict(bot_scaler.transform(bot_df))[0]

    # ---- Behavior Detection ----
    behavior_df = pd.DataFrame([{
        "typing_time": input_dict["typing_time"],
        "paste_detected": input_dict["paste_detected"],
        "mouse_moves_per_second": input_dict["mouse_moves_per_second"],
        "scroll_depth": input_dict["scroll_depth"],
        "total_time_on_page": input_dict["total_time_on_page"],
        "keystroke_variance": input_dict["keystroke_variance"],
        "click_count": input_dict["click_count"],
        "mouse_click_rate": input_dict["mouse_click_rate"],
        "idle_time_ratio": input_dict["idle_time_ratio"],
        "hover_time": input_dict["hover_time"],
        "scroll_velocity": input_dict["scroll_velocity"]
    }])
    behavior_pred = behavior_model.predict(behavior_scaler.transform(behavior_df))[0]

    # ---- Security Threat Detection ----
    security_df = pd.DataFrame([{
        "failed_login_attempts": input_dict.get("failed_login_attempts", 0),
        "geo_location_mismatch": input_dict.get("geo_location_mismatch", 0),
        "timezone_mismatch": input_dict.get("timezone_mismatch", 0),
        "multiple_sessions_same_ip": input_dict.get("multiple_sessions_same_ip", 0),
        "account_takeover_risk": input_dict.get("account_takeover_risk", 0),
        "sudden_ip_change": input_dict.get("sudden_ip_change", 0),
        "captcha_triggered": input_dict.get("captcha_triggered", 0)
    }])
    security_pred = security_model.predict(security_scaler.transform(security_df))[0]

    return {
        "fraud": int(fraud_pred),
        "bot": int(bot_pred),
        "behavior": int(behavior_pred),
        "security_threat": int(security_pred)
    }
