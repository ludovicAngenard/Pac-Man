#/!\ IMPORTANT si vous exécutez ce code vous devez aussi exécuter le code du fichier "récompenses"
# Exécutez ce code pour réinitialiser votre score et votre monnaie virtuelle
#le 'level' doit toujour être égale à 'bonus' +1
import pickle
niveaux={
  "level":    1,
  "bonus":   0,
  "argent":   0,
  "point": 0,
}

with open('donnees', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(niveaux)