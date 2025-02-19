## Requisitos para la instalación
* Tener una versión de python 3.10.12 o superior
* Tener una versión de docker 26.0.0 o superior
* Tener cuenta en github

## Instalación FeedCycle
Estas instalaciones funcionan tanto para Windows como para Linux
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
