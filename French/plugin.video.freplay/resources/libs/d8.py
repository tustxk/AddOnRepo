def list_shows(param):
    shows=[]
    
    if param=='empty':
        shows.append( ['INFO TALK', 'Info Talk','','folder'] )
        shows.append( ['DOC MAG', 'Doc Mag','','folder'] )
        shows.append( ['ART DE VIVRE', 'Art De Vivre','','folder'] )
        shows.append( ['DIVERTISSEMENT', 'Divertissement','','folder'] )
        shows.append( ['SPORT', 'Sport','','folder'] )
    
    if param=='INFO TALK':
        shows.append( ['LE GRAND 8', 'Le Grand 8','','shows'] )
        shows.append( ['D8 LE JT', 'D8 le JT','','shows'] )
        shows.append( ['langue%20bois', 'Langue de bois s\'abstenir','','shows'] )
    
    if param=='DOC MAG':
        shows.append( ['EN QUETE D\'ACTUALITE', 'En Quete d\'Actualite','','shows'] )
        shows.append( ['AU COEUR DE L\'ENQUETE', 'Au Coeur de l\'Enquete','','shows'] )
    
    if param=='ART DE VIVRE':
        shows.append( ['LES ANIMAUX DE LA 8', 'Les animaux de la 8','','shows'] )
        shows.append( ['A VOS REGIONS', 'A Vos Regions','','shows'] )
        shows.append( ['A VOS RECETTES', 'A Vos Recettes','','shows'] )
    
    if param=='DIVERTISSEMENT':
        shows.append( ['D8 PART EN LIVE', 'D8 Part en Live','','shows'] )
        shows.append( ['TPMP', 'Touche Pas a mon poste','','shows'] )
        shows.append( ['PALMASHOW', 'Palmashow','','shows'] )
        shows.append( ['TOUCHE PAS A MON ARDISSON', 'Touche pas a mon Ardisson','','shows'] )
        shows.append( ['EST-CE QUE CA MARCHE', 'Est-ce Que Ca Marche','','shows'] )
        shows.append( ['NOUVELLE STAR', 'Nouvelle Star','','shows'] )
        shows.append( ['VOYAGE AU BOUT DE LA NUIT', 'Voyage au bout de la Nuit','','shows'] )
        shows.append( ['LA CHORALE DES MONTAGNES', 'La Chorale des Montagnes','','shows'] )
        shows.append( ['LA SELECTION', 'La Selection','','shows'] )
        shows.append( ['SUR LES PAS DE SOPHIE TITH', 'Sur Les Pas de Sophie Tith','','shows'] )
    
    if param=='SPORT':
        shows.append( ['GYM DIRECT', 'Gym Direct','','shows'] )
        shows.append( ['DIRECT AUTO', 'Direct Auto','','shows'] )



    return shows
        