from ..controllers.BotBase import BotController
from ..Translate import *
from ..Constants import Direction

class Forager(BotController):
    def act(self):
        ctx = self.ctx
        
        if(ctx.getAlgaeHeld()>=5):
            pos = ctx.getNearestBank()
            dir = ctx.moveTarget(pos,ctx.getLocation())
            return move(ctx.getID(),dir)
        
        visible = ctx.senseAlgae()+ctx.senseSacraps()
        if visible:
            return harvest(ctx.getID(), visible[0]);
        i=2;
        while(i<=10):
            visible = ctx.senseAlgae(radius=i)+ctx.senseSacraps(radius=i)
            if visible:
                dir=ctx.moveTarget(visible[0].location,ctx.getLocation())
                return move(ctx.getID(),dir)
            i+=1
                
        
        