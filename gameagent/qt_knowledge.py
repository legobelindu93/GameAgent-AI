from PySide6.QtWidgets import QLineEdit
from .qt_workbench import Workbench,launch
from .obsidian_ui import label
from .knowledge import Knowledge
from .catalog import Catalog
from .advisor import advise
class KnowledgePanel(Workbench):
    def __init__(self):
        super().__init__("Centre de connaissances","Guides, personnages, builds et conseiller local")
        self.query=QLineEdit();self.query.setPlaceholderText("Question ou personnage")
        self.patch=QLineEdit();self.patch.setPlaceholderText("Version du jeu (facultatif)")
        self.controls.addWidget(label("Question","section"));self.controls.addWidget(self.query);self.controls.addWidget(self.patch)
        self.section("Recherche",[("Guides","Recherche SQLite FTS5",lambda:self.search("guides")),("Personnages / builds","Catalogue structuré",lambda:self.search("catalog")),("Interroger l’IA","Ollama local",lambda:self.search("ask"))]);self.controls.addStretch()
    def search(self,mode):
        g,q,p=self.game,self.query.text(),self.patch.text() or None
        def work():
            if mode=="ask":return advise(g,q,patch=p)
            db=Catalog(g) if mode=="catalog" else Knowledge(g)
            try:return db.search(q,patch=p)
            finally:db.close()
        self.run(work)
if __name__=="__main__":launch(KnowledgePanel)
