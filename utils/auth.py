import streamlit as st
import bcrypt
from database import User, get_db
import uuid

def hash_password(p: str) -> str:
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def login_user(email: str, password: str):
    with get_db() as db:
        user = db.query(User).filter(User.email == email).first()
        if user and verify_password(password, user.password):
            return {"id": user.id, "name": user.name, "email": user.email}
    return None

def register_user(name: str, email: str, password: str):
    new_id = str(uuid.uuid4())
    with get_db() as db:
        if db.query(User).filter(User.email == email).first():
            return None, "Email already registered"
        db.add(User(id=new_id, name=name, email=email, password=hash_password(password)))
    return {"id": new_id, "name": name, "email": email}, None

def require_auth():
    if "user" not in st.session_state:
        st.warning("Please login to continue.")
        st.stop()
    return st.session_state.user
