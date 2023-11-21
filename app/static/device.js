


$(document).ready(function() {


   /*
   const title = document.getElementById("title");

   let datatext = '<img src="../static/images/delete.png" alt="delete-button" width="20" height="20" style="float: right;" onclick="select(this.id)" />';
   
   title.innerHTML = datatext;
   */

   $.ajax({
      type: 'GET',
       url: '/directory/',
      success: function(response) {
      
         const directory = document.getElementById("hakemisto");
    
         let myHTML = '';
      
      
      /*
         let files = '<li id="tag" role="treeitem" aria-selected="false" class="doc" draggable="true" ondragstart="drag(event)">Devices</li>';

         for (let i = 0; i < 3; i++) {
      
            myHTML += '<li id="div'+i+'" role="treeitem" aria-expanded="false" aria-selected="false" ondrop="drop(event)" ondragover="allowDrop(event)" draggable="true" ondragstart="drag(event)" tabindex="0"><span> '+1+' </span><ul role="group" >'+files+'</ul></li>';
         
         }

         directory.innerHTML = myHTML;


 */

         let files = '';

         let arr = Object.values(response)
         let keys = Object.keys(response);
         
         
           for (let i = 0; i < keys.length; i++) 
           {
             let k = arr[i]
             console.log("directory: " + keys[i]);

             if(k != undefined)
             {
               for (let a = 0; a < k.length; a++) 
               {
                   console.log("file: " + k[a]);
                   files += '<li id="tag" role="treeitem" aria-selected="false" class="doc" draggable="true" ondragstart="drag(event)">'+k[a]+'</li>';
               }
             }
            

             myHTML += '<li id="div'+i+'" role="treeitem" aria-expanded="false" aria-selected="false" ondrop="drop(event)" ondragover="allowDrop(event)" draggable="true" ondragstart="drag(event)" tabindex="0"><span> '+keys[i]+' </span><ul role="group" >'+files+'</ul></li>';
             files = '';
             
           }



           directory.innerHTML = myHTML;



       }
      

   });


  





    $('#tiaportal').submit(function(event) {
       event.preventDefault();
       $("#myModal2").modal();
       $.ajax({
          type: 'POST',
          url: '/tiaportal/',
          data: $('#tiaportal').serialize(),
          success: function(response) {
             $('#type').val('');
             $('#name').val('');
      
             //alert('Starting TIA Portal!');
          
            
          }
          ,
         error: function (xhr, ajaxOptions, thrownError) {
             document.getElementById('error').innerHTML = "There must be at least one device. Project path missing?";
             document.getElementById('error-message').style.display = "block";
       }
       });
    });
 
    $('#initPortal').submit(function(event) {
      event.preventDefault();
      $("#myModal").modal();
      $.ajax({
         type: 'POST',
         url: '/initPortal/',
         data: $('#initPortal').serialize(),
         success: function(response) {
            $('#type').val('');
            $('#name').val('');
     
            //alert('Starting TIA Portal!');
            if (response.tia == 1)
            {
              document.getElementById('device-button').removeAttribute("disabled");
              document.getElementById('compile-button').removeAttribute("disabled");

              const wrapper = document.getElementsByClassName("list-group");

              let myHTML = '';

              let arr = response.dlist;
            
              for (let i = 0; i < arr.length; i++) {
               
                myHTML += '<a type="button" onClick="addList(\''+arr[i]+'\')" class="list-group-item">'+arr[i]+'</a>';
          
              }
            
              wrapper[0].innerHTML = myHTML

            }
           
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

    $.ajax({
      type: 'GET',
       url: '/tia/',
      success: function(response) {
         if (response.tia == 1)
         {
           document.getElementById('device-button').removeAttribute("disabled");
           document.getElementById('compile-button').removeAttribute("disabled");

           const wrapper = document.getElementsByClassName("list-group");

           let myHTML = '';

           let arr = response.dlist;
         
           for (let i = 0; i < arr.length; i++) {
            
             myHTML += '<a type="button" onClick="addList(\''+arr[i]+'\')" class="list-group-item">'+arr[i]+'</a>';
       
           }
         
           wrapper[0].innerHTML = myHTML
         }
       }

   });
 
 });

 /*
 $.getJSON('../static/data.json', function(data) {
    console.log(JSON.stringify(data.devices));

    let arr = data.devices;

    const wrapper = document.getElementsByClassName("list-group");

    let myHTML = '';
  
    for (let i = 0; i < arr.length; i++) {
     
      myHTML += '<a type="button" onClick="addList(\''+arr[i]+'\')" class="list-group-item">'+arr[i]+'</a>';

    }
  
    wrapper[0].innerHTML = myHTML
  
});
*/

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


