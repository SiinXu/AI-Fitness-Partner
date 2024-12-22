import React, { useState } from 'react';
import { useApi } from '../contexts/ApiContext';
import { useApiKeys } from '../hooks/useApiKeys';

const ApiConfig: React.FC = () => {
  const {
    modelScopeApiKey,
    fishAudioApiKey,
    isConfigured,
  } = useApi();

  const { loading, error, updateApiKeys } = useApiKeys();

  const [showKeys, setShowKeys] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [tempModelScopeKey, setTempModelScopeKey] = useState(modelScopeApiKey);
  const [tempFishAudioKey, setTempFishAudioKey] = useState(fishAudioApiKey);

  const handleSave = async () => {
    try {
      await updateApiKeys(tempModelScopeKey, tempFishAudioKey);
      setIsEditing(false);
    } catch (err) {
      console.error('Failed to update API keys:', err);
    }
  };

  const handleCancel = () => {
    setTempModelScopeKey(modelScopeApiKey);
    setTempFishAudioKey(fishAudioApiKey);
    setIsEditing(false);
  };

  if (!isEditing) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">API Configuration</h2>
          <button
            onClick={() => setIsEditing(true)}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            disabled={loading}
          >
            Edit
          </button>
        </div>
        <div className="space-y-4">
          <div>
            <p className="font-medium">ModelScope API Key:</p>
            <p className="text-gray-600">
              {showKeys ? modelScopeApiKey || 'Not configured' : '••••••••••••••••'}
            </p>
          </div>
          <div>
            <p className="font-medium">Fish Audio API Key:</p>
            <p className="text-gray-600">
              {showKeys ? fishAudioApiKey || 'Not configured' : '••••••••••••••••'}
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowKeys(!showKeys)}
              className="text-sm text-blue-500 hover:text-blue-600"
              disabled={loading}
            >
              {showKeys ? 'Hide Keys' : 'Show Keys'}
            </button>
          </div>
          {error && (
            <div className="text-sm text-red-500">
              {error}
            </div>
          )}
          <div className="mt-4">
            <p className="text-sm">
              Status:{' '}
              <span
                className={`font-medium ${
                  isConfigured ? 'text-green-500' : 'text-red-500'
                }`}
              >
                {isConfigured ? 'Configured' : 'Not Configured'}
              </span>
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Edit API Configuration</h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            ModelScope API Key
          </label>
          <input
            type="text"
            value={tempModelScopeKey}
            onChange={(e) => setTempModelScopeKey(e.target.value)}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter ModelScope API Key"
            disabled={loading}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Fish Audio API Key
          </label>
          <input
            type="text"
            value={tempFishAudioKey}
            onChange={(e) => setTempFishAudioKey(e.target.value)}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter Fish Audio API Key"
            disabled={loading}
          />
        </div>
        {error && (
          <div className="text-sm text-red-500">
            {error}
          </div>
        )}
        <div className="flex justify-end space-x-2 pt-4">
          <button
            onClick={handleCancel}
            className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
            disabled={loading}
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className={`px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors ${
              loading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
            disabled={loading}
          >
            {loading ? 'Saving...' : 'Save'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ApiConfig;
