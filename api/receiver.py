from flask import Blueprint, request

from mysql.crud.receiver import ReceiverDB

receiver = Blueprint('receiver', __name__)


@receiver.route('/receiver', methods=["GET"])
def get_receiver():
    with ReceiverDB() as db:
        return db.get()


@receiver.route('/receiver', methods=["POST"])
def upload_receiver():
    with ReceiverDB() as db:
        return db.upload(dict(request.values))
