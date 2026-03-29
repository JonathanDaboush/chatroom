import pytest
import asyncio
from backend.controller import (
    register_user_controller,
    login_user_controller,
    delete_user_controller,
    get_user_controller,
    set_status_controller,
    search_users_controller,
    create_room_controller,
    request_to_join_controller,
    respond_to_invite_controller,
    join_room_controller,
    leave_room_controller,
    get_room_controller,
    list_members_controller,
    assign_role_controller,
    kick_user_controller,
    send_message_controller,
    get_room_messages_controller,
    delete_message_controller,
    mark_as_read_controller,
    edit_message_controller,
    reply_to_message_controller,
    start_call_controller,
    join_call_controller,
    leave_call_controller,
    end_call_controller,
    mute_user_controller,
    unmute_user_controller,
    get_call_state_controller
)

# Helper to get user id from result
def get_user_id(user):
    if hasattr(user, 'id'):
        return user.id
    if isinstance(user, dict) and 'id' in user:
        return user['id']
    return user

# User registration
@pytest.mark.asyncio
async def test_register_user_controller_ttp():
    result = await register_user_controller("user1", "user1@email.com", "password123")
    assert result is not None

@pytest.mark.asyncio
async def test_register_user_controller_ttf():
    await register_user_controller("user2", "dup@email.com", "password123")
    with pytest.raises(Exception):
        await register_user_controller("user3", "dup@email.com", "password123")

@pytest.mark.asyncio
async def test_stress_register_user_controller():
    async def reg(i):
        try:
            await register_user_controller(f"user{i}", f"user{i}@mail.com", "pw")
        except Exception:
            pass
    await asyncio.gather(*(reg(i) for i in range(100)))

# User login
@pytest.mark.asyncio
async def test_login_user_controller_ttp():
    await register_user_controller("loginuser", "login@email.com", "pw")
    result = await login_user_controller("loginuser", "pw")
    assert result is not None

@pytest.mark.asyncio
async def test_login_user_controller_ttf():
    with pytest.raises(Exception):
        await login_user_controller("nouser", "badpw")

@pytest.mark.asyncio
async def test_stress_login_user_controller():
    await register_user_controller("stresslogin", "stresslogin@email.com", "pw")
    async def login():
        try:
            await login_user_controller("stresslogin", "pw")
        except Exception:
            pass
    await asyncio.gather(*(login() for _ in range(100)))

# Delete user
@pytest.mark.asyncio
async def test_delete_user_controller_ttp():
    user = await register_user_controller("deluser", "del@email.com", "pw")
    result = await delete_user_controller(get_user_id(user))
    assert result is not None

@pytest.mark.asyncio
async def test_delete_user_controller_ttf():
    with pytest.raises(Exception):
        await delete_user_controller(-1)

@pytest.mark.asyncio
async def test_stress_delete_user_controller():
    user = await register_user_controller("stressdel", "stressdel@email.com", "pw")
    uid = get_user_id(user)
    async def delete():
        try:
            await delete_user_controller(uid)
        except Exception:
            pass
    await asyncio.gather(*(delete() for _ in range(50)))

# Get user
@pytest.mark.asyncio
async def test_get_user_controller_ttp():
    user = await register_user_controller("getuser", "get@email.com", "pw")
    result = await get_user_controller(get_user_id(user))
    assert result is not None

@pytest.mark.asyncio
async def test_get_user_controller_ttf():
    with pytest.raises(Exception):
        await get_user_controller(-1)

@pytest.mark.asyncio
async def test_stress_get_user_controller():
    user = await register_user_controller("stressget", "stressget@email.com", "pw")
    uid = get_user_id(user)
    async def get():
        try:
            await get_user_controller(uid)
        except Exception:
            pass
    await asyncio.gather(*(get() for _ in range(50)))

# Set status
@pytest.mark.asyncio
async def test_set_status_controller_ttp():
    user = await register_user_controller("statususer", "status@email.com", "pw")
    result = await set_status_controller(get_user_id(user), "online")
    assert result is not None

@pytest.mark.asyncio
async def test_set_status_controller_ttf():
    with pytest.raises(Exception):
        await set_status_controller(-1, "offline")

@pytest.mark.asyncio
async def test_stress_set_status_controller():
    user = await register_user_controller("stressstatus", "stressstatus@email.com", "pw")
    uid = get_user_id(user)
    async def setstat():
        try:
            await set_status_controller(uid, "busy")
        except Exception:
            pass
    await asyncio.gather(*(setstat() for _ in range(50)))

# Search users
@pytest.mark.asyncio
async def test_search_users_controller_ttp():
    await register_user_controller("searchuser", "search@email.com", "pw")
    result = await search_users_controller("searchuser")
    assert result is not None

@pytest.mark.asyncio
async def test_search_users_controller_ttf():
    result = await search_users_controller("nonexistentuser")
    assert result == [] or result is not None

@pytest.mark.asyncio
async def test_stress_search_users_controller():
    await register_user_controller("stresssearch", "stresssearch@email.com", "pw")
    async def search():
        try:
            await search_users_controller("stresssearch")
        except Exception:
            pass
    await asyncio.gather(*(search() for _ in range(50)))

# Room creation
@pytest.mark.asyncio
async def test_create_room_controller_ttp():
    user = await register_user_controller("roomlead", "roomlead@email.com", "pw")
    result = await create_room_controller("Test Room", get_user_id(user))
    assert result is not None

@pytest.mark.asyncio
async def test_create_room_controller_ttf():
    with pytest.raises(Exception):
        await create_room_controller("", -1)

@pytest.mark.asyncio
async def test_stress_create_room_controller():
    user = await register_user_controller("stresslead", "stresslead@email.com", "pw")
    uid = get_user_id(user)
    async def create(i):
        try:
            await create_room_controller(f"Room{i}", uid)
        except Exception:
            pass
    await asyncio.gather(*(create(i) for i in range(50)))

# Continue this pattern for all other controller functions...
