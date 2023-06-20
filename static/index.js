// dashboard
const menu = document.querySelector(".menu");
const menuBars = document.querySelector(".fa-bars");
const menuArrow = document.querySelector(".fa-arrow-up");
const flyoutWrap = document.querySelector(".flyout-wrap");
const flyouts = document.querySelectorAll(".flyout");

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