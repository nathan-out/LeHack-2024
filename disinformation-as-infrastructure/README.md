# Disinformation as Infrastructure

*Hervé Letoqueux de VIGINUM*

Analyse de la campagne de désinformation **Portabl Kombat** par les équipes de VIGINUM.

Certaines adresses IP étaient situées derrières CloudFlare. On peut étendre l'ensemble des IPs utilisées pour disséminer de la désinformation grâce au header `ETag`. De même, il est possible d'automatiser de la récupération d'ancien contenu avec [Archive.org](https://archive.org/). Avec cela, on peut récupérer les tracker Google Analytic, des emails et toutes sortes d'informations qui serviront à pivoter.

## Enseignements

- Certains TTP peuvent fournir des heuristiques pour détecter plus rapidement ces campagnes.

- Il existe un cheuvauchement entre les FIMI (Foreign Information Manipulation and Interference), certains APTs et le cybercrime classique.

- L'audience réelle de ce genre de réseau de désinformation n'est pas correlé à son impact sur la société.
