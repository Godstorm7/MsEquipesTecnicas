from flask import request, jsonify, current_app
import requests


def jwt_required():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify(message="Token é necessário!"), 403

    url_token_validate = current_app.config["TOKEN_VALIDATE_URL"]

    headers = {
        "Authorization": token
    }

    try:
        response = requests.get(url_token_validate, headers=headers, timeout=3)
        response.raise_for_status()

    except requests.RequestException:
        return jsonify(message="Token inválido ou expirado!"), 403
    return None