#!/usr/bin/python



make clean tests
echo "test connexion is done !"

python reset-database.py
echo "Reset data done"

echo "############################# COLLECT FINGER PRINTS #################################"

python collect-fingerprints-of-songs.py
echo "la collection des finger-prints a été faite avant le build de dockerfile et docker-compose !"

echo "############################# GET DATABASE STAT #################################"
python get-database-stat.py

echo "############################# TOUT EST OK #################################"
echo "############################# AU REVOIR MONSIEUR FRANCIS MUJANI #################################"
echo "############################# YOU ARE THE BEST #################################"

