$(document).ready(function() {
   $('#tiaportal').submit(function(event) {
      event.preventDefault();
      $.ajax({
         type: 'POST',
         url: '/tiaportal/',
         data: $('#tiaportal').serialize(),
         success: function() {
            $('#type').val('');
            $('#name').val('');
     
            alert('Starting TIA Portal!');
         }
         ,
        error: function (xhr, ajaxOptions, thrownError) {
            document.getElementById('error').innerHTML = "There must be at least one device";
            document.getElementById('error-message').style.display = "block";
      }
      });
   });

});

function add() {   
$.ajax({
         type: 'POST',
         url: '/add/',
         data: $('#tiaportal').serialize(),
         success: function(response) {
            $('#type').val('');
            $('#name').val('');
            document.getElementById('editType').innerHTML = response.type;
            document.getElementById('editName').innerHTML = response.name;
         }
      });
   }  

   function addList(value) {   
        $('#type').val(value);
    }  
    
    $.getJSON('static/data.json', function(data) {
        console.log(JSON.stringify(data.devices));

        let arr = data.devices;

        var wrapper = document.getElementsByClassName("list-group");

        var myHTML = '';
      
        for (var i = 0; i < arr.length; i++) {
         
          myHTML += '<a type="button" onClick="addList(\''+arr[i]+'\')" class="list-group-item">'+arr[i]+'</a>';

        }
      
        wrapper[0].innerHTML = myHTML
      
    });