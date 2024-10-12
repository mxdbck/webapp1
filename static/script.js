// Function to get a cookie by name
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

// Display the username
window.onload = function () {
  const username = getCookie("mycookie");
  if (username) {
    document.getElementById("username").textContent = username;
  } else {
    document.getElementById("username").textContent = "Guest";
  }
};

// JavaScript to change the text color of the heading when the button is clicked
document.getElementById("colorButton").addEventListener("click", function () {
  const heading = document.getElementById("greeting");
  const currentColor = heading.style.color;

  // Toggle the color between blue and red
  if (currentColor === "red") {
    heading.style.color = "blue";
  } else {
    heading.style.color = "red";
  }
});
