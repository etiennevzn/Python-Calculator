from tkinter import *
import math
from collections import deque

class Calculatrice(Tk):
  
    def __init__(self,l=400,h=600) -> None:
        #appel du constructeur de tkinter
        super().__init__()

        """
        Ci dessous le code pour centrer la calculatrice à l'écran. Nous avons choisi de ne pas utiliser ce code de manière à ce que 
        la fenêtre s'adapte automatiquement à la taille de l'interface sans avoir besoin de trouver la largeur et hauteur adaptée. 

        ecran_x = self.winfo_screenwidth()
        ecran_y = self.winfo_screenheight()
        pos_x = ecran_x // 2 - l // 2
        pos_y = ecran_y // 2 - h // 2
        geometrie = f"{l}x{h}+{pos_x}+{pos_y}"
        self.geometry(geometrie)"""

        #titre de la fenêtre
        self.title("Calculatrice")

        #attribut d'affichage 
        self.chaine = StringVar()

        #attributs pour gérer l'historique, une pile  de taille 10 pour la mémoire et un label pour l'affichage
        self.historique = deque(maxlen=10)
        self.history_label = Label(self, text="Historique", anchor='e', bg="#a2af77", fg="white", font=("Arial", 25), padx=10, pady = 10)
        self.history_label.grid(column=5, row=0, columnspan=4, rowspan=6, padx=10, pady=10, sticky="nsew")

        #attribut permettant de réinitialiser la zone d'affichage en cas d'erreur ou après un résultat
        self.resulted = 0

        #fonctions de création l'interface graphique
        self.createButtons()
        self.configure(bg="white", padx=10, pady=10)

    def createButtons(self):

        """Création de dictionnaires qu'on réutilisera en arguments pour le style des boutons"""
        default_button_style = {
            "bg": "#595959", "fg": "white", "highlightthickness": 0,
            "font": ("Arial", 25, "bold")
        }
        default_button_grid = {"padx": 10, "pady": 10, "sticky": "nsew"}

        #zone d'affichage du résultat
        result_label = Label(self, textvariable=self.chaine, anchor='e', bg="#a2af77", fg="white", font=("Arial", 25), padx=10, pady = 10)
        result_label.grid(column=0, row=0, columnspan=5, **default_button_grid)

        #première ligne de boutons
        Button(self, text="cos", command=lambda : self.nombres('cos('), **default_button_style).grid(column=4, row=1, **default_button_grid)
        Button(self, text="*", command=lambda : self.nombres('*'),**default_button_style).grid(column=3, row=1, **default_button_grid)
        Button(self, text="7", command=lambda : self.nombres('7'),**default_button_style).grid(column=0, row=1, **default_button_grid)
        Button(self, text="8", command=lambda : self.nombres('8'),**default_button_style).grid(column=1, row=1, **default_button_grid)
        Button(self, text="9", command=lambda : self.nombres('9'),**default_button_style).grid(column=2, row=1, **default_button_grid)

        #deuxième ligne de boutons
        Button(self, text="sin", command=lambda : self.nombres('sin('), **default_button_style).grid(column=4, row=2, **default_button_grid)
        Button(self, text="-", command=lambda : self.nombres('-'),**default_button_style).grid(column=3, row=2, **default_button_grid)
        Button(self, text="4", command=lambda : self.nombres('4'),**default_button_style).grid(column=0, row=2, **default_button_grid)
        Button(self, text="5", command=lambda : self.nombres('5'),**default_button_style).grid(column=1, row=2, **default_button_grid)
        Button(self, text="6", command=lambda : self.nombres('6'),**default_button_style).grid(column=2, row=2, **default_button_grid)

        #troisième ligne de boutons
        Button(self, text="tan", command=lambda : self.nombres('tan('), **default_button_style).grid(column=4, row=3, **default_button_grid)
        Button(self, text="+", command=lambda : self.nombres('+'),**default_button_style).grid(column=3, row=3, **default_button_grid)
        Button(self, text="1", command=lambda : self.nombres('1'), **default_button_style).grid(column=0, row=3, **default_button_grid)
        Button(self, text="2", command=lambda : self.nombres('2'), **default_button_style).grid(column=1, row=3, **default_button_grid)
        Button(self, text="3", command=lambda : self.nombres('3'), **default_button_style).grid(column=2, row=3, **default_button_grid)

        #quatrième ligne de boutons
        Button(self, text="/", command=lambda : self.nombres('/'), **default_button_style).grid(column=3, row=4, **default_button_grid)
        Button(self, text="π", command=lambda : self.nombres('π'), **default_button_style).grid(column=4, row=4, **default_button_grid)
        Button(self, text="0", command=lambda : self.nombres('0'), **default_button_style).grid(column=0, row=4, columnspan=2, **default_button_grid)
        Button(self, text=".", command=lambda : self.nombres('.'), **default_button_style).grid(column=2, row=4, **default_button_grid)

        #cinquième ligne de boutons
        Button(self, text="C", command=lambda : self.clear(), **default_button_style).grid(column=2, row=5, **default_button_grid)    
        Button(self, text="√x",command=lambda : self.nombres('sqrt('), **default_button_style).grid(column=3, row=5, **default_button_grid)
        Button(self, text="x²",command=lambda : self.nombres('²'), **default_button_style).grid(column=4, row=5, **default_button_grid)
        Button(self, command=lambda : self.calculs_simples(),bg= "blue", fg = "white", highlightthickness = 0, font = ("Arial", 25, "bold"), text="=" ).grid(column=0, row=5, columnspan=2,**default_button_grid)
        
        #sixième ligne de boutons
        """"Nécessité d'inclure un bouton ) pour pouvoir utiliser les fonctions sin, cos, tan etc. 
        Ce bouton permet de délimiter la zone ou s'applique ces fonctions."""
        Button(self, text=")", command=lambda : self.nombres(')'),  **default_button_style).grid(column=4, row=6, **default_button_grid)

    def nombres(self, val):

        """Permet d'afficher le calcul en cours. S'il y a eu une erreur au préalable ou qu'un résultat est affiché à l'écran
        et que l'utilisateur appuie sur un autre bouton que ceux permettant de continuer le calcul, on réinitialise l'affichage"""
        if self.resulted == 1:
            if self.chaine.get() == "Erreur":
                self.resulted = 0 
                self.chaine.set(val)
            elif val in {"+","-","*","/"}:
                self.resulted = 0 
                self.chaine.set(self.chaine.get() + val)
            else:
                self.resulted = 0 
                self.chaine.set(val)

        else:
            self.chaine.set(self.chaine.get() + val)

    def clear(self):
        """Permet de gérer l'action du bouton C"""
        self.chaine.set("")
    
    def calculs_simples(self):
        """Réalise le calcul demandé lorsqu'on appuie sur le bouton ="""
        try:

            #remplace les symboles par leurs expressions dans le module math
            self.chaine.set(self.chaine.get().replace("π","math.pi"))
            self.chaine.set(self.chaine.get().replace("sin(","math.sin("))
            self.chaine.set(self.chaine.get().replace("cos(","math.cos("))
            self.chaine.set(self.chaine.get().replace("tan(","math.tan("))
            self.chaine.set(self.chaine.get().replace("sqrt(","math.sqrt("))
            self.chaine.set(self.chaine.get().replace("²","**2"))

            # On met à jour l'historique :
            self.update_historique(self.chaine.get() + " = " + str(float(eval(self.chaine.get()))))

            #calcul du résultat:
            self.chaine.set(str(float(eval(self.chaine.get()))))
            self.resulted = 1

        except Exception as e:
            #si on a entré une expression non calculable, on affiche Erreur
            self.chaine.set("Erreur")
            self.resulted = True


    def update_historique(self, value):
        """Ajoute le calcul sur le haut de la pile de l'historique"""
        self.historique.appendleft(value)
        historique_text = "\n".join(self.historique)
        self.history_label.config(text=historique_text)

def main():
    #lance la fenêtre
    calc = Calculatrice()
    calc.mainloop()

if __name__ == "__main__":
    main()
