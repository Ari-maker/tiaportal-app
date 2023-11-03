
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

   
    function change(){

      $.ajax({
         type: 'GET',
         url: '/interface/',
         success: function(response) {
         }
      });
    }