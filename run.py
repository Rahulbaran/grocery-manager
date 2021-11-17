# from livereload import Server
from grocery import app


if __name__=="__main__":
    # server = Server(app.wsgi_app)
    # server.watch('grocery/*.py')
    # server.watch('grocery/static/scss/*.scss', delay=5)
    # server.watch('grocery/templats/*.html')
    # server.watch('grocery/static/js/*.js')
    # server.serve(port=5000,liveport=5000, host='localhost',debug=True)
    app.run(debug=True, port=5000, load_dotenv=True)
