## Requisitos para la instalación
* Tener una versión de python 3.10.12 o superior
* Tener una versión de docker 26.0.0 o superior
* Tener cuenta en github

## Instalación FeedCycle
Estas instalaciones funcionan para cualquier sistema operativo
### Instalación desde clone
```bash
git clone https://github.com/Miguelisius/FeedCycle.git && cd FeedCycle
docker-compose up --build
```
### Instalación desde zip
```bash
unzip FeedCycle-main.zip && cd FeedCycle-main
docker-compose up --build
```
## Finalizar
### Parar y eliminar contenedor
```bash
docker stop FeedCycle
docker rm FeedCycle
```

## Base de datos
Cuando se ejecuta por primera vez el sistema crea una base de datos.
En caso de que se quiera borrar una base de datos ya existente perteneciente a este proyecto hay que ejecutar el siguiente comando:
```bash
rm db.sqlite3
```

## Enlace para instalar docker-desktop
Dentro del enlace que de adjunta viene cómo instalar docker-desktop para cualquier sistema operativo
https://docs.docker.com/desktop/
