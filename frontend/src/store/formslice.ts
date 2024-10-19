import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface FormData {
  contentPreferences: {
    purpose: string;
    scriptDescription: string;
    characters: string;
    styleDetails: string;
    backgroundInfo: string;
    additionalItems: string;
    inPostText: string;
    template: string;
    visualAesthetic: string;
    colorScheme: string;
    typography: string;
    texturePatterns: string;
    postTheme: string;
    tone: string;
    contentType: string;
    targetAudience: string;
    creativeStyle: string;
    personalization: string[];
    uploadedImages: string[];  // Changed from File[] to string[]
  };
  campaignScheduling: {
    startDate: Date | null;
    endDate: Date | null;
    frequency: string;
    deliveryChannels: string[];
    bestTimeToDeliver: string;
    goals: string;
    platforms: string[];
  };
  customerData: {
    demographics: string[];
    behaviorDateRange: { start: Date | null; end: Date | null };
    interests: string[];
    engagementData: string;
    preferredChannels: string[];
  };
  brandGuidelines: {
    logo: File | null;  // Changed from File | null to string | null
    colors: string;
    tone: string;
    fonts: string;
    keyMessages: string;
  };
}

export const initialState: FormData = {
  contentPreferences: {
    purpose: '',
    scriptDescription: '',
    characters: '',
    styleDetails: '',
    backgroundInfo: '',
    additionalItems: '',
    inPostText: '',
    template: '',
    visualAesthetic: '',
    colorScheme: '',
    typography: '',
    texturePatterns: '',
    postTheme: '',
    tone: '',
    contentType: '',
    targetAudience: '',
    creativeStyle: '',
    personalization: [],
    uploadedImages: []  // Use Base64 strings here
  },
  campaignScheduling: {
    startDate: null,
    endDate: null,
    frequency: '',
    deliveryChannels: [],
    bestTimeToDeliver: '',
    goals: '',
    platforms: []
  },
  customerData: {
    demographics: [],
    behaviorDateRange: { start: null, end: null },
    interests: [],
    engagementData: '',
    preferredChannels: []
  },
  brandGuidelines: {
    logo: null,  // Use Base64 string or null here
    colors: '',
    tone: '',
    fonts: '',
    keyMessages: ''
  },
};

const formSlice = createSlice({
  name: 'form',
  initialState,
  reducers: {
    updateFormData(state, action: PayloadAction<Partial<FormData>>) {
      return { ...state, ...action.payload };
    },
    resetFormData(state) {
      return initialState;
    }
  }
});

export const { updateFormData, resetFormData } = formSlice.actions;
export default formSlice.reducer;
