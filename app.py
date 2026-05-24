import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
import os

# 保存用データのファイル名
DIET_DETAIL_FILE = "diet_details.csv"
USER_FILE = "user_profile.csv"
INGREDIENTS_FILE = "ingredients_master.csv"
MEALS_FILE = "meals_master.csv"
HISTORY_FILE = "recent_choices.csv"

# 栄養素の定義
NUTRIENT_LABELS = [
    "エネルギー (kcal)", "たんぱく質 (g)", "脂質 (g)", "飽和脂肪酸 (g)", 
    "炭水化物 (g)", "糖質 (g)", "食物繊維 (g)", "カルシウム (mg)", 
    "鉄 (mg)", "ビタミンA (μg)", "ビタミンE (mg)", 
    "ビタミンB1 (mg)", "ビタミンB2 (mg)", "ビタミンC (mg)", "食塩相当量 (g)"
]

# --- 📊 食品成分データベースを基にしたCSVの自動生成（カテゴリ付き） ---
def generate_default_masters():
    # 1. 食材マスターの生成
    if not os.path.exists(INGREDIENTS_FILE):
        ing_data = {
            # 名前: [カテゴリ, エネルギー, たんぱく質, 脂質, 飽和脂肪酸, 炭水化物, 糖質, 食物繊維, カルシウム, 鉄, ビタミンA, ビタミンE, ビタミンB1, ビタミンB2, ビタミンC, 食塩相当量]
            "白米(150g)": ["主食・穀類", 234, 3.8, 0.5, 0.1, 55.7, 55.2, 0.5, 5, 0.2, 0, 0.0, 0.03, 0.01, 0, 0.0],
            "玄米(150g)": ["主食・穀類", 228, 4.2, 1.5, 0.3, 51.3, 49.2, 2.1, 14, 0.9, 0, 0.8, 0.24, 0.03, 0, 0.0],
            "食パン(6枚切1枚)": ["主食・穀類", 158, 5.6, 2.4, 0.5, 28.0, 26.7, 1.3, 23, 0.5, 0, 0.3, 0.05, 0.03, 0, 0.7],
            "オートミール(30g)": ["主食・穀類", 105, 4.1, 1.7, 0.3, 20.7, 17.5, 3.2, 14, 1.3, 0, 0.2, 0.06, 0.01, 0, 0.0],
            "鶏胸肉(皮なし100g)": ["肉類", 108, 22.3, 1.5, 0.4, 0.0, 0.0, 0.0, 4, 0.3, 15, 0.3, 0.09, 0.10, 2, 0.1],
            "豚バラ肉(100g)": ["肉類", 366, 14.2, 34.6, 12.4, 0.1, 0.1, 0.0, 4, 0.4, 6, 0.2, 0.50, 0.10, 0, 0.1],
            "牛もも肉(100g)": ["肉類", 182, 21.2, 9.6, 3.8, 0.5, 0.5, 0.0, 4, 2.5, 5, 0.6, 0.10, 0.20, 0, 0.1],
            "サラダチキン(100g)": ["肉類", 115, 24.0, 1.2, 0.3, 1.0, 1.0, 0.0, 5, 0.3, 0, 0.2, 0.08, 0.09, 0, 1.2],
            "サバ(生100g)": ["魚介類", 211, 20.7, 16.8, 3.7, 0.3, 0.3, 0.0, 12, 1.2, 12, 1.3, 0.17, 0.27, 1, 0.3],
            "鮭(生100g)": ["魚介類", 124, 22.3, 4.1, 0.8, 0.1, 0.1, 0.0, 10, 0.4, 25, 1.2, 0.15, 0.18, 1, 0.1],
            "マグロ(赤身100g)": ["魚介類", 115, 26.4, 1.4, 0.4, 0.1, 0.1, 0.0, 4, 1.0, 5, 0.6, 0.10, 0.05, 0, 0.1],
            "卵(1個)": ["卵・大豆製品", 76, 6.2, 5.2, 1.6, 0.2, 0.2, 0.0, 26, 0.9, 105, 0.5, 0.04, 0.22, 0, 0.2],
            "納豆(1パック)": ["卵・大豆製品", 100, 8.3, 5.0, 0.7, 6.0, 2.7, 3.3, 45, 1.7, 0, 0.3, 0.04, 0.28, 0, 0.0],
            "豆腐(絹ごし150g)": ["卵・大豆製品", 84, 7.9, 4.9, 0.7, 3.0, 2.4, 0.6, 120, 1.2, 0, 0.1, 0.15, 0.05, 0, 0.0],
            "ブロッコリー(100g)": ["野菜類", 37, 4.3, 0.5, 0.1, 6.0, 1.6, 4.4, 46, 1.3, 77, 2.4, 0.14, 0.20, 140, 0.0],
            "トマト(1個)": ["野菜類", 38, 1.3, 0.2, 0.0, 9.4, 7.4, 2.0, 13, 0.4, 108, 1.9, 0.09, 0.04, 30, 0.0],
            "ほうれん草(100g)": ["野菜類", 18, 2.2, 0.4, 0.0, 3.1, 0.3, 2.8, 49, 2.0, 350, 2.0, 0.11, 0.20, 35, 0.0],
            "バナナ(1本100g)": ["果物類", 93, 1.1, 0.2, 0.1, 22.5, 21.4, 1.1, 6, 0.3, 5, 0.4, 0.05, 0.04, 16, 0.0],
            "りんご(1/2個150g)": ["果物類", 80, 0.3, 0.2, 0.0, 21.2, 19.1, 2.1, 5, 0.2, 2, 0.3, 0.02, 0.01, 6, 0.0],
            "牛乳(200ml)": ["乳製品", 126, 6.6, 7.6, 4.7, 9.6, 9.6, 0.0, 220, 0.0, 76, 0.2, 0.08, 0.30, 2, 0.2],
            "ヨーグルト(無糖100g)": ["乳製品", 56, 3.6, 3.0, 1.9, 4.9, 4.9, 0.0, 120, 0.0, 27, 0.1, 0.04, 0.14, 0, 0.1],
            "オリーブオイル(大さじ1)": ["調味料・油", 111, 0.0, 12.0, 1.8, 0.0, 0.0, 0.0, 0, 0.0, 0, 1.5, 0.00, 0.00, 0, 0.0],
            "醤油(大さじ1)": ["調味料・油", 13, 1.4, 0.0, 0.0, 1.8, 1.6, 0.2, 4, 0.2, 0, 0.0, 0.01, 0.02, 0, 2.5]
        }
        df_ing = pd.DataFrame.from_dict(ing_data, orient='index', columns=["カテゴリ"] + NUTRIENT_LABELS)
        df_ing.to_csv(INGREDIENTS_FILE, index_label="名前")

    # 2. 料理マスターの生成
    if not os.path.exists(MEALS_FILE):
        meal_data = {
            "カレーライス": ["定番和食・ご飯物", 700, 18.0, 22.0, 6.5, 100.0, 96.5, 3.5, 40, 2.0, 80, 1.5, 0.20, 0.18, 5, 3.1],
            "牛丼(並盛)": ["定番和食・ご飯物", 730, 20.0, 24.0, 7.2, 103.0, 101.5, 1.5, 35, 2.5, 10, 1.0, 0.22, 0.20, 1, 2.7],
            "親子丼": ["定番和食・ご飯物", 550, 28.5, 12.0, 3.1, 78.0, 76.5, 1.5, 42, 1.8, 120, 0.8, 0.18, 0.25, 2, 2.5],
            "サバの塩焼き定食": ["定食・おかず系", 650, 30.0, 25.0, 5.5, 70.0, 68.0, 2.0, 50, 2.8, 25, 2.2, 0.28, 0.45, 2, 3.5],
            "から揚げ定食": ["定食・おかず系", 880, 36.0, 36.0, 8.5, 98.0, 96.0, 2.0, 48, 2.1, 40, 1.8, 0.25, 0.22, 4, 3.8],
            "お刺身定食": ["定食・おかず系", 520, 28.0, 8.0, 1.5, 75.0, 74.0, 1.0, 35, 1.8, 30, 2.5, 0.20, 0.25, 5, 2.5],
            "醤油ラーメン": ["中華・麺類", 500, 22.0, 10.0, 2.5, 75.0, 73.0, 2.0, 25, 1.8, 30, 0.5, 0.15, 0.12, 0, 6.0],
            "炒飯(チャーハン)": ["中華・麺類", 680, 14.0, 19.0, 4.5, 105.0, 103.0, 2.0, 32, 1.5, 95, 1.1, 0.15, 0.16, 2, 3.2],
            "パスタ（カルボナーラ）": ["洋食・イタリアン", 750, 20.0, 30.0, 12.0, 85.0, 83.5, 1.5, 110, 1.5, 130, 1.1, 0.14, 0.25, 1, 2.5],
            "マルゲリータ(2ピース)": ["洋食・イタリアン", 410, 15.0, 14.0, 5.8, 52.0, 49.5, 2.5, 260, 0.9, 150, 1.4, 0.09, 0.18, 12, 2.0],
            "ハンバーガー": ["軽食・ファストフード", 260, 13.0, 10.0, 3.5, 30.0, 28.5, 1.5, 45, 1.4, 15, 0.4, 0.10, 0.14, 1, 1.3],
            "味噌汁": ["スープ・サイド", 40, 2.5, 1.2, 0.2, 4.5, 3.5, 1.0, 22, 0.5, 15, 0.2, 0.03, 0.04, 3, 1.5],
            "ショートケーキ": ["スイーツ・カフェ", 350, 4.5, 22.0, 13.0, 32.0, 31.2, 0.8, 60, 0.4, 90, 0.5, 0.04, 0.12, 2, 0.2]
        }
        df_meal = pd.DataFrame.from_dict(meal_data, orient='index', columns=["カテゴリ"] + NUTRIENT_LABELS)
        df_meal.to_csv(MEALS_FILE, index_label="名前")

