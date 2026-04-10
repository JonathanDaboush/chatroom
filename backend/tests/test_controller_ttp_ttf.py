# Imports for pytest, asyncio, and controller functions
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../../'))
import pytest
import pytest_asyncio
import asyncio
from backend.repositories import clearDatabase
from backend.database import AsyncSessionLocal, engine
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
    get_call_state_controller,
    
   
)


# Fixture to cleanup database before and after each test
@pytest_asyncio.fixture(autouse=True)
async def cleanup_db():
    """Clear database before and after each test for isolation."""
    # Clear before test
    async with AsyncSessionLocal() as db:
        cd = clearDatabase(db)
        await cd.clear()
    yield
    # Clear after test and ensure all pending operations complete
    async with AsyncSessionLocal() as db:
        cd = clearDatabase(db)
        await cd.clear()
    # Small delay to ensure connections are fully released
    await asyncio.sleep(0.05)


# --- Start Call Controller TTFs ---
@pytest.mark.asyncio
async def test_start_call_controller_ttf_invalid_room():
    result = await start_call_controller(-1, 1, "audio")
    assert result is None

@pytest.mark.asyncio
async def test_start_call_controller_ttf_invalid_user():
    result = await start_call_controller(1, -1, "audio")
    assert result is None

@pytest.mark.asyncio
async def test_start_call_controller_ttf_missing_fields():
    with pytest.raises(Exception):  # Will raise exception due to None parameters
        await start_call_controller(None, None, None)  # type: ignore[arg-type]

# --- Join Call Controller TTFs ---
@pytest.mark.asyncio
async def test_join_call_controller_ttf_invalid_call():
    result = await join_call_controller(-1, 1)
    assert result is None

@pytest.mark.asyncio
async def test_join_call_controller_ttf_invalid_user():
    result = await join_call_controller(1, -1)
    assert result is None

@pytest.mark.asyncio
async def test_join_call_controller_ttf_missing_fields():
    with pytest.raises(Exception):  # Will raise TypeError due to None < int comparison
        await join_call_controller(None, None)  # type: ignore[arg-type]

# --- Leave Call Controller TTFs ---
@pytest.mark.asyncio
async def test_leave_call_controller_ttf_invalid_call():
    result = await leave_call_controller(-1, 1)
    assert result is None

@pytest.mark.asyncio
async def test_leave_call_controller_ttf_invalid_user():
    result = await leave_call_controller(1, -1)
    assert result is None

@pytest.mark.asyncio
async def test_leave_call_controller_ttf_missing_fields():
    with pytest.raises(Exception):  # Will raise TypeError due to None < int comparison
        await leave_call_controller(None, None)  # type: ignore[arg-type]

# --- End Call Controller TTFs ---
@pytest.mark.asyncio
async def test_end_call_controller_ttf_invalid_call():
    result = await end_call_controller(-1, 1)
    assert result is None

@pytest.mark.asyncio
async def test_end_call_controller_ttf_invalid_user():
    result = await end_call_controller(1, -1)
    assert result is None

@pytest.mark.asyncio
async def test_end_call_controller_ttf_missing_fields():
    with pytest.raises(Exception):  # Will raise TypeError due to None < int comparison
        await end_call_controller(None, None)  # type: ignore[arg-type]

# --- Mute User Controller TTFs ---
@pytest.mark.asyncio
async def test_mute_user_controller_ttf_invalid_call():
    result = await mute_user_controller(-1, 1, 1)
    assert result is None

@pytest.mark.asyncio
async def test_mute_user_controller_ttf_invalid_target():
    result = await mute_user_controller(1, -1, 1)
    assert result is None

@pytest.mark.asyncio
async def test_mute_user_controller_ttf_invalid_acting_user():
    result = await mute_user_controller(1, 1, -1)
    assert result is None

@pytest.mark.asyncio
async def test_mute_user_controller_ttf_missing_fields():
    with pytest.raises(Exception):  # Will raise TypeError due to None < int comparison
        await mute_user_controller(None, None, None)  # type: ignore[arg-type]

