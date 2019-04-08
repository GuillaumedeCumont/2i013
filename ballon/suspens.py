from .socceria import QStrategy
from .code_alea import QLearning
#Strategy
QTestStrategy=QStrategy()
QTestStrategy.add('right',SimpleStrategy(shoot_right,''))
QTestStrategy.add('left',SimpleStrategy(shoot_left,''))
QTestStrategy.add('up',SimpleStrategy(shoot_up,''))
QTestStrategy.add('down',SimpleStrategy(shoot_down,''))
#Learning
expe=QLearning(strategy=QTestStrategy,monte_carlo=False)
expe.start(fps=1500)

with open('qstrategy.pkl','wb') as fo:
    QTestStrategy.qtable = expe.qtable
    pkl.dump( QTestStrategy , fo )
# Test
with open ('qstrategy.pkl.351','rb') as fi :
    QStrategy = pkl.load(fi)
    # Simulate and display the match
    simu = RandomPos(QStrategy)
    simu.start()

        
        







        