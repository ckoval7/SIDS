<html>
<head>
  <title>Doors</title>
  <link rel="stylesheet" href="/static/style.css" />
  <script src="/static/utilities.js"></script>
  <script src="/static/modal.js"></script>
  <script src="/static/idService.js"></script>
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
          Tier
        </th>
        <th onclick="sortTable(document.getElementById('door_info-table'), 3)">
          Password Set
        </th>
      </tr>
      % for entry in door_info:
      <tr>
        <td>{{entry[0]}}</td>
        <td>{{entry[1]}}</td>
        <td>{{entry[2]}}</td>
        % if entry[3]:
        <td style="color: #0F0; text-align: center;">&check;</td>
        % else:
        <td style="color: #F00; text-align: center;">&cross;</td>
        % end
      </tr>
      % end
    </table>
  </div>
  <div>
    <input type="button" class="medium_button no-select" id="newDoor" value="Add Door"
      onclick="showModal(document.getElementById('addDoor'))"/>
  </div>

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
        <span class="form-context">Username:</span>
        <input id="newDoorUser" type="text" />
      </div>
      <div class="row">
        <span class="form-context">Password:</span>
        <input type="password" id="newDoorPassword" />
      </div>
      <div class="row">
        <span class="form-context">Tier:</span>
        <select id="newDoorTier" name="badge-color" style="width: 185px;">
          <option value="primary">Primary</option>
          <option value="secondary">Secondary</option>
          <option value="stanard">Standard</option>
        </select>
      </div>
      <input type="button" value="Submit"
      onclick="sendNewDoor()"/>
    </div>
  </div>
</body>
</html>