# --- Unmute User Controller TTFs ---
@pytest.mark.asyncio
async def test_unmute_user_controller_ttf_invalid_call():
    result = await unmute_user_controller(-1, 1, 1)
    assert result is None

@pytest.mark.asyncio
async def test_unmute_user_controller_ttf_invalid_target():
    result = await unmute_user_controller(1, -1, 1)
    assert result is None

@pytest.mark.asyncio
async def test_unmute_user_controller_ttf_invalid_acting_user():
    result = await unmute_user_controller(1, 1, -1)
    assert result is None

@pytest.mark.asyncio
async def test_unmute_user_controller_ttf_missing_fields():
    with pytest.raises(Exception):  # Services raise exceptions for invalid params
        await unmute_user_controller(None, 1, 1)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await unmute_user_controller(1, None, 1)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await unmute_user_controller(1, 1, None)  # type: ignore[arg-type]

# --- Get Call State Controller TTFs ---
@pytest.mark.asyncio
async def test_get_call_state_controller_ttf_invalid_call():
    result = await get_call_state_controller(-1)
    assert result is None

@pytest.mark.asyncio
async def test_get_call_state_controller_ttf_missing_call():
    result = await get_call_state_controller(None)  # type: ignore[arg-type]
    assert result is None
# --- Send Message Controller TTFs ---
@pytest.mark.asyncio
async def test_send_message_controller_ttf_invalid_user():
    with pytest.raises(Exception):
        await send_message_controller(-1, 1, "Hello")

@pytest.mark.asyncio
async def test_send_message_controller_ttf_invalid_room():
    with pytest.raises(Exception):
        await send_message_controller(1, -1, "Hello")

@pytest.mark.asyncio
async def test_send_message_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await send_message_controller(None, 1, "Hello")  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await send_message_controller(1, None, "Hello")  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await send_message_controller(1, 1, None)  # type: ignore[arg-type]

# --- Get Room Messages Controller TTFs ---
@pytest.mark.asyncio
async def test_get_room_messages_controller_ttf_invalid_room():
    result = await get_room_messages_controller(-1)
    assert result == []

@pytest.mark.asyncio
async def test_get_room_messages_controller_ttf_missing_room():
    result = await get_room_messages_controller(None)  # type: ignore[arg-type]
    assert result == []

# --- Delete Message Controller TTFs ---
@pytest.mark.asyncio
async def test_delete_message_controller_ttf_invalid_message():
    with pytest.raises(Exception):
        await delete_message_controller(-1, 1)

@pytest.mark.asyncio
async def test_delete_message_controller_ttf_invalid_user():
    with pytest.raises(Exception):
        await delete_message_controller(1, -1)

@pytest.mark.asyncio
async def test_delete_message_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await delete_message_controller(None, 1)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await delete_message_controller(1, None)  # type: ignore[arg-type]

# --- Mark As Read Controller TTFs ---
@pytest.mark.asyncio
async def test_mark_as_read_controller_ttf_invalid_message():
    with pytest.raises(Exception):
        await mark_as_read_controller(-1, 1)

@pytest.mark.asyncio
async def test_mark_as_read_controller_ttf_invalid_user():
    with pytest.raises(Exception):
        await mark_as_read_controller(1, -1)

@pytest.mark.asyncio
async def test_mark_as_read_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await mark_as_read_controller(None, 1)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await mark_as_read_controller(1, None)  # type: ignore[arg-type]

# --- Edit Message Controller TTFs ---
@pytest.mark.asyncio
async def test_edit_message_controller_ttf_invalid_message():
    with pytest.raises(Exception):
        await edit_message_controller(-1, 1, "Edit")

@pytest.mark.asyncio
async def test_edit_message_controller_ttf_invalid_user():
    with pytest.raises(Exception):
        await edit_message_controller(1, -1, "Edit")

@pytest.mark.asyncio
async def test_edit_message_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await edit_message_controller(None, 1, "Edit")  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await edit_message_controller(1, None, "Edit")  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await edit_message_controller(1, 1, None)  # type: ignore[arg-type]

# --- Reply To Message Controller TTFs ---
@pytest.mark.asyncio
async def test_reply_to_message_controller_ttf_invalid_user():
    with pytest.raises(Exception):
        await reply_to_message_controller(-1, 1, 1, "Reply")

