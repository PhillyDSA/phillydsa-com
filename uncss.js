var http = require('http'),
    parseString = require('xml2js').parseString,
    uncss = require('uncss'),
    fs = require('fs');

var options = {
    host: 'localhost',
    port: '8000',
    path: '/sitemap.xml'
}

var uncss_options = {
    stylesheets: ['/static/css/tachyons/css/tachyons.min.css'],
    csspath: '/static/css/tachyons/css/tachyons.min.css'
}

function replaceAll(str, find, replace) {
    return str.replace(new RegExp(find, 'g'), replace);
}

function createCSS(urls) {
    uncss(urls, uncss_options, function (error, output) {
        if (error) {
            return console.log(error);
        }
        console.log(output)
        var hardcoded_output = replaceAll(output, "url\\(\\.\\.\\/", "url(/static/")

        fs.writeFile("common/templates/common/css.html", hardcoded_output, function (err) {
            if (err) {
                return console.log(err);
            }
            console.log("common/templates/common/css.html saved!");
        });

        fs.writeFile("common/static/specific/phillydsa-style.min.css", output, function (err) {
            if (err) {
                return console.log(err);
            }
            console.log("common/static/specific/phillydsa-style.min.css saved!");
        });
    });
}


request = http.request(options, function (res) {
    var data = '';
    res.on('data', function (chunk) {
        data += chunk;
    });
    res.on('end', function () {
        parseString(data, function (err, result) {
            var urlArray = result['urlset']['url']
            var urlList = []
            for (var i = 0; i < urlArray.length; i++) {
                urlList.push(urlArray[i]['loc'][0].replace('localhost', 'localhost:8000'));
            }
            console.log(urlList)
            createCSS(urlList)
        });
    });
});

request.on('error', function (e) {
    console.log(e.message);
});

request.end();
