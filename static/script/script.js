let welcome = document.getElementById("welcome");
if (welcome) {
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
    setInterval(typeWriter, 200)
}
// $("#right").on("click", function () {
//     $(".block").animate({ "left": "+=50px" }, "slow");
// });

descr = document.getElementById("description");
if (descr)
if (descr.value.length >= 200) {
    descr.style.borderColor = "red";
    descr.value = descr.value.substring(0, 200);
} else {
    descr.style.borderColor = "";
}

document.querySelectorAll(".timeline").forEach(el => {
    let start = new Date(el.dataset.start);
    let end = new Date(el.dataset.end) ;
    let diffDays = Math.floor((end - start) / (1000 * 60 * 60 * 24));
    let deadline = parseInt(el.dataset.deadline, 10);
    console.log(diffDays, deadline);
    if(diffDays > 0)
        el.style.width = (diffDays / deadline) * 100 + "%"
    else
        el.style.width = "1%" 
});