generate_default_masters()

# --- 🚀 キャッシュ機能を使った高速データ読み込み ---
@st.cache_data
def load_master_databases():
    # index_col="名前" を指定して読み込みます
    df_ing = pd.read_csv(INGREDIENTS_FILE, index_col="名前")
    df_meal = pd.read_csv(MEALS_FILE, index_col="名前")
    return df_ing, df_meal

# 正しい関数名で呼び出し、大文字の変数に格納します
DF_INGREDIENTS, DF_MEALS = load_master_databases()

# --- 🕒 履歴（最近選んだ項目）の管理機能 ---
def load_recent_choices():
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)["ItemName"].tolist()
    return []

def save_recent_choice(item_name):
    choices = load_recent_choices()
    if item_name in choices:
        choices.remove(item_name)
    choices.insert(0, item_name)
    pd.DataFrame(choices[:8], columns=["ItemName"]).to_csv(HISTORY_FILE, index=False)

# --- 👤 プロフィール・目標計算 ---
def calculate_targets(gender, age, height, weight, activity):
    if gender == "男性":
        bmr = 66.47 + (13.75 * weight) + (5.0 * height) - (6.75 * age)
    else:
        bmr = 655.1 + (9.56 * weight) + (1.85 * height) - (4.68 * age)
    act_v = 1.2 if activity == "低い (デスクワーク中心)" else 1.5 if activity == "普通 (立ち仕事・軽い運動)" else 1.75
    target_cal = int(bmr * act_v)
    p = round((target_cal * 0.15) / 4, 1)
    f = round((target_cal * 0.25) / 9, 1)
    c = round((target_cal * 0.60) / 4, 1)
    return {
        "エネルギー (kcal)": target_cal, "たんぱく質 (g)": p, "脂質 (g)": f,
        "飽和脂肪酸 (g)": round(target_cal * 0.07 / 9, 1), "炭水化物 (g)": c, "糖質 (g)": round(c * 0.8, 1),
        "食物繊維 (g)": 20.0 if gender == "男性" else 18.0, "カルシウム (mg)": 800 if gender == "男性" else 650,
        "鉄 (mg)": 7.5 if gender == "男性" else (10.5 if age < 50 else 6.5), "ビタミンA (μg)": 850 if gender == "男性" else 650,
        "ビタミンE (mg)": 6.5 if gender == "男性" else 6.0, "ビタミンB1 (mg)": 1.4 if gender == "男性" else 1.1,
        "ビタミンB2 (mg)": 1.6 if gender == "男性" else 1.2, "ビタミンC (mg)": 100, "食塩相当量 (g)": 7.5 if gender == "男性" else 6.5
    }

