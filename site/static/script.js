async function addFlag(x, y){
    await fetch("/api/addflag/"+ x + "/" + y, {
        "method": "POST"
    }).then(response => {
        console.log(response.status);
        return response.json();
    }).then(data => {
        if(data.message == "OK"){
            window.location.reload();
        }
        else{
            document.querySelector(".alert").hidden = false;
            document.querySelector(".alert").className = "text-center alert alert-danger";
            document.querySelector(".alert").innerHTML = data.message;
        }
    })
}

async function clearSession(){
    await fetch("/api/clear", {
        "method": "POST"
    }).then(response => {
        console.log(response.status);
        window.location.reload();
        return response.json();
    });
}
async function onButtonClick(x, y){
    await fetch("/api/" + x + "/" + y, {
        "method": "POST"
    }).then(response => {
        console.log(response.status);
        return response.json();
    }).then(data => {
        if(data.message == "You lost"){
            document.querySelector(".alert").hidden = false;
            document.querySelector(".alert").className = "text-center alert alert-danger";
            document.querySelector(".alert").innerHTML = "You lost";
        }
        else if(data.message == "You won"){
            document.querySelector(".alert").hidden = false;
            document.querySelector(".alert").className = "text-center alert alert-success";
            document.querySelector(".alert").innerHTML = "You won";
            document.getElementById("scoreboard").hidden = false;
        }
        else if(data.message == "OK"){
            window.location.reload();
        }
        else{
            document.querySelector(".alert").hidden = false;
            document.querySelector(".alert").className = "text-center alert alert-danger";
            document.querySelector(".alert").innerHTML = data.message;
        }
    })
}