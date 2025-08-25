let welcome = document.getElementById("welcome");
let msg = welcome.innerText;
let index = 0;  
welcome.innerText = "";
function typeWriter() {
    if (index < msg.length) {
        welcome.innerHTML += msg.charAt(index);
        index++;
    } else {
        clearInterval();
    }
}
setInterval(typeWriter,200)