function getBadge(callback) {
  let _badgeListener = function(event) {
    if (event.keyCode == 13) {
      if (badgeInput.value) {
        console.log(badgeInput.value);
      } else {
        console.log("No Badge Data");
      }
      callback();
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

function sendNewUser() {
  let data = {};
  data.fname = document.getElementById("newUserFName").value;
  data.lname = document.getElementById("newUserLName").value;
  data.cardNum = document.getElementById("newUserBadgeNum").value;
  data.cardHex = document.getElementById("badgeInput").value;
  for (const i in data) {
    if (!data[i]) {
      alert("Fill in all the fields!");
      return "Error!";
    }
    console.log(data[i]);
  }
  const otherParams = {
      headers: {
          "content-type": "application/json"
      },
      body: JSON.stringify(data),
      method: "PUT"
  };

  fetch(`/adduser`, otherParams)
      .then(res => {
        alert("Enrollment Successful");
        closeModal(document.getElementById("addUser"));
        document.getElementById("newUserFName").value = "";
        document.getElementById("newUserLName").value = "";
        document.getElementById("newUserBadgeNum").value = "";
      });
}

function lookupBadge() {
  let data = {};
  data.cardHex = document.getElementById("badgeInput").value;
  const otherParams = {
      headers: {
          "content-type": "application/json"
      },
      body: JSON.stringify(data),
      method: "PUT"
  };
  // console.log(data);

  fetch(`/lookupbadge`, otherParams)
      .then(res => {
        // alert("Enrollment Successful");
        closeModal(document.getElementById("checkUser"));
      });
}
