<html>
<head>
  <title>Entry Log</title>
  <link rel="stylesheet" href="/static/style.css" />
  <script src="/static/utilities.js"></script>
</head>

<body>
  % include('header.tpl')
  <div class="logbook" id="entrylog">
    <h1 style="margin: auto;">Entry/Exit Log</h1>
    <table id="entrylog-table">
      <tr>
        <th onclick="sortTable(document.getElementById('entrylog-table'), 0)">
          Last Name
        </th>
        <th onclick="sortTable(document.getElementById('entrylog-table'), 1)">
          First Name
        </th>
        <th onclick="sortTable(document.getElementById('entrylog-table'), 2)">
          Direction
        </th>
        <th onclick="sortTable(document.getElementById('entrylog-table'), 3)">
          Date/Time
        </th>
      </tr>
      % for entry in log:
        % if entry[0] == None:
        <tr style="background: #6e1010;">
        % else:
        <tr>
        % end
        <td>{{entry[0]}}</td>
        <td>{{entry[1]}}</td>
        <td>{{"In" if entry[2] == "in" else "Out"}}</td>
        <td>{{entry[3]}}</td>
      </tr>
      % end
    </table>
  </div>
</body>
</html>
