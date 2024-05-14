# 定数の定義
R = 0.01
# 速度分布の理論式
uz(x) = 0.2 * (1 - (x/R)**2)
zp(x) = R * (1 - (x/0.2))**0.5
zm(x) = -R * (1 - (x/0.2))**0.5

# ラベルの設定
set ylabel "r [m]"
set xlabel "uz [m/s]"

# ファイル名を取得
fnames = system("/bin/ls ./postProcessing/sample")

# プロットの設定
# 'using'句で4番目のデータをx軸に、1番目のデータをy軸に設定
plot "postProcessing/sample/".fnames."/z_0.15m_U.xy" using 4:1 title "OpenFOAM laminar" lt 8 pt 2, zp(x) title "theory" with line lw 3 lt 2, zm(x) notitle with line lw 3 lt 2
