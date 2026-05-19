import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
import os

# 保存用データのファイル名（新設計の明細データ用）
DIET_DETAIL_FILE = "diet_details.csv"
USER_FILE = "user_profile.csv"

# 完全日本語化の栄養素
NUTRIENT_LABELS = [
    "エネルギー (kcal)", "たんぱく質 (g)", "脂質 (g)", "飽和脂肪酸 (g)", 
    "炭水化物 (g)", "糖質 (g)", "食物繊維 (g)", "カルシウム (mg)", 
    "鉄 (mg)", "ビタミンA (μg)", "ビタミンE (mg)", 
    "ビタミンB1 (mg)", "ビタミンB2 (mg)", "ビタミンC (mg)", "食塩相当量 (g)"
]

# --- 1. マスターデータベース ---
INGREDIENTS_DB = {
    "白米(150g)": [234, 3.8, 0.5, 0.1, 55.7, 55.2, 0.5, 5, 0.2, 0, 0.0, 0.03, 0.01, 0, 0.0],
    "玄米(150g)": [228, 4.2, 1.5, 0.3, 51.3, 49.2, 2.1, 14, 0.9, 0, 0.8, 0.24, 0.03, 0, 0.0],
    "食パン(6枚切1枚)": [158, 5.6, 2.4, 0.5, 28.0, 26.7, 1.3, 23, 0.5, 0, 0.3, 0.05, 0.03, 0, 0.7],
    "オートミール(30g)": [105, 4.1, 1.7, 0.3, 20.7, 17.5, 3.2, 14, 1.3, 0, 0.2, 0.06, 0.01, 0, 0.0],
    "パスタ(乾麺100g)": [347, 12.0, 2.0, 0.4, 72.0, 68.0, 4.0, 20, 1.5, 0, 0.5, 0.15, 0.05, 0, 0.0],
    "うどん(生1玉)": [240, 6.1, 0.8, 0.1, 52.0, 50.0, 2.0, 15, 0.4, 0, 0.0, 0.04, 0.01, 0, 0.8],
    "そぼ(乾麺100g)": [344, 14.0, 2.0, 0.4, 72.0, 67.0, 5.0, 43, 2.8, 0, 0.0, 0.45, 0.12, 0, 0.0],
    "鶏胸肉(皮なし100g)": [108, 22.3, 1.5, 0.4, 0.0, 0.0, 0.0, 4, 0.3, 15, 0.3, 0.09, 0.10, 2, 0.1],
    "鶏もも肉(皮なし100g)": [116, 18.8, 3.9, 1.1, 0.0, 0.0, 0.0, 5, 0.6, 22, 0.4, 0.12, 0.18, 1, 0.1],
    "サラダチキン(100g)": [115, 24.0, 1.2, 0.3, 1.0, 1.0, 0.0, 5, 0.3, 0, 0.2, 0.08, 0.09, 0, 1.2],
    "豚バラ肉(100g)": [366, 14.2, 34.6, 12.4, 0.1, 0.1, 0.0, 4, 0.4, 6, 0.2, 0.50, 0.10, 0, 0.1],
    "牛もも肉(100g)": [182, 21.2, 9.6, 3.8, 0.5, 0.5, 0.0, 4, 2.5, 5, 0.6, 0.10, 0.20, 0, 0.1],
    "サバ(生100g)": [211, 20.7, 16.8, 3.7, 0.3, 0.3, 0.0, 12, 1.2, 12, 1.3, 0.17, 0.27, 1, 0.3],
    "ツナ缶(オイル無1缶)": [48, 11.5, 0.2, 0.0, 0.1, 0.1, 0.0, 5, 0.6, 0, 0.5, 0.02, 0.03, 0, 0.7],
    "卵(1個)": [76, 6.2, 5.2, 1.6, 0.2, 0.2, 0.0, 26, 0.9, 105, 0.5, 0.04, 0.22, 0, 0.2],
    "納豆(1パック)": [100, 8.3, 5.0, 0.7, 6.0, 2.7, 3.3, 45, 1.7, 0, 0.3, 0.04, 0.28, 0, 0.0],
    "豆腐(絹ごし150g)": [84, 7.9, 4.9, 0.7, 3.0, 2.4, 0.6, 120, 1.2, 0, 0.1, 0.15, 0.05, 0, 0.0],
    "牛乳(200ml)": [126, 6.6, 7.6, 4.7, 9.6, 9.6, 0.0, 220, 0.0, 76, 0.2, 0.08, 0.30, 2, 0.2],
    "ヨーグルト(無糖100g)": [56, 3.6, 3.0, 1.9, 4.9, 4.9, 0.0, 120, 0.0, 27, 0.1, 0.04, 0.14, 0, 0.1],
    "ギリシャヨーグルト(100g)": [67, 10.0, 0.0, 0.0, 4.8, 4.8, 0.0, 110, 0.0, 0, 0.0, 0.04, 0.12, 0, 0.1],
    "プロテイン(1杯)": [120, 20.0, 2.0, 1.0, 3.0, 2.5, 0.5, 100, 1.5, 0, 0.0, 0.30, 0.30, 30, 0.3],
    "ブロッコリー(100g)": [37, 4.3, 0.5, 0.1, 6.0, 1.6, 4.4, 46, 1.3, 77, 2.4, 0.14, 0.20, 140, 0.0],
    "アボカド(1/2個)": [120, 1.9, 11.3, 1.7, 4.6, 1.4, 3.2, 7, 0.4, 5, 2.1, 0.06, 0.03, 9, 0.0],
    "トマト(1個)": [38, 1.3, 0.2, 0.0, 9.4, 7.4, 2.0, 13, 0.4, 108, 1.9, 0.09, 0.04, 30, 0.0],
    "ほうれん草(100g)": [18, 2.2, 0.4, 0.0, 3.1, 0.3, 2.8, 49, 2.0, 350, 2.0, 0.11, 0.20, 35, 0.0],
    "ミックスナッツ(25g)": [152, 5.0, 13.5, 1.5, 4.5, 2.5, 2.0, 35, 1.1, 0, 3.2, 0.12, 0.05, 0, 0.0],
    "オリーブオイル(大さじ1)": [111, 0.0, 12.0, 1.8, 0.0, 0.0, 0.0, 0, 0.0, 0, 1.5, 0.00, 0.00, 0, 0.0]
}

