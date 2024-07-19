# Guide outils - Workshop LE HACK

## OpenOCD

Terminal 1 :

```
openocd  -f /usr/local/share/openocd/scripts/interface/stlink.cfg -f /usr/local/share/openocd/scripts/target/panchip.cfg -c "transport select hla_swd" -c "gdb_memory_map disable" -c "gdb_breakpoint_override hard"  -d3
```
   
Terminal 2 : 

```
telnet 127.0.0.1 4444
```
#### Dump of the flash 

Terminal telnet :

```
reset 
halt
flash read_bank 0 ABSOLUTE_PATH_TO_BIN.bin
resume
```


#### Reprogrammation de la flash

Terminal telnet : 

```
reset halt
flash erase_sector 0 0 61
flash write_bank 0 ABSOLUTE_PATH_TO_BIN.bin
resume
```


#### Debug 
Terminal 2 : 

```
gdb-multiarch
```

Pour connecter gdb au serveur OpenOCD : 

```
target remote :3333
```

Attention aux conflits lorsqu'une instance telnet et une instance gdb sont actives en même temps.

Une commande d'aide a été mise à disposition pour faciliter la visualisation des informations importantes : 

```
disp_bof
```


## Logic 2

Pour lancer l'outil : 

```
cd ~/Documents/tools
./Logic-2.4.14-linux-x64.AppImage
```

Après avoir connecté l'analyseur logique (penser à le faire passer à la VM)
* Dans le menu "Devices", penser à réduire le débit de données pour éviter l'interruption de la capture
* Dans le menu "Analysers", il est possible de rajouter un interpréteur "Async Serial" sur un channel de votre choix pour lancer une interprétation UART. Le principal paramètre à ajuster est le baud rate de la communication
* Une fois la capture faite vous devriez voir le résultat de l'analyse UART dans la fenêtre "Analysers", visualisable en hexadécimal ou en ASCII.

## RF_tool

Après avoir connecté la carte Hardsploit (pensez à la passer à la VM), vous pouvez lancer l'outil : 

```
cd ~/Documents/tools
python3 RF_tool_stud.py
```

Les détails sur l'utilisation de l'outil sont accessibles via la commande `help <command>`

`CTRL C` : mettre fin à une commande
`CTRL D` : quitter l'outil 
