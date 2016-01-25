// Modeled after gulpfile here:
// https://hacks.mozilla.org/2014/08/browserify-and-gulp-with-react/
var gulp = require('gulp');
var reactify = require('reactify');
var browserify = require('browserify');
var del = require('del');
var source = require('vinyl-source-stream');
var eslint = require('gulp-eslint');
var babel = require('gulp-babel');
var transform = require('vinyl-transform');
var babelify = require('babelify');

var paths = {
    jsx: ['static/populate-array.jsx'],
    js: 'static/populate-array.js'
};

gulp.task('clean', function(done) {
    del(paths.js, done);
});

gulp.task('lint', function() {
    return gulp.src(paths.jsx)
    .pipe(eslint())
    .pipe(eslint.format())
    .pipe(eslint.failOnError());
});

gulp.task('build', function() {
    browserify(paths.jsx)
    .transform('babelify', {presets: ['es2015', 'react']})
    .bundle()
    .pipe(source(paths.js))
    .pipe(gulp.dest('./'));
});

gulp.task('watch', ['lint', 'build'], function() {
    gulp.watch(paths.jsx, ['lint', 'build']);
});

gulp.task('default', ['watch', 'build']);
