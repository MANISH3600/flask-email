from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_mail import Mail, Message
import os

app = Flask(__name__)
api = Api(app)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True


app.config['MAIL_USERNAME'] = os.getenv('GMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_PASSWORD')

mail = Mail(app)


class SendEmail(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('receiver_email', type=str, required=True)
        parser.add_argument('subject', type=str, required=True)
        parser.add_argument('body_text', type=str, required=True)
        args = parser.parse_args()

        receiver_email = args['receiver_email']
        subject = args['subject']
        body_text = args['body_text']

        msg = Message(subject=subject,
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[receiver_email])
        msg.body = body_text

        try:
            mail.send(msg)
            return {'message': 'Email sent successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500


api.add_resource(SendEmail, '/send-email')

if __name__ == '__main__':
    app.run(debug=True)