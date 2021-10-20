<html>
<head>
  <title>Doors</title>
  <link rel="stylesheet" href="/static/style.css" />
  <script src="/static/utilities.js"></script>
  <script src="/static/modal.js"></script>
</head>

<body>
  % include('header.tpl')

  <div class="doors" id="door_info">
    <h1>Doors</h1>
    <table id="door_info-table">
      <tr>
        <th onclick="sortTable(document.getElementById('door_info-table'), 0)">
          Name
        </th>
        <th onclick="sortTable(document.getElementById('door_info-table'), 1)">
          Host
        </th>
        <th onclick="sortTable(document.getElementById('door_info-table'), 2)">
          Password
        </th>
      </tr>
      % for entry in door_info:
      <tr>
        <td>{{entry[0]}}</a></td>
        <td>{{entry[1]}}</a></td>
        <td>{{entry[2]}}</td>
      </tr>
      % end
    </table>
  </div>
  <input type="button" class="big_button no-select" id="newDoor" value="Add Door"
    onclick="showModal(document.getElementById('addDoor'))"/>

  <div id="addDoor" class="modal">
    <!-- Modal content -->
    <div class="modal-content">
      <span onclick="closeModal(document.getElementById('addDoor'))" class="close">
        &times;
      </span>
      <h3>Add Door</h3>
      <hr>
      <div class="row">
        <span class="form-context">Host:</span>
        <input id="newDoorHost" type="text" />
      </div>
      <div class="row">
        <span class="form-context">Password:</span>
        <input type="password" id="newDoorPassword" />
      </div>
      <input type="button" value="Submit"
      onclick="getBadge(sendNewDoor)"/>
    </div>
  </div>
</body>
</html>
