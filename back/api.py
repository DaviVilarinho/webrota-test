from flask import Flask

app = Flask(__name__)

@app.route("/user-coordinates", methods=["GET"])
def getUserCoordinates():
    return {
        "data": [{
			"date_time": "2019-02-12T10:57:36+00:00", 
			"latitude": "-18.92406700", 
			"longitude": "-48.28214200"
        }, 
        {
			"date_time": "2019-02-12T10:57:06+00:00", 
			"latitude": "-18.92376500", 
			"longitude": "-48.28210800" 
        }, 
        {
			"date_time": "2019-02-12T10:56:36+00:00", 
			"latitude": "-18.92213500", 
			"longitude": "-48.28205200"
        }, 
        {
			"date_time": "2019-02-12T10:56:06+00:00", 
			"latitude": "-18.92082200", 
			"longitude": "-48.28132800"
        }, 
        {
			"date_time": "2019-02-12T10:55:36+00:00", 
			"latitude": "-18.91951300", 
			"longitude": "-48.28033200"
        }, 
        {
			"date_time": "2019-02-12T10:55:06+00:00", 
			"latitude": "-18.91966300", 
			"longitude": "-48.27849800"
        }, 
        {
			"date_time": "2019-02-12T10:54:36+00:00", 
			"latitude": "-18.92081800", 
			"longitude": "-48.27682200"
        }, 
        {
			"date_time": "2019-02-12T10:54:06+00:00", 
			"latitude": "-18.92195000", 
			"longitude": "-48.27513200"
        }, 
        {
			"date_time": "2019-02-12T10:53:36+00:00", 
			"latitude": "-18.92298100", 
			"longitude": "-48.27350800"
        }, 
        {
			"date_time": "2019-02-12T10:53:06+00:00", 
			"latitude": "-18.92313700", 
			"longitude": "-48.27337200"
        }, 
        {
			"date_time": "2019-02-12T10:52:36+00:00", 
			"latitude": "-18.92372200", 
			"longitude": "-48.27213800"
        }, 
        {
			"date_time": "2019-02-12T10:52:06+00:00", 
			"latitude": "-18.92295000", 
			"longitude": "-48.27078200"
        }, 
        {
			"date_time": "2019-02-12T10:51:36+00:00", 
			"latitude": "-18.91990800", 
			"longitude": "-48.26785500"
        }, 
        {
			"date_time": "2019-02-12T10:51:06+00:00", 
			"latitude": "-18.91765300", 
			"longitude": "-48.26528000"
        }, 
        {
			"date_time": "2019-02-12T10:50:36+00:00", 
			"latitude": "-18.91815100", 
			"longitude": "-48.26453900"
        }, 
        {
			"date_time": "2019-02-12T10:50:06+00:00", 
			"latitude": "-18.91814500", 
			"longitude": "-48.26453700"
        }]
    }, 200