<html>
<head>
  <title>Who's Here</title>
  <link rel="stylesheet" href="/static/style.css" />
  <script src="/static/utilities.js"></script>
</head>

<body>
  % include('header.tpl')
  <div class="logbook" id="whoshere">
    <h1 style="margin: auto;">Who's Here</h1>
    <table id="whoshere-table">
      <tr>
        <th onclick="sortTable(document.getElementById('whoshere-table'), 0)">
          Last Name
        </th>
        <th onclick="sortTable(document.getElementById('whoshere-table'), 1)">
          First Name
        </th>
        <th onclick="sortTable(document.getElementById('whoshere-table'), 2)">
          Time In
        </th>
      </tr>
      % for user in users:
      <tr>
        <td>{{user[1]}}</td>
        <td>{{user[0]}}</td>
        <td>{{user[2]}}</td>
      </tr>
      % end
    </table>
  </div>
</body>
</html>
