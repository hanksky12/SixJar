from flask import Blueprint

commands_bp = Blueprint('commands', __name__, cli_group=None)#下命令 可省略 commands 單字


from . import commands