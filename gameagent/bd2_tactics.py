"""Transparent one-turn damage estimator for user-supplied, verified stats.
Fractions, not percentages (0.5 means 50%). Not a full game simulator.
"""
from dataclasses import dataclass,asdict
from itertools import permutations
from math import isfinite

@dataclass(frozen=True)
class Skill:
    character:str
    costume:str
    attack:float
    multiplier:float
    hits:int
    sp:int
    damage_type:str="physical"
    crit_rate:float=0
    crit_bonus:float=0
    attack_buff:float=0
    defense:float=0
    vulnerability:float=0
    property_bonus:float=0
    reduction:float=0
    resist:float=0
    weak_point:float=0
    chain_bonus:float=0
    def __post_init__(self):
        if not self.character.strip() or not self.costume.strip():raise ValueError("Character and costume required")
        if self.damage_type not in ("physical","magic"):raise ValueError("Unsupported damage type")
        if type(self.hits)!=int or not 1<=self.hits<=100 or type(self.sp)!=int or not 0<=self.sp<=100:raise ValueError("Invalid hits or SP")
        for key,value in asdict(self).items():
            if key in ("character","costume","damage_type"):continue
            if not isinstance(value,(int,float)) or not isfinite(value) or value<0:raise ValueError("Invalid "+key)
        for key in ("crit_rate","defense","reduction","resist"):
            if getattr(self,key)>1:raise ValueError("Invalid fraction "+key)

def estimate(skill,chain=0):
    if type(chain)!=int or chain<0:raise ValueError("Invalid chain")
    base=skill.attack*skill.multiplier*(1+skill.attack_buff)*(1+skill.crit_rate*skill.crit_bonus)
    base*= (1-skill.defense)*(1+skill.vulnerability)*(1+skill.property_bonus)*(1-skill.reduction)*(1-skill.resist)*(1+skill.weak_point)
    return sum(base*(1+(0.1+skill.chain_bonus)*(chain+i)) for i in range(skill.hits))

def optimize(skills,sp,slots=5):
    """Exact enumeration for <=10 candidate skills, one target/turn, no buffs changing mid-turn."""
    if type(sp)!=int or sp<0 or not 1<=slots<=5 or len(skills)>10:raise ValueError("Max 10 candidates; valid SP and 1-5 slots required")
    best={"damage":0.0,"sp_used":0,"order":[]}
    for count in range(1,min(slots,len(skills))+1):
        for seq in permutations(skills,count):
            if len({s.character.casefold() for s in seq})!=count:continue
            cost=sum(s.sp for s in seq)
            if cost>sp:continue
            chain=0;damage=0.0
            for s in seq:
                damage+=estimate(s,chain);chain+=s.hits
            if (damage,-cost)>(best["damage"],-best["sp_used"]):
                best={"damage":damage,"sp_used":cost,"order":[{"character":s.character,"costume":s.costume} for s in seq]}
    return best
