# MESSAGE API
POSMAN LINK : https://documenter.getpostman.com/view/15212272/TzCQaRcq

HOSTED LINK : https://pacific-stream-26613.herokuapp.com/

Running Instructions:
--------------------

1. The postman link above include some requests example , you can try it out.
2. please note that the signup and login method already run, and the rest of te request methods is rely on the token from this session,
if you are intrested to signup a new user and login or to login again to exist user, please take the token from response of the login reques and replace it in the header Authorization for every request that you like to run

Postman Examples Explanation:
--------------------

1. /signup :
 
            description: Create a new user in the system
            headrs: Content-Type: application/json
            method: POST
            body: { user_name:<>, email:<>, password:<> }
            examples: signup user 1, signup user 2
            results : status message
      
2./login :

            description: login to exist user
            headrs: Content-Type: application/json
            method: POST
            body: { email:<>, password:<> }
            examples: login user 1, login user 2
            results : token
      
important: the next requests must have a token for the specific login session in the Authorization header   
--
3./users/<int:user_id>/message :

            description: sent message
            headrs: Content-Type: application/json , Authorization: <token>
            method: POST
            body: { receiver_id:<>, message:<> , subject:<> }
            params: { sender user_id }
            examples: sent message from 1 to 2, sent message from 1 to 2 for delete as a sender,sent message from 2 to 1
            results : {
              "message": message,
              "status": 200
          }
      
4./users/<int:user_id>/messages :

            description:get all messages for user
            headrs: Content-Type: application/json , Authorization: <token>
            method: Get
            body: { unread : 0 }
            params: { user_id }
            examples: get all messages of user 1, get all messages of user 2
            results : {
              "messages": user_messages,
              "status": 200
            }

5./users/<int:user_id>/messages/<int:message_id> :

            description: read message
            headrs: Content-Type: application/json , Authorization: <token>
            method: PATCH
            params: { user_id , message_id }
            examples: read message of user 2
            results : {
              "message": message,
              "status": 200
          }
  
6./users/<int:user_id>/messages : 

            description:get unread messages for user
            headrs: Content-Type: application/json , Authorization: <token>
            method: Get
            body: { unread : 1 }
            params: { user_id }
            examples: get unread messages of user 2
            results : {
              "messages": user_messages,
              "status": 200
            }
  
7./users/<int:user_id>/messages/<int:message_id> : 

            description: delete message as a reciver or as a sender
            headrs: Content-Type: application/json , Authorization: <token>
            method: DELETE
            params: { user_id , message_id }
            examples: delete meesage of user 1 as a receiver, delete meesage of user 1 as a sender
            results : {
              "status": 200
            }  
