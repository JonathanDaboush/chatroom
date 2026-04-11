import apiClient from './apiClient';
import { API_ENDPOINTS } from '@/config/constants';
import { Room, CreateRoomRequest } from '@/types';

export const roomService = {
  async getRooms(): Promise<Room[]> {
    const response = await apiClient.get<Room[]>(API_ENDPOINTS.ROOMS);
    return response.data;
  },

  async createRoom(data: CreateRoomRequest): Promise<Room> {
    const response = await apiClient.post<Room>(API_ENDPOINTS.ROOMS, data);
    return response.data;
  },

  async joinRoom(roomId: number): Promise<void> {
    await apiClient.post(API_ENDPOINTS.JOIN_ROOM(roomId));
  },

  async leaveRoom(roomId: number): Promise<void> {
    await apiClient.post(API_ENDPOINTS.LEAVE_ROOM(roomId));
  },
};