MEALS_DB = {
    "カレーライス": [700, 18.0, 22.0, 6.5, 100.0, 96.5, 3.5, 40, 2.0, 80, 1.5, 0.20, 0.18, 5, 3.1],
    "牛丼(並盛)": [730, 20.0, 24.0, 7.2, 103.0, 101.5, 1.5, 35, 2.5, 10, 1.0, 0.22, 0.20, 1, 2.7],
    "親子丼": [550, 28.5, 12.0, 3.1, 78.0, 76.5, 1.5, 42, 1.8, 120, 0.8, 0.18, 0.25, 2, 2.5],
    "かつ丼": [880, 32.0, 31.0, 9.5, 110.0, 108.0, 2.0, 50, 2.6, 110, 1.5, 0.65, 0.28, 1, 3.8],
    "オムライス": [620, 16.5, 19.5, 5.8, 88.0, 86.0, 2.0, 45, 1.9, 140, 1.8, 0.15, 0.22, 12, 2.6],
    "ハンバーグ定食": [850, 32.0, 38.0, 12.0, 90.0, 87.5, 2.5, 65, 3.5, 95, 2.0, 0.35, 0.30, 8, 3.8],
    "サバの塩焼き定食": [650, 30.0, 25.0, 5.5, 70.0, 68.0, 2.0, 50, 2.8, 25, 2.2, 0.28, 0.45, 2, 3.5],
    "から揚げ定食": [880, 36.0, 36.0, 8.5, 98.0, 96.0, 2.0, 48, 2.1, 40, 1.8, 0.25, 0.22, 4, 3.8],
    "生姜焼き定食": [780, 24.0, 28.0, 8.8, 98.0, 96.5, 1.5, 40, 2.0, 20, 1.1, 0.95, 0.24, 3, 3.2],
    "お刺身定食": [520, 28.0, 8.0, 1.5, 75.0, 74.0, 1.0, 35, 1.8, 30, 2.5, 0.20, 0.25, 5, 2.5],
    "餃子定食": [730, 22.0, 24.0, 6.8, 95.0, 92.5, 2.5, 55, 2.3, 60, 1.2, 0.40, 0.18, 15, 3.4],
    "ステーキ定食": [750, 42.0, 28.0, 9.5, 72.0, 70.0, 2.0, 45, 3.8, 40, 1.5, 0.30, 0.35, 6, 3.5],
    "チキン南蛮定食": [950, 38.0, 45.0, 11.0, 96.0, 93.5, 2.5, 60, 2.4, 150, 2.0, 0.28, 0.32, 8, 4.2],
    "野菜炒め定食": [580, 18.0, 18.0, 3.5, 82.0, 76.0, 6.0, 95, 2.5, 180, 1.8, 0.45, 0.26, 45, 3.2],
    "醤油ラーメン": [500, 22.0, 10.0, 2.5, 75.0, 73.0, 2.0, 25, 1.8, 30, 0.5, 0.15, 0.12, 0, 6.0],
    "とんこつラーメン": [620, 24.0, 22.0, 7.5, 78.0, 76.0, 2.0, 30, 1.9, 15, 0.4, 0.18, 0.15, 0, 6.5],
    "かけそば": [360, 15.0, 2.5, 0.5, 68.0, 64.0, 4.0, 35, 2.2, 0, 0.0, 0.38, 0.10, 0, 4.8],
    "きつねうどん": [420, 14.5, 6.2, 1.2, 69.0, 67.0, 2.0, 65, 1.2, 15, 0.4, 0.10, 0.08, 1, 4.5],
    "パスタ（カルボナーラ）": [750, 20.0, 30.0, 12.0, 85.0, 83.5, 1.5, 110, 1.5, 130, 1.1, 0.14, 0.25, 1, 2.5],
    "パスタ（ミートソース）": [600, 18.0, 15.0, 4.2, 90.0, 86.5, 3.0, 45, 2.8, 95, 2.1, 0.22, 0.18, 14, 2.8],
    "パスタ（ペペロンチーノ）": [530, 11.0, 18.5, 2.5, 76.0, 73.5, 2.5, 22, 1.3, 45, 2.3, 0.12, 0.06, 8, 2.1],
    "ミックスピザ(2ピース)": [480, 18.0, 19.5, 6.5, 54.0, 51.0, 3.0, 240, 1.1, 140, 1.3, 0.14, 0.20, 18, 2.4],
    "味噌汁": [40, 2.5, 1.2, 0.2, 4.5, 3.5, 1.0, 22, 0.5, 15, 0.2, 0.03, 0.04, 3, 1.5],
    "野菜サラダ": [85, 1.2, 6.5, 0.8, 5.0, 2.9, 2.1, 28, 0.6, 54, 1.1, 0.05, 0.06, 25, 0.8],
    "ショートケーキ": [350, 4.5, 22.0, 13.0, 32.0, 31.2, 0.8, 60, 0.4, 90, 0.5, 0.04, 0.12, 2, 0.2]
}

