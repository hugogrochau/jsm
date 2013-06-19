var express = require('express'),
    http = require('http'),
    nib = require('nib'),
    stylus = require('stylus'),
    ejs = require('ejs');

var app = module.exports = express();

var compileStylus = function(str, path) {
    return stylus(str)
        .set('filename', path)
        .set('warn', true)
        .set('compress', true)
        .use(nib());
};


app.engine('.html', ejs.__express);
app.set('port', process.env.PORT || 3000);
app.set('views', __dirname + '/views');
app.set('view engine', 'html');
app.use(express.favicon());
app.use(express.bodyParser());
app.use(express.methodOverride());

app.use(stylus.middleware({
    src: __dirname + '/public',
    compile: compileStylus
}));

app.use(express.static(__dirname + '/public'));

if ('development' == app.get('env')) {
    console.log('Running development version');
    app.use(express.logger('dev'));
    app.use(express.errorHandler({
        dumpExceptions: true,
        showStack: true
    }));
} else console.log('Running production version');

app.get('/', function(req, res) {
    res.render('index');
});

app.get('/mapa', function(req, res) {
    res.render('mapa');
});

app.get('/prealistamento', function(req, res) {
    res.render('prealistamento');
});


http.createServer(app).listen(app.get('port'), function() {
    console.log('Express server listening on port ' + app.get('port'));
});