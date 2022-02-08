const Express = require("express");
var app = Express();
app.use(Express.static(__dirname + '/public'));
app.use(Express.json());

require('dotenv').config()
var favicon = require('serve-favicon');
var path = require('path');
app.use(favicon(path.join(__dirname,'public','images','logo.ico')));
var _ = require('underscore');

app.listen(3000, () => console.log('listening at 3000'));
