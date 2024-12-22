import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useApi } from '../contexts/ApiContext';

interface ApiKeysResponse {
  modelscope_api_key: string;
  fish_audio_api_key: string;
}

export const useApiKeys = () => {
  const { token } = useAuth();
  const {
    setModelScopeApiKey,
    setFishAudioApiKey,
  } = useApi();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchApiKeys = async () => {
    if (!token) return;

    try {
      setLoading(true);
      setError(null);

      const response = await fetch('http://localhost:5001/api/auth/api-keys', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch API keys');
      }

      const data: ApiKeysResponse = await response.json();
      setModelScopeApiKey(data.modelscope_api_key);
      setFishAudioApiKey(data.fish_audio_api_key);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const updateApiKeys = async (modelscope_api_key?: string, fish_audio_api_key?: string) => {
    if (!token) return;

    try {
      setLoading(true);
      setError(null);

      const response = await fetch('http://localhost:5001/api/auth/api-keys', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          modelscope_api_key,
          fish_audio_api_key,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to update API keys');
      }

      const data: ApiKeysResponse = await response.json();
      setModelScopeApiKey(data.modelscope_api_key);
      setFishAudioApiKey(data.fish_audio_api_key);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApiKeys();
  }, [token]);

  return {
    loading,
    error,
    fetchApiKeys,
    updateApiKeys,
  };
};
