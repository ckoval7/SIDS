function showModal(modal) {
  modal.style.display = "block";
  window.onclick = function(event) {
    if (event.target == modal) {
      closeModal(modal);
    }
  }
}

// When the user clicks on <span> (x), close the modal
function closeModal(modal) {
  modal.style.display = "none";
  // new_element = modal.cloneNode(true);
  // modal.parentNode.replaceChild(new_element, modal);
}
