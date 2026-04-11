import apiClient from './apiClient';
import { API_ENDPOINTS } from '@/config/constants';
import { Call } from '@/types';

export const callService = {
  async startCall(roomId: number): Promise<Call> {
    const response = await apiClient.post<Call>(API_ENDPOINTS.START_CALL, {
      room_id: roomId,
    });
    return response.data;
  },

  async joinCall(callId: number): Promise<void> {
    await apiClient.post(API_ENDPOINTS.JOIN_CALL(callId));
  },

  async leaveCall(callId: number): Promise<void> {
    await apiClient.post(API_ENDPOINTS.LEAVE_CALL(callId));
  },

  async toggleMute(callId: number, muted: boolean): Promise<void> {
    await apiClient.post(API_ENDPOINTS.MUTE_CALL(callId), { muted });
  },
};
