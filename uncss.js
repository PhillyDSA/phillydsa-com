var http = require('http'),
    parseString = require('xml2js').parseString,
    uncss = require('uncss'),
    fs = require('fs');

var options = {
    host: 'localhost',
    port: '8000',
    path: '/sitemap.xml'
}


function createCSS(urls) {
    uncss(urls, function (error, output) {
        fs.writeFile("common/templates/common/css.html", output, function (err) {
            if (err) {
                return console.log(err);
            }
            console.log("common/templates/common/css.html saved!");
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
            createCSS(urlList)
        });
    });
});

request.on('error', function (e) {
    console.log(e.message);
});

request.end();
