# Bypass d'EDR

*Processus Thief*

- [ProcessusT - Twitter](https://twitter.com/ProcessusT)

- [Christopher Thiefin - LinkedIn](https://www.linkedin.com/in/christopher-thiefin/)

- [Processus Thief - Youtube](https://www.youtube.com/c/processusthief)

C'est une suite de la conférence de 2023 sur le même sujet. L'objectif de la conférence est de se focaliser sur la post-exploitation et l'extraction de hash du domaine sans déclencher l'EDR. Il s'agit de 10 règles à suivre.

## Les 10 règles pour bypass un EDR

1. Faire attention à l'entropie. Il faut plutôt privilégier l'encodage plutôt que le chiffrement car une entropie élevée attire l'attention de l'EDR.

2. `VirtualAlloc` n'est pas la seule option. Certains utilisent `HeapAlloc` mais attention il faut savoir ce que l'on fait car dans certains cas elle va appeller `VirtualAlloc`.

3. Eviter le stagging (loader puis payload). On préfère utiliser du stageless (tout dans le même fichier).

4. Attention aux changements de la protection de la mémoire. Les directs et indirect syscalls sont détectés à cause du jump sur la NTDLL ce qui n'est pas un comportement normal. Pour contourner cela, on peut faire du *custom call stack* (un autre thread alloue une zone mémoire pour nous).

5. L'exécution asynchrone est parfois meilleure.

6. Utiliser des *named pipes*. Ils sont utilisés de manière légitime et peut nous permettre d'éviter que l'EDR détecte le beacon car il ne voit que le pipe (car lancé depuis un service). Cela ne nécessite pas non plus de privilège administrateur.

7. Utiliser du *command line argument spoofing*.

8. Utiliser *Microsoft Process Mitigation Policy* (charger une DLL non trustée par Microsoft). Cela ne fonctionne cependant plus très bien.

9. Ne jamais mixer toutes les techniques ensemble car cela accroît le nombre de marqueurs pour l'EDR.

10. Ne jamais exposer son C2 directement. On préfèrera proxyfier le traffic avec le beacon.

## Astuces

`conhost` peut être lancé sans interface graphique (paramètre `--headless`). Cependant, cela peut être détecté.

On peut trouver des certificats qui ont fuité sur internet. Grâce à cela, on peut truster notre payload.

## DC sync

On peut voler les identifiants de connexion du compte `MSOL`. Il s'agit d'un compte par défaut qui est autorisé à faire un DC sync. Pour cela, on utilise `xpcmdshell` pour requêter les identifiants de `MSOL`. On peut ensuite extraire tous les secrets de l'AD.
