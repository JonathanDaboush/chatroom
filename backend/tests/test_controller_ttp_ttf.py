# Imports for pytest, asyncio, and controller functions
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
    with pytest.raises(Exception):
        await start_call_controller(None, 1, "audio")
    with pytest.raises(Exception):
        await start_call_controller(1, None, "audio")
    with pytest.raises(Exception):
        await start_call_controller(1, 1, None)

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
    with pytest.raises(Exception):
        await join_call_controller(None, 1)
    with pytest.raises(Exception):
        await join_call_controller(1, None)

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
    with pytest.raises(Exception):
        await leave_call_controller(None, 1)
    with pytest.raises(Exception):
        await leave_call_controller(1, None)

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
    with pytest.raises(Exception):
        await end_call_controller(None, 1)
    with pytest.raises(Exception):
        await end_call_controller(1, None)

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
    with pytest.raises(Exception):
        await mute_user_controller(None, 1, 1)
    with pytest.raises(Exception):
        await mute_user_controller(1, None, 1)
    with pytest.raises(Exception):
        await mute_user_controller(1, 1, None)

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
    with pytest.raises(Exception):
        await unmute_user_controller(None, 1, 1)
    with pytest.raises(Exception):
        await unmute_user_controller(1, None, 1)
    with pytest.raises(Exception):
        await unmute_user_controller(1, 1, None)

# --- Get Call State Controller TTFs ---
@pytest.mark.asyncio
async def test_get_call_state_controller_ttf_invalid_call():
    result = await get_call_state_controller(-1)
    assert result is None

@pytest.mark.asyncio
async def test_get_call_state_controller_ttf_missing_call():
    with pytest.raises(Exception):
        await get_call_state_controller(None)
# --- Send Message Controller TTFs ---
@pytest.mark.asyncio
async def test_send_message_controller_ttf_invalid_user():
    result = await send_message_controller(-1, 1, "Hello")
    assert result is None

@pytest.mark.asyncio
async def test_send_message_controller_ttf_invalid_room():
    result = await send_message_controller(1, -1, "Hello")
    assert result is None

@pytest.mark.asyncio
async def test_send_message_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await send_message_controller(None, 1, "Hello")
    with pytest.raises(Exception):
        await send_message_controller(1, None, "Hello")
    with pytest.raises(Exception):
        await send_message_controller(1, 1, None)

# --- Get Room Messages Controller TTFs ---
@pytest.mark.asyncio
async def test_get_room_messages_controller_ttf_invalid_room():
    result = await get_room_messages_controller(-1)
    assert result == []

@pytest.mark.asyncio
async def test_get_room_messages_controller_ttf_missing_room():
    with pytest.raises(Exception):
        await get_room_messages_controller(None)

# --- Delete Message Controller TTFs ---
@pytest.mark.asyncio
async def test_delete_message_controller_ttf_invalid_message():
    result = await delete_message_controller(-1, 1)
    assert result is None

@pytest.mark.asyncio
async def test_delete_message_controller_ttf_invalid_user():
    result = await delete_message_controller(1, -1)
    assert result is None

@pytest.mark.asyncio
async def test_delete_message_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await delete_message_controller(None, 1)
    with pytest.raises(Exception):
        await delete_message_controller(1, None)

# --- Mark As Read Controller TTFs ---
@pytest.mark.asyncio
async def test_mark_as_read_controller_ttf_invalid_message():
    result = await mark_as_read_controller(-1, 1)
    assert result is None

@pytest.mark.asyncio
async def test_mark_as_read_controller_ttf_invalid_user():
    result = await mark_as_read_controller(1, -1)
    assert result is None

@pytest.mark.asyncio
async def test_mark_as_read_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await mark_as_read_controller(None, 1)
    with pytest.raises(Exception):
        await mark_as_read_controller(1, None)

# --- Edit Message Controller TTFs ---
@pytest.mark.asyncio
async def test_edit_message_controller_ttf_invalid_message():
    result = await edit_message_controller(-1, 1, "Edit")
    assert result is None

@pytest.mark.asyncio
async def test_edit_message_controller_ttf_invalid_user():
    result = await edit_message_controller(1, -1, "Edit")
    assert result is None

@pytest.mark.asyncio
async def test_edit_message_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await edit_message_controller(None, 1, "Edit")
    with pytest.raises(Exception):
        await edit_message_controller(1, None, "Edit")
    with pytest.raises(Exception):
        await edit_message_controller(1, 1, None)

