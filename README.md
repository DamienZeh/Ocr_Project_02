# Scraper le site Books To Scrape 


Projet permettant de scraper de 3 manières différentes le contenu du site [https://books.toscrape.com](https://books.toscrape.com/).

<br/><br/>




## Téléchargement et installation 


- copiez le dépôt distant, dans votre terminal/interpréteur. <br/>
	Vous allez dans le dossier ou vous souhaitez placer le projet,
	 exemple : ``cd C:\Users\damie\Documents\pythonProject``
- Puis ``git clone https://github.com/Damndamn2/Ocr_Project_02.git``
- Puis, allez dans ce projet : ``cd Ocr_Project_02\``
- On crée l’environnement virtuel avec  ``python -m venv env``
	_(‘env’ est le nom que j’ai sur mon environnement virtuel, il est aussi noté dans le gitignore.)_
- Puis on l’active : ``.\env\Scripts\activate.bat`` (pour windows)<br/>
	_(on a maintenant un ‘(env)’ d’affiché)_
- Puis, l’installation  des packages (présent dans le requirements.text):
	``pip install -r requirements.txt``

<br/>


## Démarrage


### Basique

Lancez l’un des 3 fichiers python que vous souhaitez, avec la commande « **python fichier.py** »<br/>
exemple : ``python Analyze_A_Product.py``

- **Analyze_A_Product.py** va donner toutes les informations d’un livre du site [https://books.toscrape.com](https://books.toscrape.com/).<br/> 
De base il donne des infos sur le livre [‘Sharp Objects’](https://books.toscrape.com/catalogue/sharp-objects_997/index.html).

- **Analyze_Products_From_Category.py** va donner toutes les infos et tous les livres d’une catégorie du site.<br/>
De base, il affiche les données de la catéorie [‘fantasy’](https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html).

- **Analyze_All_Categories.py** va donner tous les livres et leurs informations de tout le site [https://books.toscrape.com](https://books.toscrape.com/)



### Avancé

Si vous souhaitez scraper d’autres liens dans le site, vous pouvez passer par un IDE, comme [**Pycharm**](https://www.jetbrains.com/fr-fr/pycharm/) :

- Lancez **Pycharm**
- Ouvrez le dossier **Ocr_Project_02**. Puis pour activer l’environnement virtuel déjà présent dans le projet :<br/>
 ``File`` → ``Settings`` → ``Project : Ocr_Project_02`` → ``Python Interpreter`` → bouton ``paramètre``(à droite) → ``add`` → cochez ``Existing environnment``, puis choisissez le fichier ``python.exe``, présent dans le projet dans ``env\Scripts\``. Puis faites ``ok``.

Puis ouvrez le fichier qui vous intéresse. Chacun des trois fichiers python, une fois exécuté vous donnera un dossier de sortie avec ses fichiers csv, et un dossier avec ses fichiers images de livres.<br/>
 _(les dossiers porteront le même nom que leur fichier, plus '**__Csv**' ou '**__Images**' à la fin.)_ <br/>
Les 3 fichiers fonctionnent de la même manière. Le lien que vous voulez taper est à mettre  tout en bas du code dans le main, entre ses guillemets.

- Pour **Analyze_A_Product.py**, vous tapez le lien d’un des livres, et vous aurez son contenu.

- Pour **Analyze_Products_From_Category.py**, vous tapez le lien de la première page d’une catégorie, pour avoir tout le contenu de cette catégorie.

- Et enfin pour **Analyze_All_Categories.py**, vous aurez tout le contenu du site book.toscrape.com.



<br/><br/><br/>





## Auteur

* **Damien Hernandez** _alias_ [DamienZeh](https://damienhernandez.fr/)


