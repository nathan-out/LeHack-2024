# Découverte du Groupe APT-C-36 sur les Réseaux D'une Profession Libérale Réglementée

*CSIRT Inquest*

- [Inquest - LinkedIn](https://linkedin.com/company/inquest-risk/)

## Contexte

Inquest intervient sur des entreprises du monde financier et de la banque. D'après plusieurs investigations chez différents cliens, certains IoC semblent converger vers un unique groupe.

Ce groupe aurait des motivations financières.

## Mode opératoire

Ils utilisent du spearphishing avec des pièces-jointes malveillantes du type `xxx.pdf.hta`. Puisque par défaut les extensions des fichiers sont cachés sous Windows, les victimes croient ouvrir un PDF. Il y a ensuite une installation de leurs charges qui comportent des keyloggers et d'autres malwares du genre.

La première persistence se fait grâce à des outils de prises en main à distance.

La reconnaissance est faite grâce à des outils type NetView, Advanced IP Scanner et d'autres outils du genre. Ensuite, l'objectif est d'élever leurs privilèges pour extraires les hashs de LSASS.

On observe plusieurs groupes sur les mêmes machines !

Pour inciter les sociétés à faire des virements vers leurs comptes, les pirates déposent des PDF sur les machines des victimes avec leurs propres RIB à l'intérieur.

Les groupes laissent beaucoup de traces, preuve d'une certaine forme d'amateurisme. L'APT pourrait se servir d'eux comme des *Initial Access Brocker*.

Dans les attaques plus récentes, les pirates utilisent du RDP entre les machines infectées. La phase de reconnaissance est plus rapide et ils maquillent leurs charges avec des noms d'outils internes à l'entreprise.

## Remédiations

Les mots de passe des victimes étaient souvent faibles et l'hardening de leurs postes inexistants (comptes chargés de l'administratif administrateurs de leur poste). La mise en place d'un EDR et l'ajout d'un pare-feux ont aidé à remédier la compromission et à endiguer du phishing depuis des adresses légitimes.

## Evolutions du mode opératoire

- Nouveaux outils.

- Exploitation des mauvaises configurations des routeurs.

- Scans plus larges.

- Latéralisation entre les entreprises.

- Logiciels de surveillance uniquement sur les machines qui peuvent effectuer des virements.

## APT C-36

Il pourrait être basé en Amérique du Sud, il ciblerait majoritairement des entités du gouvernement colombien, des entreprises du secteur financier ou des pétrolières. Ils sont peu connus et discrets.
