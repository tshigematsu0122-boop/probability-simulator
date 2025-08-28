import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, norm

# ------------------------------
# matplotlib 日本語対応（Streamlit Cloud向け）
# ------------------------------
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

# ------------------------------
# タイトル
# ------------------------------
st.title("確率分布シミュレーター ver1.002")

# ------------------------------
# 入力欄
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

# ------------------------------
# 計算
# ------------------------------
p = 1 / n1
n = n2
k = n3

# 二項分布確率
prob_exact = binom.pmf(k, n, p)

# 下側累積確率
cdf_lower = binom.cdf(k, n, p)
# 上側累積確率
cdf_upper = binom.sf(k-1, n, p)

# 小さい方の累積確率
cum_prob = min(cdf_lower, cdf_upper)

# 上位/下位％表示（小さい方だけ）
percent = 100 * cum_prob
position_text = f"この事象は上位 {percent:.2f}% に位置します。"

# 「この事象は◯回に1回」の計算（小さい方）
freq = 1 / cum_prob if cum_prob > 0 else float('inf')
freq_text = f"この事象はおよそ {freq:.2f} 回に1回の確率です。"

# 正規分布近似
mu = n * p
sigma = math.sqrt(n * p * (1 - p))

# ------------------------------
# 計算結果表示（理論値／実践値追加）
# ------------------------------
st.subheader("計算結果")

# 理論値
theoretical_str = f"1/{n1:.2f}".rstrip('0').rstrip('.')

# 実践値
if k == 0:
    practical_str = "0"
else:
    practical_str = f"1/{(n/k):.2f}".rstrip('0').rstrip('.')

st.write(f"理論値　　{theoretical_str}　　　実践値　　{practical_str}")
st.write(f"二項分布による確率: {prob_exact*100:.4f}%")
st.write(position_text)
st.write(freq_text)

# ------------------------------
# グラフ描画（色付き、濃く、ラベル太字）
# ------------------------------
st.subheader("正規分布近似グラフ")

x_min = max(0, mu - 4*sigma)
x_max = mu + 4*sigma
x = np.linspace(x_min, x_max, 500)
y = norm.pdf(x, mu, sigma)

fig, ax = plt.subplots(figsize=(8,5))
ax.plot(x, y, color='blue', linewidth=2, label="正規分布近似")

# 塗りつぶし判定（小さい方が50%以下なら塗る）
if cum_prob <= 0.5:
    x_fill = np.linspace(x_min, k, 500)
    y_fill = norm.pdf(x_fill, mu, sigma)
    ax.fill_between(x_fill, y_fill, color='salmon', alpha=0.6)

# 当たり回数の縦線（緑）
ax.axvline(k, color='green', linestyle='--', linewidth=2, label=f"当たり回数={k}")

# ラベル・タイトルを太字
ax.set_xlabel("当たり回数", fontweight='bold')
ax.set_ylabel("確率", fontweight='bold')
ax.set_title("正規分布近似", fontweight='bold')

# 縦横ゼロ固定
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

# ------------------------------
# 作成者クレジット
# ------------------------------
st.markdown("---")
st.markdown("作成者: Sigma")

