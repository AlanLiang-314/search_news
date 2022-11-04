import os 
import save

BACKUP_DIR = "backup/urls.pkl"

pickler = save.pickler("urls/urls.pkl")

data = pickler.show()

backup_pickler = save.pickler("backup/urls.pkl")