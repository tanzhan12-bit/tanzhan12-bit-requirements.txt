import math
from typing import Dict, List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

try:
    import streamlit as st
except ModuleNotFoundError:
    st = None


DEPOSITS: List[Dict] = [
    {"bank": "Евразийский Банк", "product": "Turbo Deposit", "type": "Теңгедегі мерзімсіз депозит", "topup": "Жоқ", "guarantee_mln": 10, "rate": 15.3, "K": 1.00, "Q": 1.02, "R": 0.05},
    {"bank": "Евразийский Банк", "product": "Turbo Deposit Казпочта", "type": "Теңгедегі мерзімсіз депозит", "topup": "Жоқ", "guarantee_mln": 10, "rate": 15.3, "K": 1.00, "Q": 1.01, "R": 0.05},
    {"bank": "Евразийский Банк", "product": "Turbo Deposit Накопительный без права пополнения", "type": "Теңгедегі жинақ депозиті", "topup": "Жоқ", "guarantee_mln": 20, "rate": 15.3, "K": 1.03, "Q": 0.96, "R": 0.06},
    {"bank": "Евразийский Банк", "product": "Turbo Deposit Накопительный с правом пополнения", "type": "Теңгедегі жинақ депозиті", "topup": "Иә", "guarantee_mln": 20, "rate": 15.3, "K": 1.03, "Q": 1.05, "R": 0.05},
    {"bank": "БЦК", "product": "Чемпион", "type": "Теңгедегі мерзімсіз депозит", "topup": "Жоқ", "guarantee_mln": 10, "rate": 15.3, "K": 1.02, "Q": 1.00, "R": 0.05},
    {"bank": "БЦК", "product": "Моя цель", "type": "Теңгедегі мерзімді депозит", "topup": "Иә", "guarantee_mln": 10, "rate": 15.3, "K": 1.02, "Q": 1.03, "R": 0.05},
    {"bank": "БЦК", "product": "Рахмет", "type": "Теңгедегі жинақ депозиті", "topup": "Жоқ", "guarantee_mln": 20, "rate": 15.3, "K": 1.03, "Q": 0.97, "R": 0.05},
    {"bank": "Нурбанк", "product": "Нур Алтын Оптимальный", "type": "Теңгедегі мерзімсіз депозит", "topup": "Жоқ", "guarantee_mln": 10, "rate": 15.3, "K": 0.98, "Q": 1.00, "R": 0.06},
    {"bank": "Хоум Кредит Банк", "product": "Простой", "type": "Теңгедегі мерзімсіз депозит", "topup": "Жоқ", "guarantee_mln": 10, "rate": 15.3, "K": 0.97, "Q": 1.00, "R": 0.06},
    {"bank": "Bereke Bank", "product": "Гибкий", "type": "Теңгедегі мерзімсіз депозит", "topup": "Жоқ", "guarantee_mln": 10, "rate": 15.3, "K": 1.01, "Q": 1.05, "R": 0.05},
    {"bank": "Банк ВТБ", "product": "Комфортный", "type": "Теңгедегі мерзімсіз депозит", "topup": "Жоқ", "guarantee_mln": 10, "rate": 15.3, "K": 0.95, "Q": 1.00, "R": 0.07},
    {"bank": "Халык Банк", "product": "Универсальный", "type": "Теңгедегі мерзімсіз депозит", "topup": "Жоқ", "guarantee_mln": 10, "rate": 15.3, "K": 1.05, "Q": 1.00, "R": 0.04},
    {"bank": "Халык Банк", "product": "Максимальный", "type": "Теңгедегі мерзімді депозит", "topup": "Иә", "guarantee_mln": 10, "rate": 15.3, "K": 1.05, "Q": 1.02, "R": 0.04},
    {"bank": "Kaspi Bank", "product": "Kaspi Депозит", "type": "Теңгедегі мерзімсіз депозит", "topup": "Жоқ", "guarantee_mln": 10, "rate": 15.3, "K": 1.06, "Q": 1.08, "R": 0.04},
    {"bank": "Forte Bank", "product": "Депозит со снятием", "type": "Теңгедегі мерзімсіз депозит", "topup": "Жоқ", "guarantee_mln": 10, "rate": 15.3, "K": 1.02, "Q": 1.06, "R": 0.05},
    {"bank": "Forte Bank", "product": "Депозит без снятия", "type": "Теңгедегі мерзімді депозит", "topup": "Иә", "guarantee_mln": 10, "rate": 15.3, "K": 1.02, "Q": 1.00, "R": 0.05},
    {"bank": "Jusan Bank", "product": "Jusan депозит", "type": "Теңгедегі мерзімсіз депозит", "topup": "Жоқ", "guarantee_mln": 10, "rate": 15.3, "K": 1.00, "Q": 1.01, "R": 0.05},
    {"bank": "Bank RBK", "product": "Депозит Dream", "type": "Теңгедегі мерзімді депозит", "topup": "Иә", "guarantee_mln": 10, "rate": 15.3, "K": 0.99, "Q": 1.03, "R": 0.06},
    {"bank": "Altyn Bank", "product": "Золотой Запас", "type": "Теңгедегі мерзімсіз депозит", "topup": "Жоқ", "guarantee_mln": 10, "rate": 15.3, "K": 1.03, "Q": 1.00, "R": 0.05},
    {"bank": "Шинхан Банк", "product": "Береке", "type": "Теңгедегі мерзімсіз депозит", "topup": "Жоқ", "guarantee_mln": 10, "rate": 15.3, "K": 0.97, "Q": 0.99, "R": 0.06},
]


