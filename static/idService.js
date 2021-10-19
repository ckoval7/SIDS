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
  .then(response => response.text())
  .then(data => {
    closeModal(document.getElementById("checkUser"));
    // console.log('Success:', data);
    window.location.href = data;
  });
}

function lookupName() {
  let data = {};
  let badgeNum = document.getElementById("lookupBadgeNum").value;
  let fName = document.getElementById("lookupFName").value;
  let lName = document.getElementById("lookupLName").value;
  if(!badgeNum) {
    if(fName && lName) {
      data.fname = fName;
      data.lname = lName;
      const otherParams = {
        headers: {
          "content-type": "application/json"
        },
        body: JSON.stringify(data),
        method: "PUT"
      };
      // console.log(data);

      fetch(`/lookupname`, otherParams)
      .then(response => response.text())
      .then(data => {
        closeModal(document.getElementById("checkUser"));
        // console.log('Success:', data);
        window.location.href = data;
      });
    } else {
      alert("Fill in both first and last name, or use badge number.");
    }
  } else {
    closeModal(document.getElementById("checkUser"));
    window.location.href = '/profile/' + badgeNum;
  }
}