def calculate_nutrients_from_details(df_details):
    totals = [0.0] * len(NUTRIENT_LABELS)
    for _, row in df_details.iterrows():
        item = row["ItemName"]
        amount = float(row["Amount"])
        df_db = DF_INGREDIENTS if row["ItemType"] == "食材" else DF_MEALS
        if item in df_db.index:
            for i, label in enumerate(NUTRIENT_LABELS):
                totals[i] += float(df_db.loc[item, label]) * amount
    return totals

# --- 📱 メインUI ---
st.title("🥇 パーソナル AI あすけん (大容量対応版)")

# 【新規追加】サイドバー：最近選んだ項目（別の専用枠）
st.sidebar.title("🕒 クイックアクセス")
recent_items = load_recent_choices()
if recent_items:
    st.sidebar.markdown("### 最近選んだ項目")
    selected_recent = st.sidebar.selectbox("履歴から選ぶと下に数量設定が出ます", ["選択してください"] + recent_items)
    if selected_recent != "選択してください":
        is_ing = selected_recent in DF_INGREDIENTS.index
        item_type = "食材" if is_ing else "料理"
        st.sidebar.info(f"{selected_recent} ({item_type}) を選択中")
        r_amount = st.sidebar.selectbox("数量 (履歴用)", [0.25, 0.5, 0.75, 1.0, 1.5, 2.0], index=3, key="recent_amt")
        if st.sidebar.button("この内容で即時追加", type="primary"):
            today_str = datetime.date.today().strftime("%Y-%m-%d")
            history_row = pd.DataFrame([{"Date": today_str, "Timing": "昼食", "ItemName": selected_recent, "ItemType": item_type, "InputMode": "選択式", "Amount": r_amount}])
            df_all = pd.concat([pd.read_csv(DIET_DETAIL_FILE), history_row], ignore_index=True) if os.path.exists(DIET_DETAIL_FILE) else history_row
            df_all.to_csv(DIET_DETAIL_FILE, index=False)
            st.sidebar.success("履歴から食事を追加しました！")
            st.rerun()
