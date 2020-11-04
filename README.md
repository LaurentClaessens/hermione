# Hermione

Au départ, je voulais créer un programme pour télécharger plus facilement les images de mes flux RSS en scrappant les sites. Au final, je n'ai fait qu'esquisser une fonction pour [smbc](https://www.smbc-comics.com) et fait un truc assez avancé pour youtube.

## yt

Au final, le seul programme fonctionnel intéressant est `yt.py`.

```
./yt.py  "https://www.youtube.com/watch?v=j48hBShnfB0"
```
va télécharger la vidéo en choisisant le format numéro 18, c'est à dire pas la meilleur qualité (économies d'énergie, tout ça).

Il s'agit seulement d'un petit wrapper autour de [youtube-dl](https://youtube-dl.org).


## install

Vous devez avoir `pyenv` installé sur votre système. Ensuite :
```
./install.sh
```

## Astuce

Pour avoir la liste de toutes les vidéos d'une chaine:
```
youtube-dl --get-filename -o "%(id)s" "https://www.youtube.com/channel/UCYNbYGl89UUowy8oXkipC-Q"
```

## Pour s'abonner au RSS

```
https://www.youtube.com/feeds/videos.xml?channel_id=UCYNbYGl89UUowy8oXkipC-Q
```
