# Installation Instructions

Since Prastut was working on Teem and with the help of Pablo we were able to integrate the teem-tag environment with SwellRT, so this module builds upon the same workflow. 

## Dependencies

* Git to download the teem repository and teem-tag's repository.  
* Node.js (v4.2.x) to run the code, and npm (node.js's package manager) to install the dependencies.
* You need [Docker](https://docs.docker.com/engine/installation/) (v1.9.x) to pull the images and setup the environment for all these interacting containers to work with each other (swellrt->mongo, swellrt->teemtag, teemtag->swellrt etc.) 

Add your user into the `docker` group to have the necessary permissions. In GNU/Linux, try:

```
wget -qO- https://get.docker.com/ | sh
sudo usermod -aG docker <your_user>
```

And then restart your computer.


## Setup Environment


### Work related with setting up teem:

*  Clone teem.

  Clone the teem repository using `git`:
  
  ```
  git clone https://github.com/P2Pvalue/teem.git
  cd teem
  ```

* Checkout tagger branch.
  ```
  git fetch <origin or upstream based on your remote>
  git checkout tagger
  ```

* Install dependencies related to Teem. 
  
  Please ensure that you are working on the tagger branch.
  Since teem has progressed ahead, this module might not work with the dependencies that the new code would have.
  
  * To check current branch:
    ```
    git branch
    
    tagger <- this would be highlighted in green
    master
    ```
  
  * After confirming that you are on the tagger branch, run:
  
    ```
    npm install
    ```
    
    Behind the scenes this will also call `bower install`.  You should find that you have two new
    folders in your project.
    
    * `node_modules` - contains the npm packages for the tools we need
    * `bower_components` - contains the angular framework files
    
  * You also need to install `gulp` which runs a simple development web server. 
  
    ```
    sudo npm install -g gulp
    ```

### Work related with Docker:

We are using multi-container application for Docker. You also need to install [docker-compose](https://docs.docker.com/compose/install/). Pull the following images:

```
docker pull p2pvalue/swellrt:0.51.3-alpha
docker pull mongo:latest
docker pull p2pvalue/teemtag:v1.2
```
Note: As far as we know, the [HTTP Event Dispatcher module](https://github.com/P2Pvalue/swellrt/blob/master/wave/doc/swellrt/Event-Dispatcher.md) of SwellRT is only inside `0.51.3-aplha` tag, that's why we are asking you to pull this image.
  
  
### Setting up the multi-container architecture:

* `cd` inside the cloned teem repository.

  ```
  cd teem
  ```
* Run `gulp`

  ```
  gulp
  ```
  
  * Notice the logs which shows the containers built from the images we just pulled as running:
    ```
    [01:59:00] Server started http://0.0.0.0:8000
    [01:59:00] LiveReload started on port 35729
    [01:59:00] Container teem-swellrt-mongo exists
    [01:59:00] Container teem-swellrt-mongo is stopped
    [01:59:00] Container teem-swellrt-teemtag exists
    [01:59:00] Container teem-swellrt-teemtag is stopped
    [01:59:03] Starting teem-swellrt-mongo
    [01:59:03] 
    [01:59:03] Starting teem-swellrt-teemtag
    [01:59:03] 
    [01:59:03] Container teem-swellrt exists
    [01:59:03] Container teem-swellrt is stopped
    [01:59:07] Starting teem-swellrt

    ```
  
  * Since we need to modify these containers, fire up a new terminal and stop them: 
    
    Note: Don't stop gulp, keep it running. 
    
    ```
    docker ps
    
    // Look under the names category
    teem-swellrt-teemtag
    teem-swellrt-mongo
    teem-swellrt
    
    ```
    To stop these containers:
    
    ```
    docker stop teem-swellrt-teemtag
    docker stop teem-swellrt-mongo
    docker stop teem-swellrt
    ```
    
* Now `cd` inside swellrt folder inside teem repository. 
    ```
    pwd
    // /<path leading to team repo>/teem/
    
    ls
    bower_components    config.js.sample  LICENSE       README.md  test
    bower.json          cordova           node_modules  src        www
    CODE_OF_CONDUCT.md  gulpfile.js       package.json  swellrt

    cd swellrt
    
    ```
* Fire multi-container application setup using `docker-compose`:
    ```
    pwd
    // /<path leading to team repo>/teem/swellrt
    
    docker-compose up
    ```
    
    
* Now fire up another terminal. We need to copy some application files inside the SwellRT container inorder for the HTTP Dispatcher to work:
    
    ```
    docker ps
    //Find the swellrt container name
    ```
    Now copy the config files. Command format:
    ```
    docker cp <file name> <swellrt_container name>:/usr/local/swellrt/config
    ```
    Example (Replace `swellrt_swellrt_1` with your container name by finding it from `docker ps`):
    ```
    docker cp application.conf swellrt_swellrt_1:/usr/local/swellrt/config
    docker cp event.rules.config swellrt_swellrt_1:/usr/local/swellrt/config
    ```
    
* Now restart the docker container inorder for it to process these changes:
  (Replace `swellrt_swellrt_1` with your container name by finding it from `docker ps`):
    ```
    docker restart swellrt_swellrt_1
    ```

As far as we can hope and you get lucky, you will have setup everything related to this module.

### Magic Time: 

* Now fire up your favourite web browser. Goto to `localhost:8000` where teem is running.

* Make 2 accounts one for yourself, other for teem-tag for authentication purposes with the following credentials:
    ```
    Username: teemtag
    Password: teemtag
    ```

* We recommend tiling your screens like this to see the preview 
  * The left screen is the terminal running `docker-compose up`  
  
![image](https://cloud.githubusercontent.com/assets/10279686/18765927/6dddd824-8135-11e6-8816-deedbf04509d.png)

* Now make any community and fill the name of the community and the description. When you notice closely inside the logs, the tags and the summary would be visible to you. 

## TLDR process is:
  * SwellRT using the `rules.event.config` and `application.conf` makes a POST request with `name` and `description` to `teem-tag` container as soon as the MAP_ENTRY_UPDATED flag gets high.
  * The `teem-tag` container recieves the POST request, finds the `name` and `description` from the JSON recieved from SwellRT and then processes it to generate the tags as well as the summary of the content. 
