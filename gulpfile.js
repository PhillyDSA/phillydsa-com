var gulp = require('gulp'),
    watch = require('gulp-watch'),
    livereload = require('gulp-livereload');

gulp.task('watch', function() {
    livereload.listen();

    gulp.watch([
        '**/templates/*',
        '**/templates/**/*'
    ]).on('change', livereload.changed);
});

gulp.task('default', ['watch']);
