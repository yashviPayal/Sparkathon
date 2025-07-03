import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash

USER_DB = "data/users.csv"

def load_users():
    return pd.read_csv(USER_DB)

def save_user(username, password, role="user"):
    df = load_users()
    if username in df['username'].values:
        return False  # user already exists

    # Hash the password before saving
    hashed_password = generate_password_hash(password)
    new_user = pd.DataFrame([[username, hashed_password, role]], columns=["username", "password", "role"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_DB, index=False)
    return True

def verify_login(username, password):
    df = load_users()
    user = df[df['username'] == username]
    if not user.empty:
        hashed_password = user.iloc[0]['password']
        if check_password_hash(hashed_password, password):
            return user.iloc[0]['role']
    return None
