from flask_restful import reqparse


class AuthParser:
    parser = reqparse.RequestParser()

    parser.add_argument('username', type=str, required=True,
                        help="This field can not be blank")

    parser.add_argument('password', type=str, required=True,
                        help="This field can not be blank")