else:
    st.sidebar.write("登録された履歴はまだありません。")

tab1, tab2, tab3 = st.tabs(["👤 プロフィール", "✍ 食事の記録", "📊 履歴・提案シミュレーション"])

# --- TAB 1: プロフィール ---
with tab1:
    if os.path.exists(USER_FILE):
        u_df = pd.read_csv(USER_FILE).iloc[0]
        init_g, init_a, init_h, init_w, init_ac = u_df["Gender"], int(u_df["Age"]), float(u_df["Height"]), float(u_df["Weight"]), u_df["Activity"]
    else:
        init_g, init_a, init_h, init_w, init_ac = "女性", 25, 160.0, 55.0, "普通 (立ち仕事・軽い運動)"
    with st.form("profile"):
        g = st.radio("性別", ["女性", "男性"], index=0 if init_g == "女性" else 1)
        a = st.number_input("年齢", value=init_a)
        h = st.number_input("身長 (cm)", value=init_h)
        w = st.number_input("体重 (kg)", value=init_w)
        ac = st.selectbox("活動レベル", ["低い (デスクワーク中心)", "普通 (立ち仕事・軽い運動)", "高い (活発な運動習慣あり)"], index=["低い (デスクワーク中心)", "普通 (立ち仕事・軽い運動)", "高い (活発な運動習慣あり)"].index(init_ac))
        if st.form_submit_button("保存"):
            pd.DataFrame([{"Gender": g, "Age": a, "Height": h, "Weight": w, "Activity": ac}]).to_csv(USER_FILE, index=False)
            st.rerun()

user_targets = calculate_targets(g, a, h, w, ac)

