from grocery import app


if __name__=="__main__":
    app.run(port=5000, load_dotenv=True, debug=True)