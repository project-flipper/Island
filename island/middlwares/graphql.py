import json
from typing import Any, Union

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from starlette.concurrency import iterate_in_threadpool

from island.models import Error, Response


class GraphQLResponse(Response[dict]):
    error: Union[Error, Any] = None


class GraphQLResponseMiddleware:
    async def __call__(self, request: Request, call_next):
        response = await call_next(request)
        if "/data/graphql/" not in request.url.path:
            return response

        response_body = [chunk async for chunk in response.body_iterator]
        res_json = json.loads(response_body[0])
        res_json["hasError"] = "error" in res_json
        res_json["success"] = "data" in res_json
        res_model = GraphQLResponse(**res_json)
        json_data = json.dumps(jsonable_encoder(res_model)).encode()
        response_body[0] = json_data
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        response.headers["Content-Length"] = str(len(json_data))
        return response
