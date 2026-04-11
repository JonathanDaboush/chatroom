import { create } from 'zustand';
import { Call, CallParticipant, User } from '@/types';

interface CallState {
  activeCall: Call | null;
  participants: CallParticipant[];
  mutedUsers: Set<number>;
  isMuted: boolean;
  
  // Actions
  setActiveCall: (call: Call | null) => void;
  setParticipants: (participants: CallParticipant[]) => void;
  addParticipant: (user: User) => void;
  removeParticipant: (userId: number) => void;
  toggleMute: (userId: number) => void;
  toggleSelfMute: () => void;
  clearCall: () => void;
}

export const useCallStore = create<CallState>((set) => ({
  activeCall: null,
  participants: [],
  mutedUsers: new Set(),
  isMuted: false,

  setActiveCall: (call) => set({ activeCall: call }),

  setParticipants: (participants) => set({ participants }),

  addParticipant: (user) => set((state) => ({
    participants: [...state.participants, { user, muted: false }],
  })),

  removeParticipant: (userId) => set((state) => ({
    participants: state.participants.filter((p) => p.user.id !== userId),
  })),

  toggleMute: (userId) => set((state) => {
    const newMutedUsers = new Set(state.mutedUsers);
    if (newMutedUsers.has(userId)) {
      newMutedUsers.delete(userId);
    } else {
      newMutedUsers.add(userId);
    }
    return { mutedUsers: newMutedUsers };
  }),

  toggleSelfMute: () => set((state) => ({
    isMuted: !state.isMuted,
  })),

  clearCall: () => set({
    activeCall: null,
    participants: [],
    mutedUsers: new Set(),
    isMuted: false,
  }),
}));
