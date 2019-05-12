from analysis_interface import app, logger

@app.route('/')
def index():
    logger.info("HOME")
    return 'Analysis Interface.'


if __name__ == '__main__':
    app.run()
