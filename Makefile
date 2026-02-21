PYTHON = python3
MAIN = MapMaker.py
TESTS = tests_mapmaker.py

# Commande par défaut
all: run

# Installation
install:
	pip install -r requirements.txt

# Lancer le jeu
run:
	$(PYTHON) $(MAIN)

# Lancer les tests unitaires
test:
	$(PYTHON) -m unittest $(TESTS)

# Nettoyer les dossiers de cache Python
clean:
	rm -rf __pycache__