@pytest.mark.asyncio
async def test_reply_to_message_controller_ttf_invalid_room():
    with pytest.raises(Exception):
        await reply_to_message_controller(1, -1, 1, "Reply")

@pytest.mark.asyncio
async def test_reply_to_message_controller_ttf_invalid_parent():
    with pytest.raises(Exception):
        await reply_to_message_controller(1, 1, -1, "Reply")

@pytest.mark.asyncio
async def test_reply_to_message_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await reply_to_message_controller(None, 1, 1, "Reply")  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await reply_to_message_controller(1, None, 1, "Reply")  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await reply_to_message_controller(1, 1, None, "Reply")  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await reply_to_message_controller(1, 1, 1, None)  # type: ignore[arg-type]

# --- Get Room Controller TTFs ---
@pytest.mark.asyncio
async def test_get_room_controller_ttf_invalid_room():
    with pytest.raises(Exception):
        await get_room_controller(-1)

@pytest.mark.asyncio
async def test_get_room_controller_ttf_missing_room():
    with pytest.raises(Exception):
        await get_room_controller(None)  # type: ignore[arg-type]

# --- List Members Controller TTFs ---
@pytest.mark.asyncio
async def test_list_members_controller_ttf_invalid_room():
    with pytest.raises(Exception):
        await list_members_controller(-1)

@pytest.mark.asyncio
async def test_list_members_controller_ttf_missing_room():
    with pytest.raises(Exception):
        await list_members_controller(None)  # type: ignore[arg-type]

# --- Assign Role Controller TTFs ---
@pytest.mark.asyncio
async def test_assign_role_controller_ttf_invalid_room():
    with pytest.raises(Exception):
        await assign_role_controller(-1, 1, "member", 1)

@pytest.mark.asyncio
async def test_assign_role_controller_ttf_invalid_user():
    with pytest.raises(Exception):
        await assign_role_controller(1, -1, "member", 1)

@pytest.mark.asyncio
async def test_assign_role_controller_ttf_invalid_role():
    with pytest.raises(Exception):
        await assign_role_controller(1, 1, None, 1)  # type: ignore[arg-type]

@pytest.mark.asyncio
async def test_assign_role_controller_ttf_invalid_acting_user():
    with pytest.raises(Exception):
        await assign_role_controller(1, 1, "member", -1)

@pytest.mark.asyncio
async def test_assign_role_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await assign_role_controller(None, 1, "member", 1)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await assign_role_controller(1, None, "member", 1)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await assign_role_controller(1, 1, "member", None)  # type: ignore[arg-type]

# --- Kick User Controller TTFs ---
@pytest.mark.asyncio
async def test_kick_user_controller_ttf_invalid_room():
    with pytest.raises(Exception):
        await kick_user_controller(-1, 1, 1)

@pytest.mark.asyncio
async def test_kick_user_controller_ttf_invalid_user():
    with pytest.raises(Exception):
        await kick_user_controller(1, -1, 1)

@pytest.mark.asyncio
async def test_kick_user_controller_ttf_invalid_acting_user():
    with pytest.raises(Exception):
        await kick_user_controller(1, 1, -1)

@pytest.mark.asyncio
async def test_kick_user_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await kick_user_controller(None, 1, 1)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await kick_user_controller(1, None, 1)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await kick_user_controller(1, 1, None)  # type: ignore[arg-type]

# --- Request to Join Controller TTFs ---
@pytest.mark.asyncio
async def test_request_to_join_controller_ttf_invalid_room():
    # Room does not exist
    with pytest.raises(Exception):
        await request_to_join_controller(-1, 1)

@pytest.mark.asyncio
async def test_request_to_join_controller_ttf_invalid_user():
    # User does not exist
    with pytest.raises(Exception):
        await request_to_join_controller(1, -1)

@pytest.mark.asyncio
async def test_request_to_join_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await request_to_join_controller(None, 1)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await request_to_join_controller(1, None)  # type: ignore[arg-type]

