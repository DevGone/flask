# flask

EDF API : http://docs.tic.apiary.io/

Champs historisés dans le raspberric :
ADCO : N° d’identification du compteur : 041067030782
OPTARIF : Option tarifaire (type d’abonnement)
ISOUSC : Intensité souscrite (ampères) = 30
BASE : Index si option = base (Wh)
HCHC : Index heures creuses si option = heures creuses (Wh)
HCHP : Index heures pleines si option = heures creuses (Wh)
PTEC : Période tarifaire en cours = pas de valeurs
IINST : Intensité instantanée (ampères) -> history
ADPS : Avertissement de dépassement de puissance souscrite (ampères) (message émis uniquement en cas de dépassement effectif, dans ce cas il est immédiat)
IMAX : Intensité maximale (ampères) ?
PAPP : Puissance apparente (Volt.ampères) -> history
HHPHC : Groupe horaire si option = heures creuses = pas de valeurs


**********************************************************************

Info qui peuvent être interessantes depuis l'API du raspberric :

/source/1/price-option
-> begin date : date du branchement du raspberry

/source/1/event
-> retourne les évenements (mais aucun pour l'instant ex:anomalie réacteur nucléaire)

/source/1/period 
-> retourne toutes les périodes d'heures pleines et heures creuses dans la periode demandée (par defaut depuis le début)

/period
-> type de periodes existantes

/field
-> description des champs donc donne l'unité des mesures (watt, ampere..)

/history
- field : papp (puissance apparente), iinst (intensité instantanée), isousc (=30), hchc (message toutes les minutes durant heures creuses avec value incrementée +1), hchp pour heures pleines, imax
- pattern : none (prends que la valeur pile poil à l'heure), avg (par default, moyenne sur les steps), max, min
-meta = ?
-step = pas de mesure
-begin et end pour delimiter zone temporelle (optionel)

/history/meta
-> renvoie le nombre de réponse de history avec les mêmes arguments
