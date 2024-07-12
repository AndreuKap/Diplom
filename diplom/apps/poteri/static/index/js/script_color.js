

window.addEventListener("scroll", scrollnav);

function scrollnav() {
  var y = window.scrollY;
  if (y > 100) {
    document.getElementById("col").style.backgroundColor = "rgba(170,134,46,0.7)";
   
  } else {
    document.getElementById("col").style.backgroundColor = "unset";


  }
}