let isFile = true;

$(document).ready(function() {

   document.getElementById('paths').style.display = "none";
   document.getElementById('lists').style.display = "none";
   document.getElementById('labels').style.display = "none";
   document.getElementById('device-button').style.display = "none";
   
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


   $.ajax({
      type: 'GET',
       url: '/load/',
      success: function(response) {
         $('#project').val(response.project);
         $('#dll').val(response.dll);
         $('#lib').val(response.lib);
       }

   });


   

   
});


function file() {   

   if(!isFile)
   {
      document.getElementById('paths').style.display = "none";
      document.getElementById('lists').style.display = "none";
      document.getElementById('labels').style.display = "none";
      document.getElementById('device-button').style.display = "none";
      document.getElementById('import-button').style.display = "inline-block";
   }
   else
   {
      document.getElementById('paths').style.display = "block";
      document.getElementById('lists').style.display = "block";
      document.getElementById('labels').style.display = "block";
      document.getElementById('device-button').style.display = "inline-block";
      document.getElementById('import-button').style.display = "none";
   }


   isFile = !isFile;

}

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
            $('#project').val(response.project);
         }
      });
    }  

    function selectDLL() {   
      $.ajax({
         type: 'GET',
         url: '/selectdll/',
         success: function(response) {
            $('#dll').val(response.dll);
         }
      });
    }  

    function selectLib() {   
      $.ajax({
         type: 'GET',
         url: '/selectlib/',
         success: function(response) {
            $('#lib').val(response.lib);
         }
      });
    }  

    function importExcel() {

      $.ajax({
         type: 'GET',
         url: '/importExcel/',
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



    function save(){

      let project = $('#project').val();
      let dll = $('#dll').val();
      let lib = $('#lib').val();

     
      let obj = {
         project: project,
         dll: dll,
         lib: lib
     };


     $.ajax({
     type: 'POST',
     url: '/saveFile/',
     data: obj,
     success: function(response) {
         console.log(response.data);
      }

   });

    }

    function change(){

      $.ajax({
         type: 'GET',
         url: '/interface/',
         success: function(response) {
         }
      });
    }

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



