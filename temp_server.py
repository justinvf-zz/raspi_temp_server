#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import timeseries_db
from config import TOO_COLD, NAME, PORT_NUMBER

page_template = """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {{packages:["corechart"]}});
      google.setOnLoadCallback(drawChart);
      function drawChart() {{

        var data = google.visualization.arrayToDataTable([
          ['Time', 'Temperature (F)'], {}
        ]);

        var options = {{
          title: '7 Day Temperature'
        }};

        var chart = new google.visualization.LineChart(document.getElementById('chart7_div'));
        chart.draw(data, options);


        var data = google.visualization.arrayToDataTable([
          ['Time', 'Temperature (F)'], {}
        ]);

        var options = {{
          title: '24 Hour Temperature'
        }};

        var chart = new google.visualization.LineChart(document.getElementById('chart24_div'));
        chart.draw(data, options);


        var data = google.visualization.arrayToDataTable([
          ['Time', 'Temperature (F)'], {}
        ]);

        var options = {{
          title: '60 Minute Temperature'
        }};

        var chart = new google.visualization.LineChart(document.getElementById('chart60_div'));
        chart.draw(data, options);

      }}
    </script>
  </head>
  <body>
    <center><h2>{}</h2></center>
    <div id="chart7_div" style="width: 1400px; height: 500px;"></div>
    <div id="chart24_div" style="width: 900px; height: 500px;"></div>
    <div id="chart60_div" style="width: 900px; height: 500px;"></div>
  </body>
</html>
"""

def build_hacky_list(temp_times):
    # Little hack to make it into js list format..
    return ",\n".join("['{}', {:.3f}]".format(*t_t) for t_t in temp_times)

def build_response():
    temp_times_minutes = timeseries_db.get_last_60_minutes()
    temp_times_hours = timeseries_db.get_last_24_hours()
    temp_times_days = timeseries_db.get_last_7_days()

    last_temp = temp_times_minutes[-1][1]
    if last_temp > TOO_COLD:
        msg = "It should be safe to leave bed."
    else:
        msg = "It's a little cold. Better stay in bed."
    intro = ("Hello {}! It is {:.2f} degrees F.<br> {}"
             .format(NAME, last_temp, msg))
    return page_template.format(intro,
                                build_hacky_list(temp_times_days),
                                build_hacky_list(temp_times_hours)
                                build_hacky_list(temp_times_minutes))

class tempServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(build_response())


if __name__ == '__main__':
    try:
        server = HTTPServer(('', PORT_NUMBER), tempServerHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
