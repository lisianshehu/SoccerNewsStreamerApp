# SoccerNewsStreamerApp

A small web application made using Flask and SocketIO to stream tweets in real-time using Twitter's StreamListener API

## Installation
Repository can be cloned by:
1. Using the Github UI
2. `git clone https://github.com/lisianshehu/SoccerNewsStreamerApp.git`

## Usage Example
1. This can be used to view live tweets based on a keyword or set of keywords specified 
2. Can be used as a example or component to be added to a more wholesome web application 

## Development Setup
The following steps will setup your development environment so you are able to make changes and run the web application:
1. Apply for a developer account on https://developer.twitter.com/
2. Once you receive your developer API credentials, make a `.env` file in the `app` directory
3. In the `.env` file you will add a few environment variables including your credentials and a comma separated list that will act as the keyword for the StreamListener
    - Here is an example of a .env file:
    
       `CONSUMER_KEY="YOUR CONSUMER KEY"
       
        CONSUMER_SECRET="YOUR CONSUMER SECRET"
        
        ACCESS_TOKEN="YOUR ACCESS TOKEN"
        
        ACCESS_TOKEN_SECRET="YOUR TOKEN SECRET"
        
        KEYWORD_LIST="premier league,champions league"`
    - Replace your credentials in the first four lines and customize the keyword list to your preference
4. Now the Dockerfile can be used to build and run the application
5. Use the following command to build the Dockerfile: `docker build -t twitterstream:1.0 .`
6. Once built use the following command to run the Dockerfile: `docker run -it --publish 8080:8080 --name streamapp twitterstream:1.0`
7. The server should start and you should be able to access the web app on port 8080 on your localhost
8. Tweets should be streaming and debugging can be done through the console or through the log file 

## Release History

* v1.0
    * Basic web application functionality that streams tweets in real-time using Twitter's StreamListener API
    
* v2.0
    * Improved web application that uses a HashSet to keep track of duplicate tweets for better runtime efficiency
    * Uses Dockerfile to build and run web server on port 8080
    * Uses .env file to use user credentials and customization of keyword-search for tweets to track
