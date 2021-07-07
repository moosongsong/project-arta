function message_alert(title, contents) {
    swal(title, contents, title);
}

function openNav() {
    var mql = window.matchMedia("screen and (min-width: 992px)");

    if (mql.matches) {
        document.getElementById("mySidenav").style.width = "300px";
    } else {
        document.getElementById("mySidenav").style.width = "180px";
    }

    document.getElementById("mySidenav").style.borderRight = "2px solid #5CA4A2";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("mySidenav").style.borderRight = "none";
}