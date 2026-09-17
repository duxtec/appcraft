from flask import Blueprint, jsonify, request

from application.schemas.input.user import UserInSchema
from application.use_cases.user.create import CreateUserUseCase
from application.use_cases.user.get import ReadUserUseCase
from domain.filters import EqualFilter
from domain.models.user import User
from infrastructure.dependency.container import ApplicationContainer


def register() -> Blueprint:
    bp = Blueprint("user", __name__)

    @bp.route("/users", methods=["POST"])
    def create_user():  # type: ignore
        create_uc = ApplicationContainer.get(CreateUserUseCase)
        payload = UserInSchema(**request.get_json())
        user = create_uc.execute(payload)
        return jsonify(user.model_dump()), 201

    @bp.route("/users/<int:id>")
    def get_user(id: int):  # type: ignore
        read_uc = ApplicationContainer.get(ReadUserUseCase)
        user = read_uc.execute([EqualFilter(User.id, id)])
        if user:
            return jsonify(user[0].model_dump())
        return jsonify({"message": "User not found"}), 404

    return bp