# --- 2. 目標計算関数 ---
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
        db = INGREDIENTS_DB if row["ItemType"] == "食材" else MEALS_DB
        if item in db:
            for i in range(len(NUTRIENT_LABELS)):
                totals[i] += db[item][i] * amount
    return totals

st.title("🥇 パーソナル AI あすけん")
tab1, tab2, tab3 = st.tabs(["👤 プロフィール", "✍ 食事の記録", "📊 履歴・修正・提案シミュレーション"])

# --- TAB 1 ---
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

# --- TAB 2 ---
with tab2:
    st.header("食事を新しく追加する")
    col_d, col_t = st.columns(2)
    r_date = col_d.date_input("日付", datetime.date.today())
    r_time = col_t.selectbox("タイミング", ["朝食", "昼食", "夕食", "間食"])
    
    sel_ing = st.multiselect("🥑 食材から選ぶ", list(INGREDIENTS_DB.keys()))
    sel_meal = st.multiselect("🍛 料理名から選ぶ", list(MEALS_DB.keys()))
    
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
            new_df = pd.DataFrame(save_list)
            df = pd.concat([pd.read_csv(DIET_DETAIL_FILE), new_df], ignore_index=True) if os.path.exists(DIET_DETAIL_FILE) else new_df
            df.to_csv(DIET_DETAIL_FILE, index=False)
            st.success("明細データを保存しました！")

