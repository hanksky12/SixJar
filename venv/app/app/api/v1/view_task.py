from flask import Response
import json
import time
from flask_apispec import MethodResource, use_kwargs, marshal_with, doc

from ... import celery
from .schema import EmptySchema


class TaskApi(MethodResource):
    @doc(tags=["Task"])
    @use_kwargs(EmptySchema, location="querystring")
    @marshal_with(None, code=200, description='Success')
    def get(self, task_id, **kwargs):
        def generate():
            while True:
                result = celery.AsyncResult(task_id)
                if result.status == 'PENDING':
                    current = 0
                    total = 1
                elif result.status == 'FAILURE':
                    current = 0
                    total = 1
                else:
                    current = result.result.get('current', 0)
                    total = result.result.get('total', 1)
                response_data = {'status': result.status, 'current': current, 'total': total}
                sse_str = f"data: {json.dumps(response_data)}\n\n"
                # print(sse_str)
                yield sse_str
                if result.ready():
                    break
                time.sleep(1)

        return Response(generate(), mimetype='text/event-stream')

    def delete(self):
        pass
