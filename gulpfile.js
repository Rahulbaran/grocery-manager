const {src,dest,watch,series} = require('gulp');
const scss = require('gulp-sass')(require('sass'));
const postcss = require('gulp-postcss');
const cssnano = require('cssnano');
const prefixer = require('autoprefixer');
const sourcemaps = require('gulp-sourcemaps');
const terser = require('gulp-terser');
const concat = require('gulp-concat');





//scss task
const scssTask = function () {
    return src('static/scss/*.scss')
    .pipe(scss())
    .pipe(sourcemaps.init())
    .pipe(postcss([cssnano(),prefixer()]))
    .pipe(sourcemaps.write('.'))
    .pipe(dest('static/css'))
};


//Js task
const jsTask = function () {
    return src('static/js/*.js')
    .pipe(sourcemaps.init())
    .pipe(terser())
    .pipe(sourcemaps.write('.'))
    .pipe(dest('static/minjs'))
};


//watch task
const watchTask = function () {
    watch('static/scss/*.scss',{delay : 1000}, scssTask);
    watch('static/js/*.js', jsTask);  
};



exports.default = series(
    scssTask,
    jsTask,
    watchTask
);