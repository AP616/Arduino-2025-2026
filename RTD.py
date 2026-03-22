import pyfirmata
import time
from jupyterplot import ProgressPlot
board = pyfirmata.Arduino('COM3')

it = pyfirmata.util.Iterator(board)
it.start()

board.analog[0].enable_reporting()
board.analog[1].enable_reporting()

#initial settings
Vi = 5
Rc = R2 = R3 = 988
Vadc = 5
Tref = 0
Rref = 1009
alpha = 0.00385

pp = ProgressPlot(plot_names = ['RTD temperature, Tu (°C)'], line_names = ['Tu'], line_colors = ['blue'], x_label = 'time (s)', x_iterator = False)
t= 0

while True:
  #obtain readings and do the calculations
    Vu = Vi - board.analog[0].read() * Vadc
    Vc = Vi - board.analog[1].read()*Vadc
    V0 = Vu - Vc
    Ru = (V0/Vi + Rc/(Rc+R2)/(1-(V0/Vi+Rc/(Rc+R2))))*R3
    Ru=round(Ru,2)
    print(Ru)
    Tu=((Ru/Rref-1)/alpha)+Tref
    Tu=round(Tu,2)
    time.sleep(60)
    t=t+1
    pp.update(t,Tu)
    lines=[str(t),str(Tu)]
    print(str(t), str(Tu))
    with open ('Trial5water.txt','a') as f:
        output_line = '\t'.join(lines) + '\n'
        f.writelines(output_line)
    if t == 360:
        break