# --- Respond to Invite Controller TTFs ---
@pytest.mark.asyncio
async def test_respond_to_invite_controller_ttf_invalid_room():
    with pytest.raises(Exception):
        await respond_to_invite_controller(-1, 1, True)

@pytest.mark.asyncio
async def test_respond_to_invite_controller_ttf_invalid_user():
    with pytest.raises(Exception):
        await respond_to_invite_controller(1, -1, True)

@pytest.mark.asyncio
async def test_respond_to_invite_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await respond_to_invite_controller(None, 1, True)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await respond_to_invite_controller(1, None, True)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await respond_to_invite_controller(1, 1, None)  # type: ignore[arg-type]

# --- Join Room Controller TTFs ---
@pytest.mark.asyncio
async def test_join_room_controller_ttf_invalid_room():
    with pytest.raises(Exception):
        await join_room_controller(-1, 1)

@pytest.mark.asyncio
async def test_join_room_controller_ttf_invalid_user():
    with pytest.raises(Exception):
        await join_room_controller(1, -1)

@pytest.mark.asyncio
async def test_join_room_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await join_room_controller(None, 1)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await join_room_controller(1, None)  # type: ignore[arg-type]

# --- Leave Room Controller TTFs ---
@pytest.mark.asyncio
async def test_leave_room_controller_ttf_invalid_room():
    with pytest.raises(Exception):
        await leave_room_controller(-1, 1)

@pytest.mark.asyncio
async def test_leave_room_controller_ttf_invalid_user():
    with pytest.raises(Exception):
        await leave_room_controller(1, -1)

@pytest.mark.asyncio
async def test_leave_room_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await leave_room_controller(None, 1)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await leave_room_controller(1, None)  # type: ignore[arg-type]

from typing import Any
# Helper to get user id from result
def get_user_id(user: Any) -> int | None:
    if hasattr(user, 'user_id'):
        val = getattr(user, 'user_id')
        return int(val) if isinstance(val, (int, str)) and str(val).isdigit() else None
    if hasattr(user, 'id'):
        val = getattr(user, 'id')
        return int(val) if isinstance(val, (int, str)) and str(val).isdigit() else None
    if isinstance(user, int):
        return user
    return None

# User registration
@pytest.mark.asyncio
async def test_register_user_controller_ttp():
    result = await register_user_controller("UserTest1!", "user1@email.com", "Password1!")
    assert result is not None

@pytest.mark.asyncio

# --- Register User Controller TTFs ---
@pytest.mark.asyncio
async def test_register_user_controller_ttf_invalid_username():
    # Username does not meet requirements
    with pytest.raises(Exception, match="Failed to register user"):
        await register_user_controller("short", "valid@email.com", "Password1!")

@pytest.mark.asyncio
async def test_register_user_controller_ttf_invalid_password():
    # Password does not meet requirements
    with pytest.raises(Exception, match="Failed to register user"):
        await register_user_controller("ValidUser1!", "valid2@email.com", "short")

@pytest.mark.asyncio
async def test_register_user_controller_ttf_duplicate_email():
    # Duplicate email
    await register_user_controller("UserDup1!", "dup@email.com", "Password1!")
    with pytest.raises(Exception):
        await register_user_controller("UserDup2!", "dup@email.com", "Password1!")

@pytest.mark.asyncio
async def test_register_user_controller_ttf_missing_fields():
    # Missing username
    with pytest.raises(Exception):
        await register_user_controller(None, "missing@email.com", "Password1!")  # type: ignore[arg-type]
    # Missing email
    with pytest.raises(Exception):
        await register_user_controller("MissingEmail1!", None, "Password1!")  # type: ignore[arg-type]
    # Missing password
    with pytest.raises(Exception):
        await register_user_controller("MissingPass1!", "missingpass@email.com", None)  # type: ignore[arg-type]

@pytest.mark.asyncio
async def test_stress_register_user_controller():
    async def reg(i: int) -> None:
        try:
            await register_user_controller(f"User{i}Test!A", f"user{i}@mail.com", "Password1!")
        except Exception:
            pass
    await asyncio.gather(*(reg(i) for i in range(100)))

