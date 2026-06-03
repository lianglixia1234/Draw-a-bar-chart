import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# =========================
# 页面设置
# =========================
st.set_page_config(page_title="Flicker Plot Tool", layout="centered")
st.title("📊 Score Visualization Tool")

# =========================
# 上传 Excel
# =========================
uploaded_file = st.file_uploader("📁上传 Excel 文件", type=["xlsx"])

# =========================
# 所有参数（用户输入）
# =========================
st.sidebar.header("📌 图表参数设置")

Y_MIN = st.sidebar.number_input("Y轴最小值", value=1)
Y_MAX = st.sidebar.number_input("Y轴最大值", value=7)

TITLE = st.sidebar.text_input(
    "图表标题",
    value="The flicker scores of the online version and special version"
)

Y_LABEL = st.sidebar.text_input(
    "Y轴标题",
    value="Flickering sensation"
)

st.sidebar.header("评分说明（1-7）")

score_1 = st.sidebar.text_input("1分说明", "Very noticeable flicker")
score_2 = st.sidebar.text_input("2分说明", "")
score_3 = st.sidebar.text_input("3分说明", "")
score_4 = st.sidebar.text_input("4分说明", "")
score_5 = st.sidebar.text_input("5分说明", "")
score_6 = st.sidebar.text_input("6分说明", "")
score_7 = st.sidebar.text_input("7分说明", "No noticeable flicker")



score_text = [
    f"1 = {score_1}",
    f"2 = {score_2}",
    f"3 = {score_3}",
    f"4 = {score_4}",
    f"5 = {score_5}",
    f"6 = {score_6}",
    f"7 = {score_7}",
]
# =========================
# 主逻辑
# =========================
if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    st.write("### 📄 数据预览")
    st.dataframe(df)

    conditions = df.columns.tolist()

    means = df.mean()
    sds = df.std()
    maxs = df.max()
    mins = df.min()

    colors = plt.cm.Blues(np.linspace(0.45, 0.85, len(conditions)))

    fig, ax = plt.subplots(figsize=(8, 6))
    x = np.arange(len(conditions))

    # =========================
    # bar + error
    # =========================
    ax.bar(
        x,
        means,
        yerr=sds,
        width=0.3,
        capsize=8,
        color=colors,
        edgecolor="black",
        linewidth=1.2
    )

    # mean points
    ax.scatter(x, means, color="black", s=70)

    # mean labels
    for i, mean in enumerate(means):
        ax.text(i + 0.05, mean, f"{mean:.2f}", fontsize=10)

    # max/min lines
    for i in range(len(conditions)):
        ax.hlines(maxs.iloc[i], i-0.25, i+0.25, colors="blue", linestyles="--")
        ax.hlines(mins.iloc[i], i-0.25, i+0.25, colors="lightblue", linestyles="--")

    # =========================
    # axes settings
    # =========================
    ax.set_ylim(Y_MIN, Y_MAX + 0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(conditions, rotation=0)

    ax.set_ylabel(Y_LABEL)
    ax.set_title(TITLE)

    ax.text(
        0.98, 0.98,
        SCORE_MEANING,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=10
    )

    legend_text = "\n".join(score_text)

    ax.text(
        1.05, 0.5,                 # 图右侧位置（关键）
        legend_text,
        transform=ax.transAxes,
        va="center",
        ha="left",
        fontsize=10,
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor="white",
            edgecolor="black",
            alpha=0.9
        )
    )
    

    ax.grid(axis="y", linestyle=":", alpha=0.4)

    st.pyplot(fig)

    # =========================
    # 下载 PNG
    # =========================
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")

    st.download_button(
        label="📥 下载PNG图片",
        data=buf.getvalue(),
        file_name="flicker_plot.png",
        mime="image/png"
    )

else:
    st.info("请先上传 Excel 文件")