# --- TAB 2: 食事の記録（カテゴリ分けフィルタ搭載） ---
with tab2:
    st.header("食事を新しく追加する")
    col_d, col_t = st.columns(2)
    r_date = col_d.date_input("日付", datetime.date.today())
    r_time = col_t.selectbox("タイミング", ["朝食", "昼食", "夕食", "間食"])
    
    st.markdown("---")
    
    # 【新規追加】カテゴリ分けフィルタのUI
    st.subheader("🔍 カテゴリで絞り込んで選ぶ")
    
    col_cat1, col_cat2 = st.columns(2)
    
    # 食材のフィルタリング
    all_ing_categories = ["すべて"] + sorted(list(DF_INGREDIENTS["カテゴリ"].unique()))
    selected_ing_cat = col_cat1.selectbox("🥑 食材のカテゴリ", all_ing_categories)
    if selected_ing_cat == "すべて":
        ing_options = sorted(list(DF_INGREDIENTS.index))
    else:
        ing_options = sorted(list(DF_INGREDIENTS[DF_INGREDIENTS["カテゴリ"] == selected_ing_cat].index))
        
    # 料理のフィルタリング
    all_meal_categories = ["すべて"] + sorted(list(DF_MEALS["カテゴリ"].unique()))
    selected_meal_cat = col_cat2.selectbox("🍛 料理のカテゴリ", all_meal_categories)
    if selected_meal_cat == "すべて":
        meal_options = sorted(list(DF_MEALS.index))
    else:
        meal_options = sorted(list(DF_MEALS[DF_MEALS["カテゴリ"] == selected_meal_cat].index))

    sel_ing = st.multiselect("🥑 食材を選択（上のカテゴリで絞り込めます）", ing_options)
    sel_meal = st.multiselect("🍛 料理名を選択（上のカテゴリで絞り込めます）", meal_options)
    
    save_list = []
    if sel_ing or sel_meal:
        st.write("▼ それぞれの量を調整")
        for item in sel_ing:
            m = st.radio(f"入力方法 ({item})", ["選択式", "記入式"], horizontal=True, key=f"m_i_{item}")
            v = st.selectbox(f"数量 ({item})", [0.25, 0.5, 0.75, 1.0, 1.5, 2.0], index=3, key=f"s_i_{item}") if m=="選択式" else st.number_input(f"倍率 ({item})", value=1.0, key=f"n_i_{item}")
            save_list.append({"Date": r_date.strftime("%Y-%m-%d"), "Timing": r_time, "ItemName": item, "ItemType": "食材", "InputMode": m, "Amount": v})
        for item in sel_meal:
            m = st.radio(f"入力方法 ({item})", ["選択式", "記入式"], horizontal=True, key=f"m_m_{item}")
            v = st.selectbox(f"数量 ({item})", [0.25, 0.5, 0.75, 1.0, 1.5, 2.0], index=3, key=f"s_m_{item}") if m=="選択式" else st.number_input(f"倍率 ({item})", value=1.0, key=f"n_m_{item}")
            save_list.append({"Date": r_date.strftime("%Y-%m-%d"), "Timing": r_time, "ItemName": item, "ItemType": "料理", "InputMode": m, "Amount": v})

    if st.button("この食事内容で保存する", type="primary"):
        if not save_list:
            st.error("メニューが選ばれていません。")
        else:
            # 履歴用に選択したアイテム名を保存
            for s in save_list:
                save_recent_choice(s["ItemName"])
            
            new_df = pd.DataFrame(save_list)
            df = pd.concat([pd.read_csv(DIET_DETAIL_FILE), new_df], ignore_index=True) if os.path.exists(DIET_DETAIL_FILE) else new_df
            df.to_csv(DIET_DETAIL_FILE, index=False)
            st.success("明細データを保存しました！")
            st.rerun()

