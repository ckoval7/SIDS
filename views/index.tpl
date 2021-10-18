<html>
<head>
  <title>SIDS</title>
  <link rel="stylesheet" href="/static/style.css">
  <script src="/static/modal.js"></script>
  <script src="/static/idService.js"></script>
</head>
<body>
  % include('header.tpl')
  <div class="main">
    <input type="button" class="big_button no-select" id="newUser" value="Add User"
      onclick="showModal(document.getElementById('addUser'))"/>
    <input type="button" class="big_button no-select" value="Check User"
      onclick="showModal(document.getElementById('checkUser'))"/>
    <br>
    <input type="button" class="big_button no-select" value="Update User" />
    <input type="button" class="big_button no-select" value="Lost Badge" />
  </div>

  <div id="addUser" class="modal">
    <!-- Modal content -->
    <div class="modal-content">
      <span onclick="closeModal(document.getElementById('addUser'))" class="close">
        &times;
      </span>
      <h3>Add User</h3>
      <hr>
      <div class="row">
        <span class="form-context">First Name:</span>
        <input id="newUserFName" type="text" />
      </div>
      <div class="row">
        <span class="form-context">Last Name:</span>
        <input id="newUserLName" type="text" />
      </div>
      <div class="row">
        <span class="form-context">Badge Number:</span>
        <input id="newUserBadgeNum" type="text" />
      </div>
      <div class="row">
        <span class="form-context">Badge Color:</span>
        <select id="newUserBadgeColor" name="badge-color" style="width: 185px;">
          <option value="blue">Blue</option>
          <option value="green">Green</option>
          <option value="orange">Orange</option>
          <option value="white">White</option>
          <option value="red">Red</option>
        </select>
      </div>
      <input type="button" value="Enroll"
      onclick="getBadge(sendNewUser)"/>
    </div>
  </div>

  <div id="checkUser" class="modal">
    <div class="modal-content">
      <span onclick="closeModal(document.getElementById('checkUser'))" class="close">
        &times;
      </span>
      <h3>Check User</h3>
      <hr>
      <div class="lookup_div">
        <div class="row"
          style="margin: auto; width: fit-content; bottom: 30px; position: relative;">
          <input style="vertical-align: bottom;" class="big_button" type="button"
            onclick="getBadge(lookupBadge)" value="Read Badge">
        </div>
      </div>
      <div class="lookup_div">
        <h4>Lookup Name:</h4>
        <div class="row">
          <span class="form-context">First Name:</span>
          <input id="lookupFName" />
        </div>
        <div class="row">
          <span class="form-context">Last Name:</span>
          <input id="lookupLName" />
        </div>
        <div class="row">
          <span class="form-context">OR</span>
        </div>
        <div class="row">
          <span class="form-context">Badge Number:</span>
          <input id="lookupBadgeNum" />
        </div>
        <input type="button" value="Search">
    </div>
  </div>

  <div id="swipeBadge" class="modal">
    <div onclick="document.getElementById('badgeInput').focus()" class="modal-content">
      <span onclick="closeModal(document.getElementById('swipeBadge'))" class="close">
        &times;
      </span>
      <div id="swipeBadge-content">
        <span id="swipeBadge-text" class="no-select">Swipe badge on reader</span>
        <input type="text" id="badgeInput"
          onfocusin="document.getElementById('swipeBadge-content').style.background = '#76e576'"
          onfocusout="document.getElementById('swipeBadge-content').style.background = '#e57676'"/>
      </div>
    </div>
  </div>
</body>
</html>
