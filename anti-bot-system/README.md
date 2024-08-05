# Anti Bot System

*Fabien Vauchelles* - Scrapoxy

- [Fabien Vauchelles - LinkedIn](https://www.linkedin.com/in/fabienvauchelles)

Aujourd'hui la majorité des sites web possèdent des protections contre les bots et automatisation et controlent les accès à leur api. Pour contrer ces systèmes, il est nécessaire de comprendre comment ils fonctionnent.

## La base

Lorsque nous navigons, de nombreuses information transitent :
- IP
- Header du protocole
- Navigateur
- Comportement utilisateur

Il est possible de faire des fingerprint à partir de ces informations, quelques sites pour voir des fingerprint :
- [fingerprint.scrapoxy.io](fingerprint.scrapoxy.io)
- [browserleaks.com](browserleaks.com)
- [deviceinfo.me](deviceinfo.me)

## Ce qui trahi l'automatisation

Voici une list non-exhaustive de ce qui trahi énormement l'utilisation de scripts.

### Requête de recherche ou lien direct

Il y a un différence nette entre aller sur http://google.com puis taper sa recherche ou aller directement sur https://google.com/?query=chien

### Où est le JS ?

Imaginons, nous voulons récupérer une information sur un site web, cette valeur est directement dans le HTML, un simple curl alors suffit. Cependant, si vous naviguez sur le site vous chargeriez le js, le css, les images, les polices d'écritures, etc.

### La souris

Pour nous il est impossible de faire une ligne droite avec une souris. De plus, dans la majorité des cas, nous effectuons des courbes avec la souris entre deux points. Notre script ne doit surtout pas faire des lignes droites.

## Méthodologie de scrapping

### Etape 1

Coder un scraper boosted :
- Delay de requête
- Utilisation des cookies
- Gérer le TLS
- Utiliser des users agent cohérent
- Bien spécifer les headers du protocole (comme Referer par exemple)
- Faire de payload "normaux"

Si cela ne fonctionne pas go to the next station

### Etape 2

Utiliser des proxies standards, d'abord des gratuits, ensuite des payants.

### Etape 3

Utiliser un navigateur headless comme puppeter

### Etape 4

Utiliser des proxies avancée comme :
- ISP
- Mobile
- Hardware
- Residential

### Etape 5

Utiliser un navigateur headful

### Etape 6

Utiliser un "unblocker API" comme Brightdata, Oxylabs

### Etape 7

Résoudre le captcha ou les challenges avec l'IA
- CapSolver
- CapMonster

### Etape 8

Reverse le code du système qui envoi les données au système antibot
> Bon courage, souvent js minifié avec babel qui obfusque le code.