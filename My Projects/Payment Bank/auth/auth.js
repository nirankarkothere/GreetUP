const card = document.getElementById("authCard");

function flipSignup(){
    card.classList.toggle("flipped");
    card.classList.remove("forgot-mode");
}

function flipForgot(){
    card.classList.toggle("forgot-mode");
    card.classList.remove("flipped");
}

function signupDone(){
    alert("Account Created Successfully!");
    flipSignup();
}

function resetDone(){
    alert("Reset link sent to your email!");
    flipForgot();
}
