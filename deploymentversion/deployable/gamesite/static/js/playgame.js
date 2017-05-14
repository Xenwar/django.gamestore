$(document).ready(function() {
    //How do we get player specific infor and game specific info
    var player_id = 5;
    var gamename  = 'game1'
    'use strict';
    $(window).on('message', function(evt) {
      var data = evt.originalEvent.data;
      //determine message type
      /*
          Get the score and save it,
          if value is bigger than current max for the game, then save it.
          if not save it for the palyer
      */
      if (data.messageType === "SCORE"){
          newData = {}
          newData.messageType = data.messageType;
          newData.score       = data.score;
          newData.player_id   = player_id
          //only for debugging purpose.
          var score = data.score;
          console.log("Sending new score to the platform, ", JSON.stringify(data));
          //
          var newItem = '\n\t<li>' + (JSON.stringify(data) || '') + '</li>';
          $('#actions').prepend(newItem);
          //sending request to the server.
          console.log(newData)
            $.ajax({
                "type": 'POST',
                //"contentType": 'application/json; charset=utf-8',
                "url": 'http://127.0.0.1:8000/gamesite/savescore/' + gamename + '/',
                "data": newData,
                //crossDomain:true,
                success: function(result) {
                        console.log(result);
                },error: function(result) {
                    console.log(result);
                }
          });//ending ajax
            console.log(JSON.stringify(data)+'--------------------')
      }
      /*
          message contains items and score.
          send the message to the server,
          validatin also done on the server.
          validation on client not required, at least the input methods are save unless manipulated.
      */
      if (data.messageType === "SAVE"){
        console.log("Sending new save request to the platform, ", JSON.stringify(data));
          var newItem = '\n\t<li>' + (JSON.stringify(data) || '') + '</li>';
          $('#actions').prepend(newItem);
          //make a new data that is flattened.
          newData = {}
          newData.messageType = data.messageType;
          newData.playerItems = data.gameState.playerItems.join('@');
          newData.score       = data.gameState.score;
          newData.player_id   = player_id

          console.log(newData)
          $.ajax({
                "type": 'POST',
                //"contentType": 'application/json; charset=utf-8',
                "url": 'http://127.0.0.1:8000/gamesite/savestate/' + gamename + '/',
                "data": newData,
                //crossDomain:true,
                success: function(result) {
                        console.log(result);
                },error: function(result) {
                    console.log(result);
                }
          });//ending ajax
      }
      /*
        Retrieve everything the game has on the server.
        Then what ?
          How to give it back the state ?
          How to show game content for the player ?
      */
      if (data.messageType === "LOAD_REQUEST"){
          newData = {}
          newData.messageType = data.messageType;
          newData.player_id   = player_id
        console.log("Sending state load request to the platform, ", JSON.stringify(data));
        var newItem = '\n\t<li>' + (JSON.stringify(data) || '') + '</li>';
        $('#actions').prepend(newItem);

            $.ajax({
                "type": 'POST',
                //"contentType": 'application/json; charset=utf-8',
                "url": 'http://127.0.0.1:8000/gamesite/loadrequeset/' + gamename + '/',
                "data": newData,
                //crossDomain:true,
                success: function(result) {
                        //what to do with the result
                        console.log("load message arrived")
                        console.log(JSON.stringify(result));
                },error: function(result) {
                    console.log(result);
                }
          });//ending ajax
      }
      /*
          Handle resolution related request
          Either retrieve a game with the given resolution
          Or simulated by changing the iframe width and height.
          This seems to be the only one handled not on the server side.
      */
      if (data.messageType === "SETTING"){
          newData = {}
          newData.player_id   = player_id

          newData.messageType = data.messageType;
          newData.width       = data.options.width
          newData.height      = data.options.height;
            console.log("Sending SETTING request to the platform, ", JSON.stringify(data));
            var newItem = '\n\t<li>' + (JSON.stringify(data) || '') + '</li>';
            $('#actions').prepend(newItem);

                $.ajax({
                    "type": 'POST',
                    //"contentType": 'application/json; charset=utf-8',
                    "url": 'http://127.0.0.1:8000/gamesite/loadsetting/' +gamename +  '/',
                    "data": newData,
                    //crossDomain:true,
                    success: function(result) {
                            //what to do with the result
                            var width  = result.options.width
                            var height = result.options.height
                            console.log(JSON.stringify(result));
                            $("#gameframe").width(width);
                            $("#gameframe").height(height);
                    },error: function(result) {
                        console.log(result);
                    }
              });//ending ajax
      }
    });
  });