# User login
@pytest.mark.asyncio
async def test_login_user_controller_ttp():
    await register_user_controller("LoginUser1!", "login@email.com", "Password1!")
    result = await login_user_controller("LoginUser1!", "Password1!")
    assert result is not None

@pytest.mark.asyncio

# --- Login User Controller TTFs ---
@pytest.mark.asyncio
async def test_login_user_controller_ttf_nonexistent_user():
    # User does not exist
    with pytest.raises(Exception, match="Failed to login user"):
        await login_user_controller("nouser", "badpw")

@pytest.mark.asyncio
async def test_login_user_controller_ttf_wrong_password():
    await register_user_controller("LoginFail1!", "loginfail@email.com", "Password1!")
    with pytest.raises(Exception, match="Failed to login user.*Invalid password"):
        await login_user_controller("LoginFail1!", "WrongPassword1!")

@pytest.mark.asyncio
async def test_login_user_controller_ttf_inactive_user():
    # Simulate inactive user (status set to 'inactive')
    user = await register_user_controller("InactiveU1!", "inactive@email.com", "Password1!")
    if user is not None:
        user.status = "inactive"  # type: ignore
    result = await login_user_controller("InactiveU1!", "Password1!")
    assert result is not None  # Should reactivate, but if logic changes, check for None

@pytest.mark.asyncio
async def test_login_user_controller_ttf_missing_fields():
    # Missing username
    with pytest.raises(Exception):
        await login_user_controller(None, "Password1!")  # type: ignore[arg-type]
    # Missing password
    with pytest.raises(Exception):
        await login_user_controller("missingpassuser", None)  # type: ignore[arg-type]

@pytest.mark.asyncio
async def test_stress_login_user_controller():
    await register_user_controller("StressLogin1!", "stresslogin@email.com", "Password1!")
    async def login() -> None:
        try:
            await login_user_controller("StressLogin1!", "Password1!")
        except Exception:
            pass
    await asyncio.gather(*(login() for _ in range(100)))

# Delete user
@pytest.mark.asyncio
async def test_delete_user_controller_ttp():
    user = await register_user_controller("DeleteUser1!", "del@email.com", "Password1!")
    uid = get_user_id(user)
    assert isinstance(uid, int)
    result = await delete_user_controller(uid)
    assert result is not None

@pytest.mark.asyncio

# --- Delete User Controller TTFs ---
@pytest.mark.asyncio
async def test_delete_user_controller_ttf_nonexistent_user():
    # User does not exist
    with pytest.raises(Exception, match="Failed to delete user"):
        await delete_user_controller(-1)

@pytest.mark.asyncio
async def test_delete_user_controller_ttf_missing_id():
    # Missing user_id
    with pytest.raises(Exception, match="Failed to delete user"):
        await delete_user_controller(None)  # type: ignore[arg-type]

@pytest.mark.asyncio
async def test_stress_delete_user_controller():
    user = await register_user_controller("StressDel1!", "stressdel@email.com", "Password1!")
    uid = get_user_id(user)
    async def delete() -> None:
        try:
            if isinstance(uid, int):
                await delete_user_controller(uid)
        except Exception:
            pass
    await asyncio.gather(*(delete() for _ in range(50)))

# Get user
@pytest.mark.asyncio
async def test_get_user_controller_ttp():
    user = await register_user_controller("GetUser1!", "get@email.com", "Password1!")
    uid = get_user_id(user)
    assert isinstance(uid, int)
    result = await get_user_controller(uid)
    assert result is not None

@pytest.mark.asyncio

# --- Get User Controller TTFs ---
@pytest.mark.asyncio
async def test_get_user_controller_ttf_nonexistent_user():
    # User does not exist
    with pytest.raises(Exception, match="Failed to get user"):
        await get_user_controller(-1)

@pytest.mark.asyncio
async def test_get_user_controller_ttf_missing_id():
    # Missing user_id
    with pytest.raises(Exception, match="Failed to get user"):
        await get_user_controller(None)  # type: ignore[arg-type]

@pytest.mark.asyncio
async def test_stress_get_user_controller():
    user = await register_user_controller("StressGet1!", "stressget@email.com", "Password1!")
    uid = get_user_id(user)
    async def get() -> None:
        try:
            if isinstance(uid, int):
                await get_user_controller(uid)
        except Exception:
            pass
    await asyncio.gather(*(get() for _ in range(50)))

