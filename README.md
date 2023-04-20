# moccha-madness-final-project

## About
This is a software for a client, cafe business owner with multiple offline stores. The client's exisiting software generates daily sales data at a single store and does not provide compiled data of all stores to provide the overview of whole business performance and makes it hard to draw valuable insight such as how to target customers and the best-selling products. This software will deliver ETL pipeline; extracting sales data from client's source, transforming data, and loading on client's data warehouse. 
<br>
> **Current Client Setup**
- CSV file for each branch
- File Generation Time: 8 p.m
- Daily, Weekly, Montlhy Reports (on sales, other business metrics)
- Time-consuming Collation of all CSV files

> **Vision**
- The new software should load CSV file on Cloud every night.
- The new software should have ETL pipeline.
- The new software should have monitoring system.

## Elevator Pitch:

- **For** cafe business owner with multiple branches
- **who** wants to see the whole picture of their business <br>
- (targeting customers, the best-selling products, etc) in all branches <br>
- **the** new software <br>
- **is** a customer facing software <br>
- **that** allows customers to collate all data from each stores and gain valuable business insight in a timely manner<br>
- **unlike** the current software which is limited to sales tracking of one store at a time and data collation is time-consuming.<br>
- **our product** will allow customers to utilise their sales data to drive business growth.


## Authors
----------
Developers
- Sam Feighery   [Linkedin](https://www.linkedin.com/in/sam-feighery-b5265126/) | [Github](https://github.com/Sam-Feighery)<br>
- Kendrick Filho   [Linkedin](https://www.linkedin.com/in/misael-filho/) | [Github](https://github.com/mkmfilho/)<br>
- Ife Adeoti  [Github](https://github.com/S44WSA)<br>
- Dana Kim   [Linkedin](https://www.linkedin.com/in/haneul-kim-987b7744/) | [Github](https://github.com/ttcielott/)<br>
- Rishi Ravindran  [Linkedin](https://www.linkedin.com/in/rishiram-ravindran-a00127238/) | [Github](https://github.com/Rishi06R)<br>
----------


### Some basic Git commands are:
```
git status
git add
git commit
```

### Comands to setup docker
```
cd database
docker compose up -d
```

### Creating venv 
```
Windows - py -3.10 -m venv .venv
Mac - python3.10 -m venv .venv
```


### Activating venv
```
Windows - .venv/Scripts/Activate.bat
Mac - source .venv/bin/activate
``` 


### Install packages from requirments 
```
cd main_files
pip install -r requirements.txt
```

### Comands to run the application
```
cd main_files
py main_display.py
```