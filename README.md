# Hermione


Il s'agit seulement d'un petit wrapper autour de [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## yt

Au final, le principal programme fonctionnel intéressant est `yt.py`.

```
./yt.py  "https://www.youtube.com/watch?v=j48hBShnfB0"
```


## installation

Vous devez avoir `pyenv` installé sur votre système. Ensuite :
```
./install.sh
```

## Astuce

Pour avoir la liste de toutes les vidéos d'une chaine:
```
youtube-dl --get-filename -o "%(id)s" "https://www.youtube.com/channel/UCYNbYGl89UUowy8oXkipC-Q"
```
