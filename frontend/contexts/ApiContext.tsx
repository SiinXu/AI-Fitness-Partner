import React, { createContext, useContext, useState, useEffect } from 'react';

interface ApiContextType {
  modelScopeApiKey: string;
  fishAudioApiKey: string;
  setModelScopeApiKey: (key: string) => void;
  setFishAudioApiKey: (key: string) => void;
  isConfigured: boolean;
}

const ApiContext = createContext<ApiContextType>({
  modelScopeApiKey: '',
  fishAudioApiKey: '',
  setModelScopeApiKey: () => {},
  setFishAudioApiKey: () => {},
  isConfigured: false,
});

export const useApi = () => useContext(ApiContext);

export const ApiProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [modelScopeApiKey, setModelScopeApiKey] = useState('');
  const [fishAudioApiKey, setFishAudioApiKey] = useState('');

  useEffect(() => {
    // Load API keys from localStorage on mount
    const storedModelScopeKey = localStorage.getItem('modelscope_api_key');
    const storedFishAudioKey = localStorage.getItem('fish_audio_api_key');
    
    if (storedModelScopeKey) setModelScopeApiKey(storedModelScopeKey);
    if (storedFishAudioKey) setFishAudioApiKey(storedFishAudioKey);
  }, []);

  const handleSetModelScopeApiKey = (key: string) => {
    setModelScopeApiKey(key);
    localStorage.setItem('modelscope_api_key', key);
  };

  const handleSetFishAudioApiKey = (key: string) => {
    setFishAudioApiKey(key);
    localStorage.setItem('fish_audio_api_key', key);
  };

  const isConfigured = Boolean(modelScopeApiKey && fishAudioApiKey);

  return (
    <ApiContext.Provider
      value={{
        modelScopeApiKey,
        fishAudioApiKey,
        setModelScopeApiKey: handleSetModelScopeApiKey,
        setFishAudioApiKey: handleSetFishAudioApiKey,
        isConfigured,
      }}
    >
      {children}
    </ApiContext.Provider>
  );
};