# Set status
@pytest.mark.asyncio
async def test_set_status_controller_ttp():
    user = await register_user_controller("StatusUser1!", "status@email.com", "Password1!")
    uid = get_user_id(user)
    assert isinstance(uid, int)
    result = await set_status_controller(uid, "online")
    assert result is not None

@pytest.mark.asyncio

# --- Set Status Controller TTFs ---
@pytest.mark.asyncio
async def test_set_status_controller_ttf_nonexistent_user():
    # User does not exist
    with pytest.raises(Exception, match="Failed to set status"):
        await set_status_controller(-1, "offline")

@pytest.mark.asyncio
async def test_set_status_controller_ttf_invalid_status():
    user = await register_user_controller("StatusFail1!", "statusfail@email.com", "Password1!")
    with pytest.raises(ValueError, match="status is required"):
        await set_status_controller(get_user_id(user), None)  # type: ignore[arg-type]

@pytest.mark.asyncio
async def test_set_status_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await set_status_controller(None, "offline")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="status is required"):
        await set_status_controller(1, None)  # type: ignore[arg-type]

@pytest.mark.asyncio
async def test_stress_set_status_controller():
    user = await register_user_controller("StressStatus1!", "stressstatus@email.com", "Password1!")
    uid = get_user_id(user)
    async def setstat() -> None:
        try:
            if isinstance(uid, int):
                await set_status_controller(uid, "busy")
        except Exception:
            pass
    await asyncio.gather(*(setstat() for _ in range(50)))

# Search users
@pytest.mark.asyncio
async def test_search_users_controller_ttp():
    await register_user_controller("SearchUser1!", "search@email.com", "Password1!")
    result = await search_users_controller("SearchUser1!")
    assert result is not None

@pytest.mark.asyncio

# --- Search Users Controller TTFs ---
@pytest.mark.asyncio
async def test_search_users_controller_ttf_empty_query():
    # Empty query string  
    with pytest.raises(ValueError, match="query is required"):
        await search_users_controller("")

@pytest.mark.asyncio
async def test_search_users_controller_ttf_missing_query():
    # Missing query
    with pytest.raises(ValueError, match="query is required"):
        await search_users_controller(None)  # type: ignore[arg-type]

@pytest.mark.asyncio
async def test_stress_search_users_controller():
    await register_user_controller("StressSearch1!", "stresssearch@email.com", "Password1!")
    async def search() -> None:
        try:
            await search_users_controller("StressSearch1!")
        except Exception:
            pass
    await asyncio.gather(*(search() for _ in range(50)))

# Room creation
@pytest.mark.asyncio
async def test_create_room_controller_ttp():
    user = await register_user_controller("RoomLead1!", "roomlead@email.com", "Password1!")
    uid = get_user_id(user)
    assert isinstance(uid, int)
    result = await create_room_controller("Test Room", uid)
    assert result is not None

@pytest.mark.asyncio

# --- Create Room Controller TTFs ---
@pytest.mark.asyncio
async def test_create_room_controller_ttf_empty_room_name():
    with pytest.raises(Exception):
        await create_room_controller("", 1)

@pytest.mark.asyncio
async def test_create_room_controller_ttf_invalid_leader_id():
    with pytest.raises(Exception):
        await create_room_controller("Valid Room", -1)

@pytest.mark.asyncio
async def test_create_room_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await create_room_controller(None, 1)  # type: ignore[arg-type]
    with pytest.raises(Exception):
        await create_room_controller("Room", None)  # type: ignore[arg-type]

@pytest.mark.asyncio
async def test_stress_create_room_controller():
    user = await register_user_controller("StressLead1!", "stresslead@email.com", "Password1!")
    uid = get_user_id(user)
    async def create(i: int) -> None:
        try:
            if isinstance(uid, int):
                await create_room_controller(f"Room{i}", uid)
        except Exception:
            pass
    await asyncio.gather(*(create(i) for i in range(50)))

# Continue this pattern for all other controller functions...