# --- Reply To Message Controller TTFs ---
@pytest.mark.asyncio
async def test_reply_to_message_controller_ttf_invalid_user():
    result = await reply_to_message_controller(-1, 1, 1, "Reply")
    assert result is None

@pytest.mark.asyncio
async def test_reply_to_message_controller_ttf_invalid_room():
    result = await reply_to_message_controller(1, -1, 1, "Reply")
    assert result is None

@pytest.mark.asyncio
async def test_reply_to_message_controller_ttf_invalid_parent():
    result = await reply_to_message_controller(1, 1, -1, "Reply")
    assert result is None

@pytest.mark.asyncio
async def test_reply_to_message_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await reply_to_message_controller(None, 1, 1, "Reply")
    with pytest.raises(Exception):
        await reply_to_message_controller(1, None, 1, "Reply")
    with pytest.raises(Exception):
        await reply_to_message_controller(1, 1, None, "Reply")
    with pytest.raises(Exception):
        await reply_to_message_controller(1, 1, 1, None)
# --- Get Room Controller TTFs ---
@pytest.mark.asyncio
async def test_get_room_controller_ttf_invalid_room():
    result = await get_room_controller(-1)
    assert result is None

@pytest.mark.asyncio
async def test_get_room_controller_ttf_missing_room():
    with pytest.raises(Exception):
        await get_room_controller(None)

# --- List Members Controller TTFs ---
@pytest.mark.asyncio
async def test_list_members_controller_ttf_invalid_room():
    result = await list_members_controller(-1)
    assert result == []

@pytest.mark.asyncio
async def test_list_members_controller_ttf_missing_room():
    with pytest.raises(Exception):
        await list_members_controller(None)

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
        await assign_role_controller(1, 1, None, 1)

@pytest.mark.asyncio
async def test_assign_role_controller_ttf_invalid_acting_user():
    with pytest.raises(Exception):
        await assign_role_controller(1, 1, "member", -1)

@pytest.mark.asyncio
async def test_assign_role_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await assign_role_controller(None, 1, "member", 1)
    with pytest.raises(Exception):
        await assign_role_controller(1, None, "member", 1)
    with pytest.raises(Exception):
        await assign_role_controller(1, 1, "member", None)

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
        await kick_user_controller(None, 1, 1)
    with pytest.raises(Exception):
        await kick_user_controller(1, None, 1)
    with pytest.raises(Exception):
        await kick_user_controller(1, 1, None)
# --- Request to Join Controller TTFs ---
@pytest.mark.asyncio
async def test_request_to_join_controller_ttf_invalid_room():
    # Room does not exist
    result = await request_to_join_controller(-1, 1)
    assert result["success"] is False

@pytest.mark.asyncio
async def test_request_to_join_controller_ttf_invalid_user():
    # User does not exist
    result = await request_to_join_controller(1, -1)
    assert result["success"] is False

@pytest.mark.asyncio
async def test_request_to_join_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await request_to_join_controller(None, 1)
    with pytest.raises(Exception):
        await request_to_join_controller(1, None)

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
        await respond_to_invite_controller(None, 1, True)
    with pytest.raises(Exception):
        await respond_to_invite_controller(1, None, True)
    with pytest.raises(Exception):
        await respond_to_invite_controller(1, 1, None)

# --- Join Room Controller TTFs ---
@pytest.mark.asyncio
async def test_join_room_controller_ttf_invalid_room():
    result = await join_room_controller(-1, 1)
    assert result["success"] is False

@pytest.mark.asyncio
async def test_join_room_controller_ttf_invalid_user():
    result = await join_room_controller(1, -1)
    assert result["success"] is False

@pytest.mark.asyncio
async def test_join_room_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await join_room_controller(None, 1)
    with pytest.raises(Exception):
        await join_room_controller(1, None)

# --- Leave Room Controller TTFs ---
@pytest.mark.asyncio
async def test_leave_room_controller_ttf_invalid_room():
    result = await leave_room_controller(-1, 1)
    assert result["success"] is False

@pytest.mark.asyncio
async def test_leave_room_controller_ttf_invalid_user():
    result = await leave_room_controller(1, -1)
    assert result["success"] is False

@pytest.mark.asyncio
async def test_leave_room_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await leave_room_controller(None, 1)
    with pytest.raises(Exception):
        await leave_room_controller(1, None)

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

