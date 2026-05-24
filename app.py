import streamlit as st
import pandas as pd
import os

# --- 設定 ---
INGREDIENTS_FILE = "ingredients_master.csv"
HISTORY_FILE = "recent_choices.csv"

# --- 1. 最近選んだ項目の管理 ---
def load_recent_choices():
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)["ItemName"].tolist()
    return []

def save_choice(item_name):
    choices = load_recent_choices()
    if item_name in choices:
        choices.remove(item_name)
    choices.insert(0, item_name)
    pd.DataFrame(choices[:10], columns=["ItemName"]).to_csv(HISTORY_FILE, index=False)

# --- 2. 検索とリスト表示 ---
st.title("🥇 パーソナル AI あすけん (Ver. 1000+) ")

# 最近の履歴を表示（すぐに選択できるように）
recent = load_recent_choices()
if recent:
    st.sidebar.subheader("🕒 最近選んだ項目")
    selected_recent = st.sidebar.radio("履歴から選ぶ", recent)
    if st.sidebar.button("履歴から追加"):
        st.write(f"{selected_recent} を追加します！")
        save_choice(selected_recent)

# 全データからの検索（1000件あっても高速）
# 実際にはここに ingredients_master.csv を読み込む処理を入れます
st.subheader("🥑 食材検索")
search = st.text_input("食材名で検索...")
# ここで df[df['name'].str.contains(search)] のようにフィルタリングして表示します
import streamlit as st
import pandas as pd

# データファイルをキャッシュ付きで読み込む（1000件あっても一瞬です）
@st.cache_data
def load_data():
    df_ing = pd.read_csv("ingredients_master.csv")
    df_meal = pd.read_csv("meals_master.csv")
    return df_ing, df_meal

df_ing, df_meal = load_data()

# 検索UIの作成
st.title("食材・料理データベース (Ver. 1000+)")
search_query = st.text_input("食材や料理名で検索:")

if search_query:
    # 検索結果を表示
    result = df_ing[df_ing['名前'].str.contains(search_query)]
    st.write(result)