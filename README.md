#SevenTweets

SevenTweets is a network of mini services that should resemble twitter. Each service that
will be part of SevenTweets can have different implementation but will be built to support
a standardised API so that the communication between services can be possible. Every
node in SevenTweets would:
- Be a separate service
- Be able to work with tweets (published message)
- Have its own identificator (username)
- Have its own local storage for tweets originating from that node
- Have to know addresses of all other nodes
- Perform notifications to other nodes when starting/shutting down

##API
```
- GET /tweets
  - Returns: [{"id": 1, "name": "zeljko", "tweet": "this is tweet"}, …]
  - Status code: 200
- GET /tweets/<id>
  - Returns: {‘id’:’...’, ‘name’:’...’, ‘tweet’:’...’ }
  - Status code : 200
- POST /tweets
  - Body: {'tweet': '...'}
  - Returns: {‘id’:’...’, ‘name’:’...’, ‘tweet’:’...’ }
  - Status code: 201
- DELETE /tweets/<id>
  - Status code 204
```