# --- TAB 3: 履歴・修正・提案 ---
with tab3:
    st.header("履歴の管理と提案シミュレーション")
    if os.path.exists(DIET_DETAIL_FILE) and len(pd.read_csv(DIET_DETAIL_FILE)) > 0:
        df_history = pd.read_csv(DIET_DETAIL_FILE)
        unique_dates = sorted(df_history["Date"].unique(), reverse=True)
        view_date = st.selectbox("確認・修正したい日付", unique_dates)
        
        st.markdown("### 🛠 登録メニューの修正・削除")
        df_day = df_history[df_history["Date"] == view_date]
        selected_time = st.selectbox("食事のタイミングを選択", df_day["Timing"].unique())
        
        df_target_meal = df_day[df_day["Timing"] == selected_time]
        st.write("このタイミングに登録されているメニュー一覧:")
        edited_meal_df = st.data_editor(
            df_target_meal[["ItemName", "ItemType", "InputMode", "Amount"]], 
            hide_index=True, 
            key=f"editor_{view_date}_{selected_time}"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        if col_btn1.button("✍ 変更（数量など）を適用する", type="primary"):
            df_history = df_history[~((df_history["Date"] == view_date) & (df_history["Timing"] == selected_time))]
            edited_meal_df["Date"] = view_date
            edited_meal_df["Timing"] = selected_time
            df_history = pd.concat([df_history, edited_meal_df], ignore_index=True)
            df_history.to_csv(DIET_DETAIL_FILE, index=False)
            st.success("食事内容を修正しました！")
            st.rerun()
            
        if col_btn2.button("🗑 このタイミングの食事を丸ごと削除する"):
            df_history = df_history[~((df_history["Date"] == view_date) & (df_history["Timing"] == selected_time))]
            df_history.to_csv(DIET_DETAIL_FILE, index=False)
            st.success("削除しました。")
            st.rerun()
            
        st.divider()
        
        df_day_latest = df_history[df_history["Date"] == view_date]
        day_totals = calculate_nutrients_from_details(df_day_latest)
        
        overs, unders = [], []
        sim_totals = list(day_totals)
        
        for i, label in enumerate(NUTRIENT_LABELS):
            consumed = day_totals[i]
            target = user_targets[label]
            pct = (consumed / target) * 100 if target > 0 else 0.0
            if label in ["エネルギー (kcal)", "脂質 (g)", "飽和脂肪酸 (g)", "糖質 (g)", "食塩相当量 (g)"]:
                if pct > 110.0: overs.append(label)
            else:
                if pct < 70.0: unders.append(label)
                
        sim_applied_msg = []
        if ("エネルギー (kcal)" in overs or "脂質 (g)" in overs) and any(x in df_day_latest["ItemName"].values for x in ["カレーライス", "かつ丼", "から揚げ定食"]):
            for idx, r in df_day_latest.iterrows():
                if r["ItemName"] in ["カレーライス", "かつ丼", "から揚げ定食"]:
                    old_item = r["ItemName"]
                    for i, label in enumerate(NUTRIENT_LABELS):
                        sim_totals[i] -= float(DF_MEALS.loc[old_item, label]) * float(r["Amount"])
                        sim_totals[i] += float(DF_MEALS.loc["お刺身定食", label])
                    sim_applied_msg.append(f"・過剰な脂質対策：重い主食『{old_item}』を『お刺身定食』へ置き換え")
                    break
        if "たんぱく質 (g)" in unders:
            for i, label in enumerate(NUTRIENT_LABELS): sim_totals[i] += float(DF_INGREDIENTS.loc["サラダチキン(100g)", label])
            sim_applied_msg.append("・たんぱく質不足対策：『サラダチキン(100g)』を1品追加")
        if "食物繊維 (g)" in unders:
            for i, label in enumerate(NUTRIENT_LABELS): sim_totals[i] += float(DF_INGREDIENTS.loc["ブロッコリー(100g)", label])
            sim_applied_msg.append("・食物繊維不足対策：『ブロッコリー(100g)』を1品追加")

        comp_rows = []
        graph_colors = []
        for i, label in enumerate(NUTRIENT_LABELS):
            c = day_totals[i]
            t = user_targets[label]
            pct = round((c / t) * 100, 1) if t > 0 else 0.0
            sim_pct = round((sim_totals[i] / t) * 100, 1) if t > 0 else 0.0
            
            if label in ["エネルギー (kcal)", "脂質 (g)", "飽和脂肪酸 (g)", "糖質 (g)", "食塩相当量 (g)"]:
                color = "#EF5350" if pct > 110.0 else "#66BB6A" if pct >= 70.0 else "#42A5F5"
            else:
                color = "#66BB6A" if pct >= 100.0 else "#81C784" if pct >= 70.0 else "#FFCA28"
                
            comp_rows.append({"栄養素": label, "現在摂取量": c, "目標値": t, "現在達成率(%)": pct, "提案反映後達成率(%)": sim_pct})
            graph_colors.append(color)
            
        df_comp = pd.DataFrame(comp_rows)
        
        st.subheader(f"📅 {view_date} の栄養素比較（現在 vs 提案反映後）")
        
        fig = go.Figure()
        fig.add_trace(go.Bar(y=df_comp["栄養素"], x=df_comp["現在達成率(%)"], name="現在の食事", orientation='h', marker_color=graph_colors))
        fig.add_trace(go.Bar(y=df_comp["栄養素"], x=df_comp["提案反映後達成率(%)"], name="AI提案を反映した場合", orientation='h', marker_color="#FFA726"))
        fig.update_layout(barmode='group', height=600, margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 💡 AI栄養士からのアドバイス")
        if sim_applied_msg:
            for msg in sim_applied_msg: st.markdown(msg)
        else:
            st.success("🎉 パーフェクトな栄養バランスです！")
            
        st.dataframe(df_comp, use_container_width=True)
    else:
        st.info("新しい形式での食事履歴がありません。「食事の記録」から新しく登録してください。")