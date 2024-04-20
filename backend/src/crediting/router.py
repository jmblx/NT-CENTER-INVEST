import fastapi

from crediting.processing_model import use_model

router = fastapi.APIRouter(prefix="/credit", tags=["credit"])


@router.post("/processing_request")
async def processing_request(
    data: dict,
):
    result = (use_model(data))[0][0]
    data = {key: value[0] for key, value in data.items()}
    data["is_good_client"] = float(result)

    return {"result": str(result)}

#
# # Эндпоинт получения всех заявок пользователя
# @router.get("/get_requests")
# async def get_requests(
#     user: User = Depends(current_user)
# ):
#     requests = await get_data(
#         class_=Request,
#         filter=Request.user_id == user.id,
#         is_scalar=False,
#         order_by=Request.created_at
#     )
#     return requests
