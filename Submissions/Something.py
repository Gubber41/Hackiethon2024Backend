# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
SECONDARY_SKILL = Hadoken

#constants, for easier move return
#movements
JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)
CANCEL = ("skill_cancel", )

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = SECONDARY,
moves_iter = iter(moves)

# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        self.time = 0
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        self.time += 1
        
        if get_secondary_skill(enemy) == "hadoken":
            try:
                if abs(get_proj_pos(enemy_projectiles[0])[0] - get_pos(player)[0]) <= 2:
                    if not primary_on_cooldown:
                        return PRIMARY
                    return JUMP_FORWARD
            except IndexError:
                pass

        if get_pos(player)[0] == 15:
            return JUMP_FORWARD
        
        if get_pos(player)[0] == 0:
            return JUMP_FORWARD
        
        if get_distance(player, enemy) == 1:
            if get_stun_duration(enemy) > 0:
                return heavy_combo(player, enemy)
            if self.time % 15 == 0:
                return BACK
            return BLOCK

        if not secondary_on_cooldown(player):
            if get_distance(player, enemy) < 3:
                return BACK
            return SECONDARY
        
        
        if not primary_on_cooldown(player):
            if get_distance(player, enemy) < 6:
                return PRIMARY
            return FORWARD
        
        
        
        return JUMP_BACKWARD

        
