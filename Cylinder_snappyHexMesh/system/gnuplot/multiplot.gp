set terminal pdf enhanced size 30cm ,15cm color solid font "Arial,24"
set output "gnuplot/result/multiplot.pdf"

set tmargin at screen 0.8
set multiplot layout 1,3
set ytics 0.001
set xrange[0:0.2]
set yrange[-0.01:0.01]
set grid
set key at 0.2, 0.015

R=0.01
rp(x)=R*(1-(x/0.2) )**0.5
rm(x)=-R*(1-(x/0.2) )**0.5
#uz(x)=0.2*(1-(x/R)**2)

set ylabel "r[m]"
set xlabel "uz[m/s]"


fnames=system("/bin/ls ./postProcessing/sample")

set title "z=0.001m"
plot \
     rp(x) notitle with line lw 3 lt 2,\
     rm(x) notitle with line lw 3 lt 2,\
      "postProcessing/sample/".fnames."/z_0.001m_U.xy" using 4:1 notitle lt 8 pt 6

set title "z=0.4m"
plot \
     rp(x) notitle with line lw 3 lt 2,\
     rm(x) notitle with line lw 3 lt 2,\
     "postProcessing/sample/".fnames."/z_0.4m_U.xy" using 4:1 notitle lt 8 pt 6

set title "z=0.6m"
plot \
     rp(x) with line lw 3 lt 2 title "theory",\
     rm(x) notitle with line lw 3 lt 2,\
     "postProcessing/sample/".fnames."/z_0.6m_U.xy" using 4:1 title "OpenFOAM laminar" lt 8 pt 6

unset multiplot
reset