<html>
<head>
  <title>User Profile</title>
  <link rel="stylesheet" href="/static/style.css" />
  <script src="/static/utilities.js"></script>
</head>

<body>
  % include('header.tpl')

  <div class="logbook" id="user_info">
    <h1>User</h1>
    <table id="user_info-table">
      <tr>
        <th onclick="sortTable(document.getElementById('user_info-table'), 0)">
          Last Name
        </th>
        <th onclick="sortTable(document.getElementById('user_info-table'), 1)">
          First Name
        </th>
        <th onclick="sortTable(document.getElementById('user_info-table'), 2)">
          Badge Number
        </th>
      </tr>
      % for entry in user_info:
      % badge_num = entry[2]
      <tr>
        <td><a href="/profile/{{badge_num}}">{{entry[0]}}</a></td>
        <td><a href="/profile/{{badge_num}}">{{entry[1]}}</a></td>
        <td><a href="/profile/{{badge_num}}">{{badge_num}}</a></td>
      </tr>
      % end
    </table>
  </div>
% if log is not None:
  <div class="logbook" id="user_entrylog">
    <hr>
    <h1>Entry/Exit Log</h1>
    <table id="user_entrylog-table">
      <tr>
        <th onclick="sortTable(document.getElementById('user_entrylog-table'), 0)">
          Time
        </th>
        <th onclick="sortTable(document.getElementById('user_entrylog-table'), 1)">
          Direction
        </th>
      </tr>
      % for entry in log:
        <tr>
        <td>{{entry[0]}}</td>
        <td>{{entry[1]}}</td>
      </tr>
      % end
    </table>
  </div>
% end
</body>
</html>
