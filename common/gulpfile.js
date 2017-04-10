var gulp = require('gulp'),
    watch = require('gulp-watch'),
    livereload = require('gulp-livereload'),
    tachyonsSrc = './static/tachyons/css',
    tachyonsDest = './static/css/tachyons/prod';

gulp.task('tach', function() {
    gulp.src(tachyonsSrc + '/**/*', {base: tachyonsSrc})
        .pipe(watch(tachyonsSrc, {base: tachyonsSrc}))
        .pipe(gulp.dest(tachyonsDest))
});

gulp.task('watch', function() {
    livereload.listen();

    gulp.watch([
        tachyonsSrc,
        '**/static/css/*',
        '**/templates/*',
        '**/templates/**/*'
    ]).on('change', livereload.changed);
});

gulp.task('default', ['watch']);
