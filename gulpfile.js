var gulp = require('gulp'),
    watch = require('gulp-watch'),
    rename = require('gulp-rename'),
    cache = require('gulp-cached'),
    plumber = require('gulp-plumber'),
    notify = require('gulp-notify'),

    Filter = require('gulp-filter'),
    // SASS
    sass = require('gulp-sass'),
    minify = require('gulp-minify-css'),
    autoprefixer = require('gulp-autoprefixer'),
    sourcemaps = require('gulp-sourcemaps'),
    // JADE
    jade = require('gulp-jade'),
    // COFFEESCRIPT
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat')

var root = './static/';
var src = {
  sass: root + 'sass/*.sass',
  jade: root + 'jade/*.jade',
  js: root + 'js/*.js'
};

gulp.task('default', function() {
  watch(src.sass, { ignoreInitial: false }, function (files) {
    gulp.start('sass');
  });
});

gulp.task('sass', function() {
  var dest = root + 'style/';
  var once = true;
  return gulp.src(src.sass)
    .pipe(plumber({ errorHandler: function (err) {
      console.log(err.toString());
      this.emit('end');
    } }))
    .pipe(sass({ indentedSyntax: true }))
    .pipe(autoprefixer())
    .pipe(gulp.dest(dest))
    .pipe(plumber.stop())
    .pipe(notify(function () {
      if (once) {
        once = false;
        return 'SASS Finished..';
      }
      return null;
    }));
});