# --- TAB 3 ---
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
        if ("エネルギー (kcal)" in overs or "脂質 (g)" in overs) and any(x in df_day_latest["ItemName"].values for x in ["カレーライス", "かつ丼", "ハンバーグ定食", "から揚げ定食", "チキン南蛮定食", "とんこつラーメン"]):
            for idx, r in df_day_latest.iterrows():
                if r["ItemName"] in ["カレーライス", "かつ丼", "ハンバーグ定食", "から揚げ定食", "チキン南蛮定食", "とんこつラーメン"]:
                    old_item = r["ItemName"]
                    for i in range(len(NUTRIENT_LABELS)):
                        sim_totals[i] -= MEALS_DB[old_item][i] * float(r["Amount"])
                        sim_totals[i] += MEALS_DB["お刺身定食"][i]
                    sim_applied_msg.append(f"・過剰な脂質対策：重い主食『{old_item}』を『お刺身定食』へ置き換え")
                    break
        if "たんぱく質 (g)" in unders:
            for i in range(len(NUTRIENT_LABELS)): sim_totals[i] += INGREDIENTS_DB["サラダチキン(100g)"][i]
            sim_applied_msg.append("・たんぱく質不足対策：『サラダチキン(100g)』を1品追加")
        if "食物繊維 (g)" in unders:
            for i in range(len(NUTRIENT_LABELS)): sim_totals[i] += INGREDIENTS_DB["ブロッコリー(100g)"][i]
            sim_applied_msg.append("・食物繊維不足対策：『ブロッコリー(100g)』を1品追加")
        if "ビタミンC (mg)" in unders:
            for i in range(len(NUTRIENT_LABELS)): sim_totals[i] += INGREDIENTS_DB["トマト(1個)"][i]
            sim_applied_msg.append("・ビタミンC不足対策：『トマト(1個)』を1品追加")
        if "食塩相当量 (g)" in overs:
            sim_totals[14] = max(0.0, sim_totals[14] - 2.0)
            sim_applied_msg.append("・塩分過剰対策：ラーメンのスープ残し等で『塩分を2gカット』")

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
        
        # --- 📊 Plotlyによる爆速日本語対応グループ化横棒グラフ ---
        fig = go.Figure()
        
        # 現在の食事（条件分岐カラーを1本ずつ反映）
        fig.add_trace(go.Bar(
            y=df_comp["栄養素"],
            x=df_comp["現在達成率(%)"],
            name="現在の食事",
            orientation='h',
            marker_color=graph_colors,
            hovertemplate="栄養素: %{y}<br>現在達成率: %{x}%<extra></extra>"
        ))
        
        # 提案反映後（オレンジ固定）
        fig.add_trace(go.Bar(
            y=df_comp["栄養素"],
            x=df_comp["提案反映後達成率(%)"],
            name="AI提案を反映した場合",
            orientation='h',
            marker_color="#FFA726",
            hovertemplate="栄養素: %{y}<br>提案後達成率: %{x}%<extra></extra>"
        ))
        
        # レイアウト調整
        fig.update_layout(
            barmode='group',
            height=600,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(title="目標に対する割合 (%)", range=[0, max(max(df_comp["現在達成率(%)"].max(), df_comp["提案反映後達成率(%)"].max()) + 20, 130)]),
            yaxis=dict(autorange="reversed") # 上からエネルギー順にする
        )
        # 100%の目標ラインを引く
        fig.add_vline(x=100, line_width=2, line_dash="dash", line_color="gray")
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 💡 AI栄養士からのアドバイスシミュレーション")
        if sim_applied_msg:
            st.info("上記のオレンジ色の棒は、以下の提案メニューを実際に適用・トレードした後の**『改善予測値』**です！")
            for msg in sim_applied_msg:
                st.markdown(msg)
        else:
            st.success("🎉 現在のままで完璧な栄養バランスです！シミュレーションの必要はありません。")
            
        st.subheader("📋 詳細数値一覧")
        st.dataframe(df_comp, use_container_width=True)
    else:
        st.info("新しい明細形式での食事故歴がまだありません。「食事の記録」から新しく登録してください。")