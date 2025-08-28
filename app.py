import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, norm

# ------------------------------
# matplotlib 日本語対応
# ------------------------------
plt.rcParams["font.family"] = "Yu Gothic"
plt.rcParams["axes.unicode_minus"] = False

# ------------------------------
# タイトル（バージョン管理）
# ------------------------------
st.title("確率分布シミュレーター ver1.000")

# ------------------------------
# 入力欄（デフォルト値）
# ------------------------------
n1_str = st.text_input("確率分母", "319.7")
try:
    n1 = float(n1_str)
    if n1 <= 0:
        st.warning("確率分母は0より大きい値を入力してください")
        n1 = 319.7
except ValueError:
    st.warning("有効な数字を入力してください")
    n1 = 319.7

n2 = st.number_input("回転数（ゲーム数）", min_value=1, value=320, step=1)
n3 = st.number_input("当たり回数", min_value=0, value=1, step=1)

# 整数化
n = int(n2)
k = int(n3)

# ------------------------------
# 確率計算
# ------------------------------
p = 1.0 / n1

# 二項分布で「ちょうど k 回」の確率
prob_exact = binom.pmf(k, n, p)

# P(X < k) = P(X <= k-1)
if k > 0:
    cdf_below_k = binom.cdf(k - 1, n, p)
else:
    cdf_below_k = 0.0

# 上側: P(X >= k) = 1 - P(X <= k-1)
cdf_ge_k = 1.0 - cdf_below_k

# 上位 / 下位（合計 ≒ 100%）
upper_percent = 100.0 * cdf_ge_k
lower_percent = 100.0 * cdf_below_k

# 小さい方（表示・頻度計算に使う）
if upper_percent < lower_percent:
    small_label = "上位"
    small_percent = upper_percent
else:
    small_label = "下位"
    small_percent = lower_percent

# 「この事象は◯回に1回」の計算（小さい方の逆数、制限なし）
if small_percent > 0:
    one_in_x = 100.0 / small_percent
else:
    one_in_x = float("inf")

# ------------------------------
# 表示用の文字列（理論値/実践値）
# ------------------------------
def fmt_trim(x: float) -> str:
    return f"{x:.2f}".rstrip("0").rstrip(".")

theoretical_str = f"1/{fmt_trim(n1)}"
if k == 0:
    practical_str = "0"
else:
    practical_str = f"1/{fmt_trim(n / k)}"  # 実践値は 1/(n/k)

# ------------------------------
# 結果表示
# ------------------------------
st.subheader("計算結果")
st.write(f"理論値　　{theoretical_str}　　　実践値　　{practical_str}")
st.write(f"二項分布による確率: {prob_exact * 100:.4f}%")
st.write(f"この事象は上位 {upper_percent:.2f}%、下位 {lower_percent:.2f}% に位置します。")
if math.isfinite(one_in_x):
    st.write(f"この事象はおよそ {one_in_x:.2f} 回に1回の確率です。")
else:
    st.write("この事象はほぼ起こりません。")

# ------------------------------
# 正規近似（グラフ用）
# ------------------------------
mu = n * p
sigma = math.sqrt(n * p * (1 - p))

st.subheader("正規分布近似グラフ")

# 描画範囲
x_min = max(0, mu - 4 * sigma)
x_max = mu + 4 * sigma
x_vals = np.linspace(x_min, x_max, 500)
y_vals = norm.pdf(x_vals, mu, sigma)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x_vals, y_vals, color="blue", linewidth=2, label="正規分布近似")

# 小さい方だけを塗る（表示に合わせる）
if small_label == "下位":
    # 下側を赤で塗る（x <= k）
    x_fill = np.linspace(x_min, min(k, x_max), 500)
    y_fill = norm.pdf(x_fill, mu, sigma)
    ax.fill_between(x_fill, y_fill, color="salmon", alpha=0.6)
else:
    # 上側を水色で塗る（x >= k）
    x_fill = np.linspace(max(k, x_min), x_max, 500)
    y_fill = norm.pdf(x_fill, mu, sigma)
    ax.fill_between(x_fill, y_fill, color="skyblue", alpha=0.6)

# 当たり回数の縦線（緑）
ax.axvline(k, color="green", linestyle="--", linewidth=2, label=f"当たり回数={k}")

# ラベル・スタイル
ax.set_xlabel("当たり回数", fontweight="bold")
ax.set_ylabel("確率", fontweight="bold")
ax.set_title("正規分布近似", fontweight="bold")
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)

# ------------------------------
# 作成者クレジット
# ------------------------------
st.markdown("---")
st.markdown("作成者: Sigma")
