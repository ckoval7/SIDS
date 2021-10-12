function getBadge() {
  let _badgeListener = function(event) {
    if (event.keyCode == 13) {
      console.log(badgeInput.value);
      badgeInput.value = "";
      closeModal(modal);
      badgeInput.removeEventListener("keypress", _badgeListener);
    }
  }
  let badgeInput = document.getElementById("badgeInput");
  let modal = document.getElementById('swipeBadge');
  showModal(modal);
  badgeInput.focus();
  badgeInput.addEventListener("keypress", _badgeListener);
}
