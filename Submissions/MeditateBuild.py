# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = Meditate
SECONDARY_SKILL = BearTrap

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

def anydodgers(player, enemy, enemy_projectiles):
    if get_secondary_skill(enemy) == "hadoken" or get_secondary_skill(enemy) == "grenade":
        try:
            if abs(get_proj_pos(enemy_projectiles[0])[0] - get_pos(player)[0]) <= 2:
                return JUMP_FORWARD
            
        except IndexError:
            return
        
    if get_secondary_skill(enemy) == "boomerang":
        try:
            if abs(get_proj_pos(enemy_projectiles[0])[0] - get_pos(player)[0]) <= 2:
                return JUMP_BACKWARD
            
        except IndexError:
            return
    return
               
def vsMeditate(time, player, enemy, enemy_projectiles):
    distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
    if anydodgers(player, enemy, enemy_projectiles) == JUMP_FORWARD:
        return JUMP_FORWARD
    if not primary_on_cooldown(player) and get_hp(player) <= 80:
        return PRIMARY
    if distance > 2:
        return JUMP_FORWARD
    if distance == 1:
        return heavy_combo(player, enemy)
    if not secondary_on_cooldown(player):
        if get_distance(player, enemy) <= 7:
            return SECONDARY
        else: 
            return FORWARD
    return FORWARD
def vsTeleport(time, player, enemy, enemy_projectiles):
    distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
    if not primary_on_cooldown(player) and get_hp(player) <= 80:
        return PRIMARY
    if distance > 2:
        return JUMP_FORWARD
    if distance == 1:
        return heavy_combo(player, enemy)
    if not secondary_on_cooldown(player):
        if get_distance(player, enemy) <= 7:
            return SECONDARY
        else: 
            return FORWARD
    return FORWARD
def vsDashAttack(time, player, enemy, enemy_projectiles):
    if time%50 == 0:
        return BACK
    distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
    if anydodgers(player, enemy, enemy_projectiles) == JUMP_FORWARD:
        return JUMP_FORWARD
    if not primary_on_cooldown(player) and get_hp(player) <= 80:
        return PRIMARY
    if get_stun_duration(enemy) > 0 and distance == 1:
        return heavy_combo(player, enemy)
    if distance == 1 and get_block_status(player) > 0:
        return BLOCK
    if distance <= 2:
        return heavy_combo(player, enemy)
    if not secondary_on_cooldown(player):
        if distance <= 7:
            return SECONDARY
        else: 
            return FORWARD
    return FORWARD
def vsUppercut(time, player, enemy, enemy_projectiles):
    if time%50 == 0:
        return BACK
    distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
    if anydodgers(player, enemy, enemy_projectiles) == JUMP_FORWARD:
        return JUMP_FORWARD
    if not primary_on_cooldown(player) and get_hp(player) <= 80:
        return PRIMARY
    if get_stun_duration(enemy) > 0 and distance == 1:
        return heavy_combo(player, enemy)
    if distance == 1:
        return BLOCK
    if not secondary_on_cooldown(player):
        if get_distance(player, enemy) <= 7:
            return SECONDARY
        else: 
            return FORWARD
    return FORWARD
def vsOnePunch(time, player, enemy, enemy_projectiles):
    distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
    if not primary_on_cooldown(player) and get_hp(player) <= 80:
        return PRIMARY
    if get_stun_duration(enemy) > 0 and distance == 1:
        return heavy_combo(player, enemy)
    if distance == 1:
        return BLOCK
    if not secondary_on_cooldown(player):
        if get_distance(player, enemy) <= 7:
            return SECONDARY
        else: 
            return FORWARD
    return FORWARD



# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        self.time = 0
        self.time_since_meditate = 0 
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        self.time += 1
        if self.time > 1:  
            if get_last_move(player)[0] == "meditate":
                self.time_since_meditate = 0
        self.time_since_meditate += 1
        if self.time_since_meditate >= 40 and get_hp(player) < 100:
            return PRIMARY
        opp = get_primary_skill(enemy)
        if opp == "meditate":
            return vsMeditate(self.time, player, enemy, enemy_projectiles)
        if opp == "teleport":
            return vsTeleport(self.time, player, enemy, enemy_projectiles)
        if opp == "dash_attack":
            return vsDashAttack(self.time, player, enemy, enemy_projectiles)
        if opp == "uppercut":
            return vsUppercut(self.time, player, enemy, enemy_projectiles)
        if opp == "onepunch":
            return vsOnePunch(self.time, player, enemy, enemy_projectiles)