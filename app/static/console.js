let arr = [];

let keys = []

function addCommand(e) {   

    if(e.keyCode === 13){
        e.preventDefault(); // Ensure it is only this code that runs

        let x = document.getElementById("command").value;
        keys.push(x);
        arr.push(x);
        $('#command').val('');

        loopData();
    }


} 

function loopData() {  
    const consoleData = document.getElementsByClassName("media-body");

    let myHTML = '';
  
    for (let i = 0; i < arr.length; i++) {
         
        console.log(arr[i]);

        let sup = arr[i].replace(/["']/g, "");

        myHTML += '<p>'+sup+'</p>';

      }
  
      consoleData[0].innerHTML = myHTML
}


$(document).ready(function() {

    $.ajax({
        type: 'GET',
        url: '/getConsoleData/',
        success: function(response) {
            console.log("update");
            
            if (response.consoleArr == '[]')
                return;

            let result = response.consoleArr.replace(/\[|\]/g,'').split(',');

            let newArray = result.concat(keys);

            arr = newArray;

            loopData();

        }
     });

    setInterval(function() {

        $.ajax({
            type: 'GET',
            url: '/getConsoleData/',
            success: function(response) {
                console.log("update");
    
                

                let result = response.consoleArr.replace(/\[|\]/g,'').split(',');

                let newArray = result.concat(keys);
    
                arr = newArray;

                if (response.consoleArr == '[]')
                    arr = []

                loopData();
    
            }
         });
    
    }, 5000);

});