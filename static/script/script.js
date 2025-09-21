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
    if(el.classList.contains("overdue")){
            el.style.backgroundColor = "#dc3545"; 
            el.style.width = "100%";
        
    } else {
    let start = new Date(el.dataset.start);
    let end = new Date() ;
    if(el.classList.contains("complete")){
        end = new Date(el.dataset.completed);
    }
    let diffDays = Math.floor((end - start) / (1000 * 60 * 60 * 24));
    let deadline = parseInt(el.dataset.deadline, 10);
    let percent = ((diffDays / deadline) * 100);
    console.log((start- end)/(1000 * 60 * 60 * 24));
    console.log(diffDays, deadline, percent);
    el.style.width = (diffDays > 0) ? (percent >= 100)?(100 + "%"):(percent + "%") : "1%" ;
    if (percent < 25) {
        el.style.backgroundColor = "#28a745";
    } else if (percent < 50) {
        el.style.backgroundColor = "#ffc107"; 
    } else if (percent < 75) {
        el.style.backgroundColor = "#fd7e14"; 
    } else if( percent <= 100) {
        el.style.backgroundColor = "#dc3545"; 
        if (percent == 100) {
            el.classList.add("overdue");
        }
    } 
}
    
});

let toggle = document.querySelector("#togglePassword");
let toggleConfirm = document.querySelector("#togglePasswordConfirm");
if (toggle)
toggle.addEventListener("click", function () {
    console.log('yu[p')
        let input = document.getElementById("floatingPassword");
        if (input.type === "password") {
            input.type = "text";
            this.classList.remove("fa-eye");
            this.classList.add("fa-eye-slash");
        } else {
            input.type = "password";
            this.classList.remove("fa-eye-slash");
            this.classList.add("fa-eye");
        }
    });

if (toggleConfirm)
toggleConfirm.addEventListener("click", function () {
        let input = document.getElementById("confirm_new_password");
        if (input.type === "password") {
            input.type = "text";
            this.classList.remove("fa-eye");
            this.classList.add("fa-eye-slash");
        } else {
            input.type = "password";
            this.classList.remove("fa-eye-slash");
            this.classList.add("fa-eye");
        }
    });

function Done(id){
    let taskCard = document.getElementById(id);
    taskCard.classList.add("complete");
}

let achievment = document.getElementById("achievment-line");
if(achievment){
    let acheived = parseInt(achievment.getAttribute("acheived"));
    let total = parseInt(achievment.getAttribute("total"));
    let percent = (total == 0) ? 0 : Math.floor((acheived / total) * 100);
    achievment.style.width = percent + "%";
    achievment.classList.add("bg-success");

}

let home = document.getElementById('home')
let features = document.getElementById('features')
let about = document.getElementById('about')
let us = document.getElementById('why-us')
let nav = document.querySelectorAll('header ul li a')
if(us){
    document.onscroll = () => {
        nav.forEach((nv) => {
        nv.classList.remove('link-secondary')
    })
    if(window.scrollY - parseInt(home.style.marginTop) <= home.offsetHeight){
        nav[0].classList.add('link-secondary')
    } else if(Math.round(window.scrollY - parseInt(home.style.marginTop)) < home.offsetHeight + features.offsetHeight) {
        nav[1].classList.add('link-secondary')
    } else if(window.scrollY - parseInt(home.style.marginTop) <= home.offsetHeight + features.offsetHeight + about.offsetHeight) {
        nav[2].classList.add('link-secondary')
    } else {
        nav[3].classList.add('link-secondary')
    }
    }
    
}