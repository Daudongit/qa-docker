# DOCKERIZE QA

Dockerize qa template for selenium testing

### Prerequisites

* selenium driver
* git
* docker

### setup

* create settings.ini file in setup folder(use settings.ini.example as template)
* create test folder
* clone the qa repository to test folder(with a parent folder name qa)

### step
step 1: build the image 
```
docker build -t your-image-tag-here your-directory-path-here
```
step 2: create a container to run the test
```
docker run [-e "ENVIRONMENT=int|stage"] [-e "WESITE=linuxjobber|chatscrum"] --name your-container-name your-image-tag-here
```
Note from the above command if environment variable ENVIRONMENT is not specify int will be use and if WEBSITE is not specify linuxjobber will be use