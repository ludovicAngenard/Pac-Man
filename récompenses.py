
#Exécutez ce code pour réinitialiser les bonus que sont les déguisements et les quatre fantômes noirs
import pickle
debloquage={
  "debloque1":0,
  "debloque2":0,
  "debloque3":0,
  "debloque4":0,
  "debloque5":0,
  "debloque6":0,
  "debloque7":0,
  "debloque8":0,
  "actif":0,
}

with open('récompenses', 'wb') as fichier2:
    mon_pickler_recompenses = pickle.Pickler(fichier2)
    mon_pickler_recompenses.dump(debloquage)