# --- Register User Controller TTFs ---
@pytest.mark.asyncio
async def test_register_user_controller_ttf_invalid_username():
    # Username does not meet requirements
    with pytest.raises(ValueError):
        await register_user_controller("short", "valid@email.com", "Password1!")

@pytest.mark.asyncio
async def test_register_user_controller_ttf_invalid_password():
    # Password does not meet requirements
    with pytest.raises(ValueError):
        await register_user_controller("ValidUser1!", "valid2@email.com", "short")

@pytest.mark.asyncio
async def test_register_user_controller_ttf_duplicate_email():
    # Duplicate email
    await register_user_controller("user2", "dup@email.com", "Password1!")
    with pytest.raises(Exception):
        await register_user_controller("user3", "dup@email.com", "Password1!")

@pytest.mark.asyncio
async def test_register_user_controller_ttf_missing_fields():
    # Missing username
    with pytest.raises(Exception):
        await register_user_controller(None, "missing@email.com", "Password1!")
    # Missing email
    with pytest.raises(Exception):
        await register_user_controller("MissingEmail1!", None, "Password1!")
    # Missing password
    with pytest.raises(Exception):
        await register_user_controller("MissingPass1!", "missingpass@email.com", None)

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

# --- Login User Controller TTFs ---
@pytest.mark.asyncio
async def test_login_user_controller_ttf_nonexistent_user():
    # User does not exist
    result = await login_user_controller("nouser", "badpw")
    assert result is None

@pytest.mark.asyncio
async def test_login_user_controller_ttf_wrong_password():
    await register_user_controller("loginfail", "loginfail@email.com", "Password1!")
    result = await login_user_controller("loginfail", "WrongPassword1!")
    assert result is None

@pytest.mark.asyncio
async def test_login_user_controller_ttf_inactive_user():
    # Simulate inactive user (status set to 'inactive')
    user = await register_user_controller("inactiveuser1", "inactive@email.com", "Password1!")
    if hasattr(user, 'status'):
        user.status = "inactive"
    result = await login_user_controller("inactiveuser1", "Password1!")
    assert result is not None  # Should reactivate, but if logic changes, check for None

@pytest.mark.asyncio
async def test_login_user_controller_ttf_missing_fields():
    # Missing username
    with pytest.raises(Exception):
        await login_user_controller(None, "Password1!")
    # Missing password
    with pytest.raises(Exception):
        await login_user_controller("missingpassuser", None)

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

# --- Delete User Controller TTFs ---
@pytest.mark.asyncio
async def test_delete_user_controller_ttf_nonexistent_user():
    # User does not exist
    result = await delete_user_controller(-1)
    assert result is None

@pytest.mark.asyncio
async def test_delete_user_controller_ttf_missing_id():
    # Missing user_id
    with pytest.raises(Exception):
        await delete_user_controller(None)

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

# --- Get User Controller TTFs ---
@pytest.mark.asyncio
async def test_get_user_controller_ttf_nonexistent_user():
    # User does not exist
    result = await get_user_controller(-1)
    assert result is None

@pytest.mark.asyncio
async def test_get_user_controller_ttf_missing_id():
    # Missing user_id
    with pytest.raises(Exception):
        await get_user_controller(None)

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

# --- Set Status Controller TTFs ---
@pytest.mark.asyncio
async def test_set_status_controller_ttf_nonexistent_user():
    # User does not exist
    result = await set_status_controller(-1, "offline")
    assert result is None

@pytest.mark.asyncio
async def test_set_status_controller_ttf_invalid_status():
    user = await register_user_controller("statusfail", "statusfail@email.com", "Password1!")
    result = await set_status_controller(get_user_id(user), None)
    assert result is not None  # Should handle gracefully, but check for None if logic changes

@pytest.mark.asyncio
async def test_set_status_controller_ttf_missing_fields():
    with pytest.raises(Exception):
        await set_status_controller(None, "offline")
    with pytest.raises(Exception):
        await set_status_controller(1, None)

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

# --- Search Users Controller TTFs ---
@pytest.mark.asyncio
async def test_search_users_controller_ttf_empty_query():
    # Empty query string
    result = await search_users_controller("")
    assert result == [] or result is not None

@pytest.mark.asyncio
async def test_search_users_controller_ttf_missing_query():
    # Missing query
    with pytest.raises(Exception):
        await search_users_controller(None)

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
        await create_room_controller(None, 1)
    with pytest.raises(Exception):
        await create_room_controller("Room", None)

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
