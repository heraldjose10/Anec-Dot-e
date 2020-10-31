from flask import jsonify
from app.api.auth import auth,token_auth
from app.api import bp
from app import db


@bp.route('/tokens',methods=['POST'])
@auth.login_required
def get_token():
    token = auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token' : token})

@bp.route('/tokens',methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '',204