def build_df() -> pd.DataFrame:
    df = pd.DataFrame(DEPOSITS)
    df["label"] = df["bank"] + " — " + df["product"]
    df["guarantee"] = df["guarantee_mln"].astype(str) + " млн ₸"
    return df


BASE_DF = build_df()


def calc_model(row: pd.Series, amount: float, years: int) -> pd.Series:
    if amount <= 0:
        raise ValueError("amount must be positive")
    if years < 1:
        raise ValueError("years must be at least 1")

    s = amount * math.pow(1 + float(row["rate"]) / 100, int(years))
    m = (s / amount) * float(row["K"]) * float(row["Q"]) - float(row["R"])
    profit = s - amount
    return pd.Series({"S": s, "profit": profit, "M": m})



def format_money(value: float) -> str:
    return f"{value:,.0f} ₸".replace(",", " ")



def filter_deposits(df: pd.DataFrame, search: str = "", type_filter: str = "Барлығы", topup_filter: str = "Барлығы") -> pd.DataFrame:
    filtered = df.copy()
    if search:
        mask = filtered["bank"].str.contains(search, case=False, na=False) | filtered["product"].str.contains(search, case=False, na=False)
        filtered = filtered[mask]
    if type_filter != "Барлығы":
        filtered = filtered[filtered["type"] == type_filter]
    if topup_filter != "Барлығы":
        filtered = filtered[filtered["topup"] == topup_filter]
    return filtered.reset_index(drop=True)



def calculate_comparison(selected_labels: List[str], amount: float, years: int, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    source_df = BASE_DF if df is None else df
    selected_df = source_df[source_df["label"].isin(selected_labels)].copy()
    if selected_df.empty:
        raise ValueError("At least one valid deposit must be selected")

    metrics = selected_df.apply(calc_model, axis=1, amount=amount, years=years)
    selected_df[["S", "profit", "M"]] = metrics
    return selected_df.sort_values("M", ascending=False).reset_index(drop=True)



def make_bar_chart(viz_df: pd.DataFrame, y: str, title: str):
    color_sequence = ["#2e7d32", "#66bb6a", "#a5d6a7"]
    fig = px.bar(
        viz_df,
        x="label",
        y=y,
        text_auto=".3f" if y == "M" else ".0f",
        title=title,
        color="label",
        color_discrete_sequence=color_sequence,
    )
    fig.update_traces(marker_line_color="#1b5e20", marker_line_width=1.5)
    fig.update_layout(
        xaxis_title="",
        showlegend=False,
        template="plotly_white",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(color="#1a1a1a"),
        title_font=dict(color="#1b5e20", size=20),
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#dfeee2")
    return fig



def make_growth_df(best_row: pd.Series, amount: float) -> pd.DataFrame:
    year_rows = []
    for year in range(1, 6):
        temp = calc_model(best_row, amount, year)
        year_rows.append({"Жыл": f"{year} жыл", "Соңғы сома": temp["S"]})
    return pd.DataFrame(year_rows)


def style_table(df: pd.DataFrame):
    return (
        df.style
        .format({"rate": "{:.1f}%"})
        .set_properties(**{
            "background-color": "#ffffff",
            "color": "#1a1a1a",
            "border": "1px solid #c8e6c9",
        })
        .set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#e8f5e9"),
                ("color", "#1b5e20"),
                ("border", "1px solid #2e7d32"),
                ("font-weight", "600"),
            ]},
            {"selector": "td", "props": [
                ("border", "1px solid #c8e6c9"),
            ]},
            {"selector": "table", "props": [
                ("border-collapse", "collapse"),
                ("width", "100%"),
            ]},
        ])
    )



