from deal.algo1 import cal1
from deal.algo2 import cal2
from deal.algo3 import cal3
from deal.algo4 import cal4

msg = 0
while True:
    try:
        # 选择输入数字1-4运行不同的降维算法
        msg = int(input("请选择输入数字1-4运行不同的降维算法：\n"))
        break
    except ValueError:
        print("输入错误，请重新输入")
        continue
if msg == 1:
    cal1()
elif msg == 2:
    cal2()
elif msg == 3:
    cal3()
elif msg == 4:
    cal4()
else:
    print("输入错误，请重新输入")