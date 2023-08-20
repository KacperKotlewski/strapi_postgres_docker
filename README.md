to be done



required python and docker compose installed on the machine


how to run:
run the following command in the terminal to create .env file, follow instructions in the terminal:
```
python3 env_creator.py
```

developement mode:
```
source dev.build
```

production mode:
```
source build
```

all data will be saved under folder app_data (both database and strapi data)

to copy data from one computer to other:
```
    ssh -r user@ip_of_source_machine:~/location/to/application/app_data user@ip_of_destination_machine:~/location/to/paste
```
or to copy from remote to local:
```
    scp -r user@ip_of_source_machine:~/location/to/application/app_data .
```
or to copy from local to remote:
```
    scp -r app_data user@ip_of_destination_machine:~/location/to/paste
```