def run_tests() -> None:
    df = BASE_DF.copy()

    sample = pd.Series({"rate": 10.0, "K": 1.0, "Q": 1.0, "R": 0.0})
    result = calc_model(sample, 100000, 2)
    assert round(result["S"]) == 121000
    assert round(result["profit"]) == 21000
    assert round(result["M"], 3) == 1.210

    assert format_money(1234567) == "1 234 567 ₸"

    filtered = filter_deposits(df, search="Kaspi")
    assert len(filtered) == 1
    assert filtered.iloc[0]["bank"] == "Kaspi Bank"

    filtered_topup = filter_deposits(df, topup_filter="Иә")
    assert len(filtered_topup) >= 1
    assert set(filtered_topup["topup"]) == {"Иә"}

    labels = df["label"].tolist()[:3]
    comparison = calculate_comparison(labels, 100000, 1, df)
    assert len(comparison) == 3
    assert comparison.iloc[0]["M"] >= comparison.iloc[-1]["M"]

    growth_df = make_growth_df(comparison.iloc[0], 100000)
    assert len(growth_df) == 5
    assert growth_df.iloc[0]["Соңғы сома"] < growth_df.iloc[-1]["Соңғы сома"]

    fig = make_bar_chart(comparison[["label", "S", "profit", "M"]], "M", "Тест")
    assert fig.layout.paper_bgcolor == "#ffffff"
    assert fig.layout.plot_bgcolor == "#ffffff"



