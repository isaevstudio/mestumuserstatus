from userstatus import app
from flask import request, jsonify 
import pandas as pd
from config import *
from userstatus.models import StreamingStatus
from sqlalchemy import create_engine
import jwt
import datetime


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        engine = create_engine(app.config['DATABASE'])
        dbConnection = engine.connect()
        df  = pd.read_sql(app.config['SELECT_DF'], dbConnection)
        dbConnection.close()

        value_counts = df.sort_values(by="time").drop_duplicates(subset=["user_id"], keep="last")['status'].value_counts()

        list_id=list(df.sort_values(by="time").drop_duplicates(subset=["user_id"], keep="last").loc[df.sort_values(by="time").drop_duplicates(subset=["user_id"], keep="last")['status']==0]['user_id'])
        _list = []

        for i in list_id:   
            encoded_jwt = jwt.encode({"user_id": i, 'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=60)}, "secret", algorithm="HS256")
            _list.append(encoded_jwt)

        return jsonify({"Pause": str(value_counts[1]),
                        "Play": str(value_counts[0]),
                        'List of user id': _list})
    else:
        _user_id = request.json.get('user_id', -1)
        _streaming = request.json.get('streaming', -1)
        _time = request.json.get('time', -1)
        _status = request.json.get('status', -1)

        if _user_id != -1 or _streaming != -1 or _time != -1 or _status != -1:
            StreamingStatus.insert(
                user_id = _user_id,
                streaming = _streaming,
                time = _time,
                status = _status).execute()
            return "Done"
        else:
            return jsonify({'msg':'Missing data'})