"""Evidence-backed F2P planning. Advisory only; no game input or purchase execution."""
from dataclasses import dataclass
from pathlib import Path
import json
from .profiles import ROOT
from .knowledge import Knowledge
from .advisor import advise

@dataclass(frozen=True)
class Account:
    stage: str = "beginner"
    damage: str = "unknown"
    bottleneck: str = "unknown"
    minutes: int = 30
    diamonds: int = 0
    tickets: int = 0
    costumes: str = ""
    goal: str = "story"
    def __post_init__(self):
        if self.stage not in {"beginner","midgame","endgame"}:raise ValueError("Invalid stage")
        if self.damage not in {"physical","magic","unknown"}:raise ValueError("Invalid damage type")
        if self.bottleneck not in {"gear","gold","level","combat","unknown"}:raise ValueError("Invalid bottleneck")
        if self.goal not in {"story","resources","boss","general"}:raise ValueError("Invalid goal")
        if not 1<=self.minutes<=1440 or min(self.diamonds,self.tickets)<0:raise ValueError("Invalid resources")

def seed():
    notes=json.loads((ROOT/"brown_dust_2"/"expert_seed.json").read_text(encoding="utf-8"))
    db=Knowledge("brown_dust_2")
    try:return sum(db.ingest(**n) for n in notes)
    finally:db.close()

def plan(account):
    """Heuristic priority order, not a mathematically proven optimum."""
    result=[]
    def add(title,reason,score,time):
        result.append(dict(title=title,reason=reason,priority=score,minutes=time))
    add("Vérifier les récompenses gratuites et échéances","Confirmer les événements actifs dans le client ou les annonces officielles.",100,5)
    add("Réserver les diamants","Aucun achat réel ; vérifier le rendement et les alternatives avant toute invocation.",99,0)
    if account.stage=="beginner":
        add("Avancer dans les packs histoire","Débloquer les systèmes et obtenir des ressources plutôt que disperser les investissements.",85 if account.goal=="story" else 65,15)
    if account.damage=="physical":
        add("Évaluer Arines et les soutiens possédés","Soutien physique accessible ; vérifier le costume et les synergies réelles.",80,5)
    elif account.damage=="magic":
        add("Évaluer les soutiens magiques possédés","Ne pas appliquer une composition physique à une équipe magique.",80,5)
    else:
        add("Identifier les costumes et leur type de dégâts","Impossible de calculer une équipe optimale sans inventaire.",90,5)
    reasons={"gear":("Améliorer les équipements utiles","Prioriser les pièces des attaquants utilisés et vérifier le coût des matériaux."),
             "gold":("Rechercher les sources gratuites d'or","Évaluer le coût des améliorations et les récompenses actuelles."),
             "level":("Concentrer les ressources de niveau","Investir dans une équipe utilisée régulièrement."),
             "combat":("Analyser le combat bloquant","Comparer zones, ordre des compétences et soutiens avant de changer d'équipe."),
             "unknown":("Identifier le principal blocage","Éviter les dépenses non justifiées.")}
    title,reason=reasons[account.bottleneck]
    add(title,reason,88,10)
    if account.goal=="boss":add("Examiner les règles du boss","Construire une équipe adaptée à la rencontre, pas une tier list générale.",87,10)
    remaining=account.minutes
    for task in sorted(result,key=lambda t:-t["priority"]):
        task["fits_budget"]=task["minutes"]<=remaining
        if task["fits_budget"]:remaining-=task["minutes"]
    return sorted(result,key=lambda t:-t["priority"])

def ask(account,question,model="qwen2.5:3b"):
    seed()
    from dataclasses import asdict
    context=json.dumps(asdict(account),ensure_ascii=False)
    return advise("brown_dust_2","Progression F2P, équipe, équipement, ressources, événements, combat. Répondre en français. Ne pas inventer de statistiques ni de bannières actuelles. Compte déclaré : "+context+"\nQuestion : "+question,model=model)
