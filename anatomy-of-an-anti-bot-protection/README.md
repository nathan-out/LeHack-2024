# Anatomy of an Anti-Bot Protection

*Fabien Vauchelles*

- [Fabien Vauchelles - LinkedIn](https://www.linkedin.com/in/fabienvauchelles/)

- [Scrapoxy_IO - Twitter](https://x.com/scrapoxy_io)

Les VM d'un cloud provider ne permettent pas de contourner d'éventuels bloquages. Pour les contourner il faut passer le *Test de Turing*.

## Comment les systèmes anti-bot fonctionnent

Ils analysent plusieurs couchent : 

- adresses IP.

- protocoles.

- navigateurs.

- comportement.

Tous ces éléments **doivent être cohérents** il ne faut en négliger aucun, au risque de se faire bloquer.

## Adresses IP

Ce sont des éléments très riches en informations. Votre géolocalisation doit être cohérente avec ce que vous recherchez et quand vous le faites.

## Protocoles

De la même manière, l'utilisation des protocoles par un bot doit être cohérente et la plus proche possible de ce qu'un humain pourrait en faire.

Par exemple pour le TLS handshake, chaque navigateur a son propre *TLS fingerprinting*.

Pour HTTP2, on peut faire du *browser fingerprinting* grâce aux headers HTTP renvoyés. Si votre système utilise un nombre de header minimal, comme c'est souvent le cas, alors vous serrez bloqués très vite car aucun fingerprinting n'est possible.

## Navigateurs

Ils contiennent énormément de données (OS, plugins installés, taille de fenêtre, architecture...). Vous devez être cohérent et vous faire passer pour un **vrai** navigateur. Par exemple, un Android émulé ne devrait pas être sous une architecture x64 mais plutôt sous ARM.

Il est aussi possible de faire du canvas fingerprinting ; en fonction de comment sont rendus certaines éléments graphiques (smileys par exemple), il est possible d'identifier votre carte graphique et tout un tas d'autres informations.

## Comportement

Quelques règles pour éviter d'être suspect : 

- utiliser des search queries (recherche classique via Google par exemple) au lieu de directement utiliser un *deep-link* (résultat de la search query).

- ne désactivez pas le JS et faites un rendu du maximum d'information.

- privilégiez des mouvements de souris organiques (pas de lignes droites).

## Synthèse

Tous ces signaux sont aggrégés par les systèmes anti-bots et ces derniers calculent un score. Lorsque votre score dépasse une certaine valeur, alors vous serrez soit bloqué soit redirigé vers des captchats. Les systèmes anti-bots utilisent des modèles d'IA pour calculer votre score.

C'est donc assez complexe d'avoir un système résilient face à autant de paramètres. Cependant, comme tous modèles d'IA, ils ont aussi des faux-positifs (vrais humains détectés comme bots). Pour éviter un impact trop important sur les sites qu'ils monitorent, les systèmes anti-bots nivellent souvent par le bas l'agressivité de leurs modèles. Si on arrive à se faire passer pour un faux-positif, on peut donc contourner le bloquage. Ces modèles se concentrent sur les signaux les plus marquants.

Wappalyser est une extension de navigateur qui donne toutes les technologies qu'un site utilise, système anti-bot inclus.

## La pyramide du contournement de système anti-bots

Des mesures les plus simples aux plus complexes pour contourner (presque) tous les bloquages.

1. coder un scrapper (lib `scrapy` sous Python). Il doit être consistent avec le user-agent utilisé, la version TLS, l'adresse IP, etc...

2. utiliser un proxy standard (`Scrapoxy`).

3. démarrer un navigateur *headless* (sans interface graphique).

4. utiliser des proxies avancés (*residential proxies*, proxy hardware, ferme de téléphones...), ils sont très efficaces mais plus chers.

5. utiliser un *headfull browser* (inverse de *headless*) commercial ou open source.

6. utiliser *unblocker API* (plus cher).

7. résoudre les captchats grâce à l'IA.

Enfin, tenter de reverse les codes JavaScript utilisés par les systèmes anti-bots est une tâche **très** difficile car ils sont fortement obfusqués à plusieurs niveaux.