def render_streamlit_app() -> None:
    st.set_page_config(page_title="DepoSmart KZ 2026", layout="wide")

    # Ақ + жасыл ғылыми дизайн
    st.markdown("""
        <style>
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {
            background: #ffffff !important;
        }

        [data-testid="stSidebar"] {
            background: #f8fcf8 !important;
            border-right: 1px solid #dfeee2;
        }

        [data-testid="stAppViewContainer"] * {
            color: #1a1a1a;
        }

        h1, h2, h3 {
            color: #1b5e20 !important;
            font-weight: 700 !important;
            letter-spacing: 0.2px;
        }

        p, label, .stCaption, .stMarkdown, .stText {
            color: #1a1a1a !important;
        }

        div[data-testid="metric-container"] {
            background: linear-gradient(180deg, #f7fcf8 0%, #eef8f0 100%) !important;
            border: 1px solid #d0e8d8 !important;
            padding: 14px !important;
            border-radius: 14px !important;
            box-shadow: 0 1px 4px rgba(46, 125, 50, 0.06);
        }

        div[data-testid="metric-container"] label,
        div[data-testid="metric-container"] [data-testid="stMetricLabel"],
        div[data-testid="metric-container"] [data-testid="stMetricValue"] {
            color: #1b5e20 !important;
        }

        .stTextInput input,
        .stNumberInput input,
        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div {
            background: #ffffff !important;
            color: #1a1a1a !important;
            border: 1.5px solid #a5d6a7 !important;
            border-radius: 10px !important;
        }

        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stSelectbox div[data-baseweb="select"] > div:focus-within,
        .stMultiSelect div[data-baseweb="select"] > div:focus-within {
            border-color: #2e7d32 !important;
            box-shadow: 0 0 0 1px #2e7d32 !important;
        }

        .stButton > button {
            background: #2e7d32 !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }

        .stButton > button:hover {
            background: #1b5e20 !important;
        }

        .stSlider [data-baseweb="slider"] div[role="slider"] {
            background-color: #2e7d32 !important;
            border-color: #2e7d32 !important;
        }

        .stSlider [data-baseweb="slider"] > div > div {
            background: #c8e6c9 !important;
        }

        .stDataFrame, div[data-testid="stDataFrame"] {
            background: #ffffff !important;
            border: 2px solid #2e7d32 !important;
            border-radius: 14px !important;
            overflow: hidden !important;
        }

        .stAlert {
            background: #e8f5e9 !important;
            border: 1px solid #a5d6a7 !important;
            border-radius: 12px !important;
            color: #1b5e20 !important;
        }

        [data-testid="stExpander"] {
            border: 1px solid #d0e8d8 !important;
            border-radius: 12px !important;
            background: #fcfffc !important;
        }

        hr {
            border-color: #dfeee2 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("DepoSmart KZ 2026")
    st.subheader("Қазақстан депозиттері: банк түрлері, депозит өнімдері және математикалық салыстыру")
    st.caption("Python + Streamlit нұсқасы")

    base_df = BASE_DF.copy()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Қатысушы банктер", base_df["bank"].nunique())
    c2.metric("Депозит өнімдері", len(base_df))
    c3.metric("Ең жоғары кепілдік", "20 млн ₸")
    c4.metric("Орташа мөлшерлеме", f"{base_df['rate'].mean():.1f}%")

    st.markdown("---")

    left, right = st.columns([1.1, 1])

    with left:
        st.header("1. Депозит базасы")
        search = st.text_input("Іздеу", placeholder="Банк атауы немесе өнім атауы")
        type_filter = st.selectbox("Депозит түрі", ["Барлығы"] + sorted(base_df["type"].unique().tolist()))
        topup_filter = st.selectbox("Толықтыру", ["Барлығы", "Иә", "Жоқ"])

        filtered = filter_deposits(base_df, search, type_filter, topup_filter)
        st.dataframe(
            style_table(filtered[["bank", "product", "type", "topup", "guarantee", "rate"]]),
            use_container_width=True,
            hide_index=True,
            height=420,
        )
        st.caption("Бұл тізім оқу жобасы үшін берілді. Нақты шарттарды банктің өзінен тексеру қажет.")

    with right:
        st.header("2. Авторлық формула")
        st.latex(r"S = P \times (1+r)^t")
        st.latex(r"M = (S/P) \times K \times Q - R")
        st.markdown(
            """
**Мұнда:**
- **P** — бастапқы сома
- **r** — жылдық мөлшерлеме
- **t** — жыл саны
- **S** — соңғы сома
- **K** — қауіпсіздік коэффициенті
- **Q** — қолайлылық коэффициенті
- **R** — тәуекел коэффициенті
- **M** — тиімділік индексі
            """
        )
        st.info("Бұл модель пайыз, қауіпсіздік және қолайлылықты бірге ескеріп, депозиттерді кешенді салыстыруға мүмкіндік береді.")

    st.markdown("---")
    st.header("3. Онлайн салыстыру калькуляторы")

    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Бастапқы сома (₸)", min_value=1000, step=1000, value=100000)
    with col2:
        years = st.slider("Мерзім (жыл)", min_value=1, max_value=5, value=1)

    labels = base_df["label"].tolist()
    defaults = labels[:3] if len(labels) >= 3 else labels
    selected_labels = st.multiselect(
        "Салыстыру үшін 2–3 депозит таңдаңыз",
        options=labels,
        default=defaults,
        max_selections=3,
    )

    if len(selected_labels) < 2:
        st.warning("Кемінде 2 депозит таңдаңыз.")
        st.stop()

    calc_df = calculate_comparison(selected_labels, amount, years, base_df)

    st.header("4. Нәтиже")
    cols = st.columns(len(calc_df))
    for idx, (_, row) in enumerate(calc_df.iterrows()):
        with cols[idx]:
            card_color = "#edf7ee" if idx == 0 else "#f8fcf8"
            border_color = "#2e7d32" if idx == 0 else "#c8e6c9"
            st.markdown(f"""
                <div style="background:{card_color}; border:2px solid {border_color}; border-radius:16px; padding:16px; min-height:340px;">
                    <div style="font-size:12px; font-weight:700; color:#1b5e20; margin-bottom:8px;">
                        {'ҰСЫНЫЛАТЫН НҰСҚА' if idx == 0 else 'САЛЫСТЫРУ'}
                    </div>
                    <div style="font-size:20px; font-weight:700; color:#1b5e20;">{row['bank']}</div>
                    <div style="font-size:15px; margin:6px 0 10px 0; color:#1a1a1a;">{row['product']}</div>
                    <div style="font-size:13px; color:#455a45; margin-bottom:12px;">{row['type']} · Толықтыру: {row['topup']} · Кепілдік: {row['guarantee']}</div>
                    <div>Жылдық мөлшерлеме: <b>{row['rate']:.1f}%</b></div>
                    <div>K = <b>{row['K']:.2f}</b></div>
                    <div>Q = <b>{row['Q']:.2f}</b></div>
                    <div>R = <b>{row['R']:.2f}</b></div>
                    <div style="margin-top:10px;">Соңғы сома S = <b>{format_money(row['S'])}</b></div>
                    <div>Таза кіріс = <b>{format_money(row['profit'])}</b></div>
                    <div style="margin-top:10px; font-size:18px; color:#1b5e20;"><b>M = {row['M']:.3f}</b></div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.header("5. Нәтижелерді визуализациялау")

    viz_df = calc_df[["label", "S", "profit", "M"]].copy()

    v1, v2 = st.columns(2)
    with v1:
        fig_s = make_bar_chart(viz_df, "S", "Соңғы сома бойынша салыстыру")
        fig_s.update_layout(yaxis_title="Соңғы сома (₸)")
        st.plotly_chart(fig_s, use_container_width=True)

    with v2:
        fig_m = make_bar_chart(viz_df, "M", "Тиімділік индексі (M) бойынша салыстыру")
        fig_m.update_layout(yaxis_title="M индексі")
        st.plotly_chart(fig_m, use_container_width=True)

    fig_profit = make_bar_chart(viz_df, "profit", "Таза кіріс бойынша салыстыру")
    fig_profit.update_layout(yaxis_title="Таза кіріс (₸)")
    st.plotly_chart(fig_profit, use_container_width=True)

    st.header("6. Уақыт бойынша өсім")
    best_row = calc_df.iloc[0]
    growth_df = make_growth_df(best_row, amount)
    fig_growth = go.Figure()
    fig_growth.add_trace(
        go.Scatter(
            x=growth_df["Жыл"],
            y=growth_df["Соңғы сома"],
            mode="lines+markers",
            line=dict(color="#2e7d32", width=4),
            marker=dict(size=10, color="#66bb6a", line=dict(color="#1b5e20", width=2)),
            fill="tozeroy",
            fillcolor="rgba(102, 187, 106, 0.15)",
            name="Өсім",
        )
    )
    fig_growth.update_layout(
        title=f"Ұсынылған депозиттің уақыт бойынша өсімі: {best_row['bank']} — {best_row['product']}",
        template="plotly_white",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(color="#1a1a1a"),
        title_font=dict(color="#1b5e20", size=20),
        yaxis_title="Соңғы сома (₸)",
        xaxis_title="",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig_growth.update_xaxes(showgrid=False)
    fig_growth.update_yaxes(gridcolor="#dfeee2")
    st.plotly_chart(fig_growth, use_container_width=True)

    st.markdown("---")
    st.header("7. Қорытынды")
    st.markdown(
        f"""
**Ұсынылатын депозит:** **{best_row['bank']} — {best_row['product']}**

Бұл нұсқа таңдалды, себебі оның **M индексі ең жоғары** (**{best_row['M']:.3f}**).
Ол пайыздық өсім, қауіпсіздік коэффициенті және қолайлылық көрсеткіштері бойынша ең жақсы жиынтық нәтиже берді.

- Соңғы сома: **{format_money(best_row['S'])}**
- Таза кіріс: **{format_money(best_row['profit'])}**
- Тиімділік индексі: **{best_row['M']:.3f}**
        """
    )

    with st.expander("Қысқаша техникалық түсіндірме"):
        st.code(
            """# Егер Streamlit орнатылған болса
pip install streamlit pandas plotly
streamlit run deposmart_kz_streamlit.py

# Егер Streamlit орнатылмаған болса
python deposmart_kz_streamlit.py""",
            language="bash",
        )



def render_console_report() -> None:
    print("DepoSmart KZ 2026")
    print("=" * 60)
    print("Streamlit табылмады. Консольдік режим іске қосылды.\n")

    labels = BASE_DF["label"].tolist()[:3]
    amount = 100000
    years = 1
    calc_df = calculate_comparison(labels, amount, years)
    best_row = calc_df.iloc[0]

    print(f"Бастапқы сома: {format_money(amount)}")
    print(f"Мерзім: {years} жыл\n")
    print("Салыстыру нәтижелері:")

    for idx, (_, row) in enumerate(calc_df.iterrows(), start=1):
        print(f"{idx}. {row['bank']} — {row['product']}")
        print(f"   Соңғы сома: {format_money(row['S'])}")
        print(f"   Таза кіріс: {format_money(row['profit'])}")
        print(f"   M индексі: {row['M']:.3f}\n")

    print("Ұсынылатын депозит:")
    print(f"{best_row['bank']} — {best_row['product']}")
    print(f"M = {best_row['M']:.3f}")


if __name__ == "__main__":
    run_tests()
    if st is None:
        render_console_report()
    else:
        render_streamlit_app()
