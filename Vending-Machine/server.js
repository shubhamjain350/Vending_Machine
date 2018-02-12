const express = require('express')
const srv = express();
var PythonShell = require('python-shell');





srv.get('/hello', function (req, res) {
    res.send("Hello")
})

srv.get('/run_script', function (req, res) {
    PythonShell.run('get_pulse.py', function (err) {
        if (err) throw err;
        console.log('finished');
      });
});

srv.use('/public', express.static(__dirname + "/public"))



srv.listen(1234);