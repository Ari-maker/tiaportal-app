$(document).ready(function () {

   $.ajax({
      type: 'GET',
      url: '/getDevices/',
      success: function (response) {

         if (response.name.length <= 0)
            return;

         let typeArr = response.type;
         let nameArr = response.name;

         const laskuri = document.getElementsByClassName("laskuri");
         const panel = document.getElementsByClassName("panel panel-primary");

         let myHTML = '';

         for (let i = 0; i < typeArr.length; i++) {

            myHTML += '<div class="panel-heading">' + nameArr[i] + '<img id=' + nameArr[i] + ' src="../static/images/delete.png" alt="delete-button" width="20" height="20" style="float: right;" onclick="select(this.id)"></div>';
            myHTML += '<div class="panel-body">' + typeArr[i] + '</div>';

         }

         panel[0].innerHTML = myHTML

         laskuri[0].innerHTML = '<h4>Added devices (' + typeArr.length + ')</h4>';

      }
   });

   $('#tiaportal').submit(function (event) {
      event.preventDefault();
      $("#myModal2").modal();
      $.ajax({
         type: 'POST',
         url: '/tiaportal/',
         data: $('#tiaportal').serialize(),
         success: function (response) {
            $('#type').val('');
            $('#name').val('');

         }
         ,
         error: function (xhr, ajaxOptions, thrownError) {
            document.getElementById('error').innerHTML = "There must be at least one device. Project path missing?";
            document.getElementById('error-message').style.display = "block";
         }
      });
   });

   $('#initPortal').submit(function (event) {
      event.preventDefault();
      $("#myModal").modal();
      $.ajax({
         type: 'POST',
         url: '/initPortal/',
         data: $('#initPortal').serialize(),
         success: function (response) {
            $('#type').val('');
            $('#name').val('');

            if (response.tia == 1) {
               document.getElementById('device-button').removeAttribute("disabled");
               document.getElementById('compile-button').removeAttribute("disabled");

               const wrapper = document.getElementsByClassName("list-group");

               let myHTML = '';

               let arr = response.dlist;

               for (let i = 0; i < arr.length; i++) {

                  myHTML += '<a type="button" onClick="addList(\'' + arr[i] + '\')" class="list-group-item">' + arr[i] + '</a>';

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
      success: function (response) {
         $('#project').val(response.project);
         $('#dll').val(response.dll);
         $('#lib').val(response.lib);
      }

   });

   $.ajax({
      type: 'GET',
      url: '/tia/',
      success: function (response) {

         if (response.tia == 1) {
            document.getElementById('device-button').removeAttribute("disabled");
            document.getElementById('compile-button').removeAttribute("disabled");

            const wrapper = document.getElementsByClassName("list-group");

            let myHTML = '';

            let arr = response.dlist;

            for (let i = 0; i < arr.length; i++) {

               myHTML += '<a type="button" onClick="addList(\'' + arr[i] + '\')" class="list-group-item">' + arr[i] + '</a>';

            }

            wrapper[0].innerHTML = myHTML
         }
      }

   });

});

function add() {
   $.ajax({
      type: 'POST',
      url: '/addDevice/',
      data: $('#tiaportal').serialize(),
      success: function (response) {
         $('#type').val('');
         $('#name').val('');

         window.location.href = "/device";
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
      success: function (response) {
         $('#project').val(response.project);
      }
   });
}

function selectDLL() {
   $.ajax({
      type: 'GET',
      url: '/selectdll/',
      success: function (response) {
         $('#dll').val(response.dll);
      }
   });
}

function selectLib() {
   $.ajax({
      type: 'GET',
      url: '/selectlib/',
      success: function (response) {
         $('#lib').val(response.lib);
      }
   });
}




function save() {

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
      success: function (response) {
         console.log(response.data);
      }

   });

}




function change() {

   $.ajax({
      type: 'GET',
      url: '/interface/',
      success: function (response) {
      }
   });
}

function select(name) {
   console.log(name);

   $.ajax({
      type: 'POST',
      url: '/delete/',
      data: { "name": name },
      success: function (response) {

         window.location.href = "/device";

      }

   });


}

function addDirectory() {

   let value = document.getElementById("folder").value;

   if (value == "")
      return;

   let obj = {
      foldername: value
   }

   $.ajax({
      type: 'POST',
      url: '/addDirectory/',
      data: obj,
      success: function (response) {

         window.location.href = "/device";

      }
   });



}