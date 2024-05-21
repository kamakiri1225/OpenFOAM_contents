# 必要なライブラリのインポート
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import os

# 計算結果が保存されているディレクトリを指定
resultDir = Path("postProcessing/sample")  
latestTime = os.listdir(resultDir)[0]
sampleData = resultDir / latestTime

# サンプルデータフォルダ内のファイルリストを取得
caseList = os.listdir(sampleData)

'''
理論式に基づく計算:
半径をメートル単位で指定 (10mm = 0.01m)
'''
Radius = 10 / 1000  # 半径をメートル単位で設定
ub = 0.2  # 断面平均速度 (流入速度 0.1 m/s)
y = np.arange(0, Radius, 0.01 / 1000)
uz = np.arange(0, ub, 0.01 / 1000)

# 理論式による動径位置の計算
rp = Radius * (1 - (uz / ub))**0.5
rm = -Radius * (1 - (uz / ub))**0.5

# 抽出対象のサブストリングリスト
substrings = ["0.001m", "0.4m", "0.6m"]

# 条件に一致するファイル名を抽出
filtered_cases = [item for item in caseList if any(sub in item for sub in substrings)]

# ["0.001m", "0.4m", "0.6m"]の順に並ぶようにソート
filtered_cases = sorted(filtered_cases, key=lambda x: substrings.index(next(sub for sub in substrings if sub in x)))

# グラフ設定
fig, axes = plt.subplots(1, 3, figsize=(22, 8), tight_layout=True)

for i, zCase in enumerate(filtered_cases):
    # OpenFOAMのデータをDataFrameとして読み込み
    df_data = pd.read_table(
                            sampleData / zCase, 
                            index_col=False, 
                            names=('y[m]', 'Ux[m/s]', 'Uy[m/s]', 'Uz[m/s]')
                            )

    # データのプロット (散布図)
    axes[i].scatter(
                    df_data["Uz[m/s]"], # x軸
                    df_data["y[m]"],    # y軸
                    facecolors='white', # 内部の色を白
                    edgecolors='black', # 枠線の色を黒
                    linewidths=2,       # 枠線の幅
                    s=100,              # マーカーサイズ
                    label="OpenFOAM"    # 凡例
                    )

    # 理論曲線のプロット
    axes[i].plot(uz, rp, color="green", label="Theory")
    axes[i].plot(uz, rm, color="green")

    # 軸ラベルと目盛りの設定
    axes[i].set_ylabel("y[m]", fontsize=24)
    axes[i].set_xlabel("Uz[m/s]", fontsize=24)
    axes[i].set_xticks(np.arange(0, 0.21, 0.02))
    axes[i].set_yticks(np.arange(-0.01, 0.011, 0.002))
    axes[i].tick_params(axis='x', labelsize=16)
    axes[i].tick_params(axis='y', labelsize=16)
    axes[i].tick_params(axis='x', labelsize=16, rotation=90)  # X軸のラベルを縦向きに設定

    # 凡例とグリッドの設定
    if i >= 2:
        plt.legend(loc="upper center",bbox_to_anchor=(1.0, 1.2), fontsize=16)
        
    # グラフタイトルの設定
    axes[i].set_title(f"z={zCase.split('_')[1]}", fontsize=20)
    
    # グリッド
    axes[i].grid()
# グラフをPDFファイルとして保存
plt.savefig("python_plot/result/multiplot_py.pdf", bbox_inches='tight')