import datetime
from mysql.db_object import DBInit
from mysql.tables.receiver import Receiver


class ReceiverDB(DBInit):
    def get(self):
        infos = []
        receivers = self.session.query(Receiver).filter().all()
        for receiver in receivers:
            infos.append({
                'name': receiver.name,
                'email': receiver.email,
            })
        return {'receivers': infos}

    def upload(self, user_info):
        check = self.session.query(Receiver).filter(
            Receiver.name == user_info['name']
        ).all()
        if check:
            return {
                'status': 'error',
                'message': f"User {user_info['name']} is already exist!"
            }
        medical_order = Receiver(
            upload_time=datetime.datetime.now(),
            name=user_info['name'],
            email=user_info['email'],
        )
        self.session.add(medical_order)
        return {
            'status': 'success',
            'message': 'Done!'
        }
