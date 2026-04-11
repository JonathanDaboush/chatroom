import apiClient from './apiClient';
import { API_ENDPOINTS } from '@/config/constants';
import { Message, SendMessageRequest, UpdateMessageRequest } from '@/types';

export const messageService = {
  async getMessages(roomId: number): Promise<Message[]> {
    const response = await apiClient.get<Message[]>(
      API_ENDPOINTS.ROOM_MESSAGES(roomId)
    );
    return response.data;
  },

  async sendMessage(
    roomId: number,
    data: SendMessageRequest
  ): Promise<Message> {
    const response = await apiClient.post<Message>(
      API_ENDPOINTS.ROOM_MESSAGES(roomId),
      data
    );
    return response.data;
  },

  async updateMessage(
    messageId: number,
    data: UpdateMessageRequest
  ): Promise<Message> {
    const response = await apiClient.put<Message>(
      API_ENDPOINTS.MESSAGE_BY_ID(messageId),
      data
    );
    return response.data;
  },

  async deleteMessage(messageId: number): Promise<void> {
    await apiClient.delete(API_ENDPOINTS.MESSAGE_BY_ID(messageId));
  },
};
