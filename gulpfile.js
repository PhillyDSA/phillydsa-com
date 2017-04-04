var gulp = require('gulp'),
    watch = require('gulp-watch');
    sass = require('gulp-ruby-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    cssnano = require('gulp-cssnano'), jshint = require('gulp-jshint'),
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    rename = require('gulp-rename'),
    concat = require('gulp-concat'),
    notify = require('gulp-notify'),
    cache = require('gulp-cache'),
    livereload = require('gulp-livereload'),
    del = require('del');

gulp.task('style', function() {
    return sass('static/sass/style.sass', { style: 'expanded' })
        .pipe(autoprefixer('last 2 version'))
        .pipe(gulp.dest('static/css/prod'))
        .pipe(rename({suffix: '.min'}))
        .pipe(cssnano())
        .pipe(gulp.dest('static/css/prod'));
});

gulp.task('watch', function() {
    gulp.watch('static/sass/**/*.sass', ['style']);

    livereload.listen();

    gulp.watch([
        '**/templates/*',
        '**/templates/**/*'
    ]).on('change', livereload.changed);
});

gulp.task('default', ['watch']);
