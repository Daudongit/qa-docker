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
step 2: make runtest.sh executable
```
sudo chmod +x runtest.sh
```
step 3: create a container to run the test
```
sudo ./runtest.sh  [https://stage.linuxjobber.com]  [your-image-tag-here]
```
Note from the above command if [https://stage.linuxjobber.com] is not specify [https://int.linuxjobber.com] will be use and if [your-image-tag-here] is not specify [qaserver] will be use