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
     
            //alert('Starting TIA Portal!');
            $("#myModal").modal();
           
         }
         ,
        error: function (xhr, ajaxOptions, thrownError) {
            document.getElementById('error').innerHTML = "There must be at least one device. Project path missing?";
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
        

            let typeArr = response.type;
            let nameArr = response.name;

            const laskuri = document.getElementsByClassName("laskuri");
            const panel = document.getElementsByClassName("panel panel-primary");
    
            let myHTML = '';
          
            for (let i = 0; i < typeArr.length; i++) {
             
              myHTML += '<div class="panel-heading">'+nameArr[i]+'<img id='+nameArr[i]+' src="static/images/delete.png" alt="delete-button" width="20" height="20" style="float: right;" onclick="select(this.id)"></div>';
              myHTML += '<div class="panel-body">'+typeArr[i]+'</div>';
    
            }
          
            panel[0].innerHTML = myHTML

            laskuri[0].innerHTML = '<h4>Added devices ('+typeArr.length+')</h4>';

         }
      });
   }  

   function addList(value) {   
        $('#type').val(value);
    }  
    
    function openproject() {   
      $.ajax({
         type: 'GET',
         url: '/openproject/',
         success: function(response) {
            
         }
      });
    }  


    $.getJSON('static/data.json', function(data) {
        console.log(JSON.stringify(data.devices));

        let arr = data.devices;

        const wrapper = document.getElementsByClassName("list-group");

        let myHTML = '';
      
        for (let i = 0; i < arr.length; i++) {
         
          myHTML += '<a type="button" onClick="addList(\''+arr[i]+'\')" class="list-group-item">'+arr[i]+'</a>';

        }
      
        wrapper[0].innerHTML = myHTML
      
    });

    function select(name){
      console.log(name);

      $.ajax({
         type: 'POST',
         url: '/delete/',
         data: {"name":name},
         success: function(response) {

            let typeArr = response.type;
            let nameArr = response.name;

            const laskuri = document.getElementsByClassName("laskuri");
            const panel = document.getElementsByClassName("panel panel-primary");
    
            let myHTML = '';
          
            for (let i = 0; i < typeArr.length; i++) {
             
              myHTML += '<div class="panel-heading">'+nameArr[i]+'<img id='+nameArr[i]+' src="static/images/delete.png" alt="delete-button" width="20" height="20" style="float: right;" onclick="select(this.id)"></div>';
              myHTML += '<div class="panel-body">'+typeArr[i]+'</div>';
    
            }

            if(typeArr.length == 0) {
               myHTML += '<div class="panel-body">Empty list!</div>';
            }
          
            panel[0].innerHTML = myHTML

            laskuri[0].innerHTML = '<h4>Added devices ('+typeArr.length+')</h4>';
         }

      });


    }