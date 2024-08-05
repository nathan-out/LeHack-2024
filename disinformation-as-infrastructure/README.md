# Disinformation as Infrastructure

*Hervé Letoqueux de VIGINUM*

- [Hervé Letoqueux - LinkedIn](https://www.linkedin.com/in/herv%C3%A9-letoqueux-3b5111298/)

Analyse de la campagne de désinformation **Portal Kombat** par les équipes de VIGINUM. **Portal Kombat** est un vaste réseau Russe de désinformation. Il y avait plus de 193 portails d'information ciblant les pays de l'ouest. 

## Comment cela a commencé ?

32 Octobre 2023 - Plusieurs pro-russes se mettent en photo devant la tour Eiffel. Cette photo a été relayée dans des groupes Telegram mais à fait moins de 800 vues. Le site pravda-fr.com a repris cette photo pour la partager.

## L'enquête

**Premier pivot** : Grâce à ce site, une analyse des tags HTML a permis de trouver d'autres sites liés pravda-de.com, pravda-es.com ou même pravda-pl.com. D'autres site sous la forme {ville_ukrainienne}-news.ru

Tous les sites sous la forme pravda-XX.com étaient protégés par CloudFlare, impossible alors de récupérer leur adresse IP. Cependant, les sites sous la forme {ville_ukrainienne}-news.ru ne l'étaient pas forcément. L'hypthèse a été la suivante : Est-il probable que tous les sites soient dans le même sous réseau ?

**Deuxième pivot** : Un script a alors été créé pour parcourir toutes les IPs du sous-réseau en demandant à la machine si elle répondait au nom de pravda-fr.com, ou pravda-es.com, etc.

**Troisième pivot** : Grâce au header `ETag`, il a été possible de récupérer plusieurs informations utiles. La récupération de contenu la plus intéressant fut grâce à [Archive.org](https://archive.org/), dans laquelle se trouvait une adresse mail gmail.com et des trackers Google Analytic.

## Enseignements

- Certains TTP peuvent fournir des heuristiques pour détecter plus rapidement ces campagnes.

- Il existe un cheuvauchement entre les FIMI (Foreign Information Manipulation and Interference), certains APTs et le cybercrime classique.

- L'audience réelle de ce genre de réseau de désinformation n'est pas correlé à son impact sur la société.

Viginum effectue ces opérations pour prévenir des potentiels dégâts.