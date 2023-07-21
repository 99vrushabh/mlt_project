// dashboard
const menu = document.querySelector(".menu");
const menuBars = document.querySelector(".fa-bars");
const menuArrow = document.querySelector(".fa-arrow-up");
const flyoutWrap = document.querySelector(".flyout-wrap");
const flyouts = document.querySelectorAll(".flyout");
const formContainer = document.getElementById("form_section");
const loginForm = document.querySelector(".login-form");
const signupForm = document.querySelector(".signUp-form");
const loginButton = document.querySelector("#multiple-btn button:nth-child(1)");
const signupButton = document.querySelector("#multiple-btn button:nth-child(2)");

menu.addEventListener("click", function () {
  menuBars.classList.toggle("hidden");
  menuArrow.classList.toggle("hidden");
  flyouts.forEach((flyout) => {
    flyout.classList.toggle("flyout-out");
  });
});
k;

// form 
const inputs = document.querySelectorAll("input");
inputs.forEach(function (input) {
  input.addEventListener("focus", function () {
    const parentElement = input.parentElement.parentElement;
    parentElement.classList.add("box-animation");
  });
  input.addEventListener("blur", function () {
    const parentElement = input.parentElement.parentElement;
    parentElement.classList.remove("box-animation");
  });
});

const buttons = document.querySelectorAll("#multiple-btn button");
const form_container = document.getElementById("form_section");
buttons.forEach((button) => {
  button.addEventListener("click", () => {
    form_container.classList.toggle("left-right");
  });
});

// hide/show password 
loginForm.style.display = "block";
signupForm.style.display = "none";

// Add event listeners to buttons
loginButton.addEventListener("click", showLoginForm);
signupButton.addEventListener("click", showSignupForm);

// Function to show login form and hide signup form
function showLoginForm() {
  formContainer.classList.remove("left-right");
  loginForm.style.display = "block";
  signupForm.style.display = "none";
}

// Function to show signup form and hide login form
function showSignupForm() {
  formContainer.classList.add("left-right");
  loginForm.style.display = "none";
  signupForm.style.display = "block";
}

// Function to toggle password visibility
function togglePasswordVisibility(inputId, toggleBtnId) {
  var passwordInput = document.getElementById(inputId);
  var toggleButton = document.getElementById(toggleBtnId);

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    toggleButton.textContent = "Hide";
  } else {
    passwordInput.type = "password";
    toggleButton.textContent = "Show";
  }
}
window.addEventListener("load", function () {
  var loader = document.querySelector(".loader");
  loader.style.display = "none";
});
var parent = document.querySelector(".modal-parent"),
  btn = document.querySelector(".pop-btn"),
  X = document.querySelector(".x"),
  section = document.querySelector("section");

btn.addEventListener("click", appear);

function appear() {
  parent.style.display = "block";
  section.style.filter = "blur(10px)";
}
X.addEventListener("click", disappearX);

function disappearX() {
  parent.style.display = "none";
  section.style.filter = "blur(0px)";
}
parent.addEventListener("click", disappearParent);

function disappearParent(e) {
  if (e.target.className == "modal-parent") {
      parent.style.display = "none";
      section.style.filter = "blur(0px)";
  }
}
  