# Energy Management System (EMS)

## Introduction
A program that uses tools like Python, MySQL, Docker and Angular in its development.

EMS will provide the following services:
* Optimal day-ahead dispatch of the available distributed energy resources (DER);
* Monitoring and management of CampusGrid microgrid, modeled and simulated in the Typhoon HIL (Hardware in the Loop);
* Microgrid operation data is stored in a MySQL database;
* Real-time visualization of microgrid operation;
* Visualization of dispatchs defined by the economic dispatch optimizer;
* Configuration of hourly energy prices from the main network, thermal generation costs and load curtailment costs.
    
## Architecture

![alt text](https://labrei.dsce.fee.unicamp.br:6498/merge/e75_software_gestao_microrredes/-/raw/master/arquitetura.PNG)

## Installation

- Make sure [Git](https://git-scm.com/downloads), [Docker](https://docs.docker.com/get-docker/) and [Docker-Compose](https://docs.docker.com/compose/install/) are installed on your computer;

- Clone the repository:

    `$ git clone https://gitlab.com/j262748/e75_software_gestao_microrredes.git`

- Run the file rebuild.sh:

    `$ sudo ./rebuild.sh`

## Inner Execution:

- Frontend - open the browser at http://localhost:4202
- EMS API Backend - open the browser at http://localhost:8051




## Acknowledgment
This work is developed under the Electricity Sector Research and Development Program PD-00063-3058/2019 - PA3058: "MERGE: Microgrids for Efficient, Reliable and Greener Energy", regulated by the National Electricity Agency (ANEEL in Portuguese), in partnership with CPFL Energia (Local Electricity Distributor).


## People involved
Jéssica Alice A. Silva
Email: j262748@dac.unicamp.br

Juan Camilo López
Email: jclopeza@unicamp.br

Cindy Paola
Email: cindy19gl@gmail.com 




